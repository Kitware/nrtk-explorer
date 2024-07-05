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
        await asyncio.sleep(0.1)
        await asyncio.sleep(0)
