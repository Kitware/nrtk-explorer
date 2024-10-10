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
                try:
                    await asyncio.sleep(wait)
                    if state:
                        with state:
                            result = func(*args, **kwargs)
                    else:
                        result = func(*args, **kwargs)

                    if asyncio.iscoroutine(result):
                        await result
                except asyncio.CancelledError:
                    pass

            task = asynchronous.create_task(debounced())

        return wrapper

    return decorator
