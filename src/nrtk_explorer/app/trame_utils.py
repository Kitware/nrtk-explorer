from typing import Hashable, Callable
from trame_server import Server
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


class ProcessingStep:
    def __init__(
        self,
        server: Server,
        feature_enabled_state_key: str,
        gui_switch_key: str,
        column_name: str,
        enabled_callback: Callable,
    ):
        self.state = server.state
        self.feature_enabled_state_key = feature_enabled_state_key
        self.gui_switch_key = gui_switch_key
        self.enabled_callback = enabled_callback
        self.column_name = column_name
        self.state.change(self.gui_switch_key)(self.on_gui_switch)
        self.update_feature_enabled_state()
        self.state.change("visible_columns", self.gui_switch_key)(
            self.update_feature_enabled_state
        )
        self.state.change(self.feature_enabled_state_key)(self.on_change_feature_enabled)

    def on_gui_switch(self, **kwargs):
        if self.state[self.gui_switch_key]:
            self.state.visible_columns = list(set([*self.state.visible_columns, self.column_name]))
        else:
            self.state.visible_columns = [
                col for col in self.state.visible_columns if col != self.column_name
            ]

    def update_feature_enabled_state(self, **kwargs):
        self.state[self.feature_enabled_state_key] = (
            self.column_name in self.state.visible_columns and self.state[self.gui_switch_key]
        )

    def on_change_feature_enabled(self, **kwargs):
        if self.state[self.feature_enabled_state_key]:
            self.enabled_callback()
