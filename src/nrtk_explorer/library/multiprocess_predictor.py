import multiprocessing
import asyncio
import signal
import threading
import logging
import queue
import uuid
from enum import Enum
from .predictor import Predictor


class Command(Enum):
    SET_MODEL = "SET_MODEL"
    INFER = "INFER"
    RESET = "RESET"


def _child_worker(request_queue, result_queue, model_name, force_cpu):
    signal.signal(signal.SIGINT, signal.SIG_IGN)  # Ignore Ctrl+C in child
    logger = logging.getLogger(__name__)
    predictor = Predictor(model_name=model_name, force_cpu=force_cpu)

    while True:
        try:
            msg = request_queue.get()
        except (EOFError, KeyboardInterrupt):
            logger.debug("Worker: Exiting on interrupt or queue EOF.")
            break
        if msg is None:  # Exit signal
            logger.debug("Worker: Received EXIT command. Shutting down.")
            break

        command = Command(msg["command"])
        req_id = msg["req_id"]
        payload = msg.get("payload", {})

        if command == Command.SET_MODEL:
            try:
                predictor = Predictor(
                    model_name=payload["model_name"], force_cpu=payload["force_cpu"]
                )
                result_queue.put((req_id, {"status": "OK"}))
            except Exception as e:
                logger.exception("Failed to set model.")
                result_queue.put((req_id, {"status": "ERROR", "message": str(e)}))
        elif command == Command.INFER:
            try:
                predictions = predictor.eval(payload["images"])
                result_queue.put((req_id, {"status": "OK", "result": predictions}))
            except Exception as e:
                logger.exception("Inference failed.")
                result_queue.put((req_id, {"status": "ERROR", "message": str(e)}))
        elif command == Command.RESET:
            try:
                predictor.reset()
                result_queue.put((req_id, {"status": "OK"}))
            except Exception as e:
                logger.exception("Reset failed.")
                result_queue.put((req_id, {"status": "ERROR", "message": str(e)}))

        del msg
        del command
        del req_id
        del payload

    logger.debug("Worker: shutting down.")


class MultiprocessPredictor:
    def __init__(self, model_name="facebook/detr-resnet-50", force_cpu=False):
        self._lock = threading.Lock()
        self.model_name = model_name
        self.force_cpu = force_cpu
        self._proc = None
        self._request_queue = None
        self._result_queue = None
        self._pending_futures = {}
        self._result_thread = None

        self.loop = asyncio.get_event_loop()

        self._start_process()

        # Start a dedicated thread for responses instead of scheduling an async task.
        self._result_thread = threading.Thread(target=self._result_listener, daemon=True)
        self._result_thread.start()

        self.loop.add_signal_handler(signal.SIGINT, self.shutdown)

    def _start_process(self):
        with self._lock:
            if self._proc is not None and self._proc.is_alive():
                self.shutdown()
            multiprocessing.set_start_method("spawn", force=True)
            self._request_queue = multiprocessing.Queue()
            self._result_queue = multiprocessing.Queue()
            self._proc = multiprocessing.Process(
                target=_child_worker,
                args=(
                    self._request_queue,
                    self._result_queue,
                    self.model_name,
                    self.force_cpu,
                ),
                daemon=True,
            )
            self._proc.start()

    def _result_listener(self):
        while True:
            try:
                result = self._result_queue.get()
            except (EOFError, KeyboardInterrupt):
                break
            if result is None:
                break
            r_id, payload = result
            with self._lock:
                future = self._pending_futures.pop(r_id, None)
            if future and not future.done():
                self.loop.call_soon_threadsafe(future.set_result, payload)

    async def _submit_request(self, command, payload):
        future = self.loop.create_future()
        req_id = str(uuid.uuid4())

        def cleanup(_):
            with self._lock:
                self._pending_futures.pop(req_id, None)
                # Remove the request if it's still in the queue. Probably got canceled.
                stashed_requests = []
                while not self._request_queue.empty():
                    try:
                        req = self._request_queue.get_nowait()
                        if req["req_id"] != req_id:
                            stashed_requests.append(req)
                    except queue.Empty:
                        break
                for req in stashed_requests:
                    self._request_queue.put(req)

        future.add_done_callback(cleanup)

        with self._lock:
            self._pending_futures[req_id] = future

        self._request_queue.put(
            {
                "command": command.value,
                "req_id": req_id,
                "payload": payload,
            }
        )

        try:
            r = await future
            return r
        except asyncio.CancelledError:
            cleanup(None)
            raise

    async def infer(self, images):
        if not images:
            return {}
        resp = await self._submit_request(Command.INFER, {"images": images})
        return resp.get("result")

    def _run_coro(self, coro):
        if self.loop.is_running():
            return asyncio.ensure_future(coro)
        else:
            return self.loop.run_until_complete(coro)

    def set_model(self, model_name, force_cpu=False):
        with self._lock:
            self.model_name = model_name
            self.force_cpu = force_cpu

        async def _async_set():
            return await self._submit_request(
                Command.SET_MODEL, {"model_name": self.model_name, "force_cpu": self.force_cpu}
            )

        return self._run_coro(_async_set())

    def reset(self):
        async def _async_reset():
            return await self._submit_request(Command.RESET, {})

        return self._run_coro(_async_reset())

    def shutdown(self):
        async def _async_shutdown():
            with self._lock:
                try:
                    self._request_queue.put(None)
                    self._result_queue.put(None)  # Signal the listener thread to exit.
                except Exception:
                    logging.warning("Could not send exit message to worker.")
            if self._proc:
                self._proc.join()
            if self._result_thread:
                self._result_thread.join()

        return self._run_coro(_async_shutdown())
