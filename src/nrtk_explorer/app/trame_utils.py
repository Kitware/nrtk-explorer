from typing import Hashable
from trame_server.state import State


def delete_state(state: State, key: Hashable):
    if state.has(key) and state[key] is not None:
        state[key] = None
