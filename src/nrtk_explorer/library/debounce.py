import asyncio
from functools import wraps


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
                            await func(*args, **kwargs)
                    else:
                        await func(*args, **kwargs)
                except asyncio.CancelledError:
                    pass

            task = asyncio.create_task(debounced())

        return wrapper

    return decorator
