import asyncio
from functools import wraps
from trame.app import asynchronous


def debounce(wait, state=None):
    """Pass Trame state as arg if function modifies state"""

    def decorator(func):
        task = None

        @wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal task
            if task:
                task.cancel()

            async def debounced():
                await asyncio.sleep(wait)
                result = func(*args, **kwargs)
                if asyncio.iscoroutine(result):
                    await result
                if state:
                    state.flush()

            task = asynchronous.create_task(debounced())

        return wrapper

    return decorator
