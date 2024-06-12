from typing import Dict, Hashable


def delete_state(state: Dict, key: Hashable):
    if state.has(key) and state[key] is not None:
        state[key] = None
