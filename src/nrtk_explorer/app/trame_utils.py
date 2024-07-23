import asyncio
from typing import Hashable
from trame_server.state import State


def delete_state(state: State, key: Hashable):
    if state.has(key) and state[key] is not None:
        state[key] = None


class SetStateAsync:
    def __init__(self, state: State):
        self.state = state

    async def __aenter__(self):
        return self.state

    async def __aexit__(self, exc_type, exc, tb):
        self.state.flush()
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await asyncio.sleep(0)


def diff(a, b):
    return a != b


def change_checker(state, key, callback, trigger_check=diff):
    old_value = state[key]

    def on_change():
        nonlocal old_value
        new_value = state[key]
        if trigger_check(old_value, new_value):
            callback()
        old_value = new_value

    def on_state(**kwargs):
        on_change()

    state.change(key)(on_state)
