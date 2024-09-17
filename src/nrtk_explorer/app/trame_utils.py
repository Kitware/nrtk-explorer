from typing import Hashable, Callable
from trame_server.state import State


def delete_state(state: State, key: Hashable):
    if state.has(key) and state[key] is not None:
        state[key] = None


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
