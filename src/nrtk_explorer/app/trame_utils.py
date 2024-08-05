import asyncio
from typing import Hashable, Callable
from trame_server.state import State


def delete_state(state: State, key: Hashable):
    if state.has(key) and state[key] is not None:
        state[key] = None


class SetStateAsync:
    """
    Usage::
        async with SetStateAsync(state):
            state["key"] = value
    """

    def __init__(self, state: State):
        self.state = state

    async def __aenter__(self):
        await asyncio.sleep(0)  # give task.cancel() a chance to trigger early exit
        return self.state

    async def __aexit__(self, exc_type, exc, tb):
        self.state.flush()
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await asyncio.sleep(0)


def change_checker(state: State, key: str, trigger_check=lambda a, b: a != b):
    """
    Usage::
        @change_checker(self.state, "visible_columns", transformed_became_visible)
        def on_apply_transform(old_value, new_value):
    """

    def decorator(callback: Callable):
        old_value = state[key]

        def on_change():
            nonlocal old_value
            new_value = state[key]
            if trigger_check(old_value, new_value):
                callback(old_value, new_value)
            old_value = new_value

        def on_state(**kwargs):
            on_change()

        state.change(key)(on_state)
        return callback

    return decorator
