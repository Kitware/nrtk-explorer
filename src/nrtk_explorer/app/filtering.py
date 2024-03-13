from typing import Callable, Iterable

from nrtk_explorer.app.applet import Applet

from trame.widgets import quasar, html
from trame.ui.quasar import QLayout

from trame.app import get_server

from nrtk_explorer.library.filtering import (
    FilterProtocol,
    NotFilter,
    ConcreteIdFilter,
)

from nrtk_explorer.widgets.nrtk_explorer import FilterOptionsWidget, FilterOperatorWidget


class FilteringApp(Applet):
    def __init__(self, server):
        super().__init__(server)

        self._on_apply_filter = lambda _filter: None

        self.state.categories = {
            0: {"id": 0, "name": "a"},
            1: {"id": 1, "name": "b"},
            2: {"id": 2, "name": "c"},
            3: {"id": 3, "name": "d"},
            4: {"id": 4, "name": "e"},
            5: {"id": 5, "name": "f"},
        }
        self.state.filter_categories = []
        self.state.filter_operator = "or"
        self.state.filter_not = False

        self.server.controller.add("on_server_ready")(self.on_server_ready)

        self._filter = ConcreteIdFilter()
        self._not_filter = NotFilter(self._filter)

        self._ui = None

    def set_on_apply_filter(self, fn: Callable[[FilterProtocol[Iterable[int]]], None]):
        self._on_apply_filter = fn

    def on_server_ready(self, *args, **kwargs):
        # Bind instance methods to state change
        self.on_filter_categories_change()
        self.state.change("filter_categories")(self.on_filter_categories_change)
        self.state.change("filter_operator")(self.on_filter_categories_change)

    def on_apply_click(self):
        if self.state.filter_not:
            self._on_apply_filter(self._not_filter)
        else:
            self._on_apply_filter(self._filter)

    def on_filter_categories_change(self, **kwargs):
        self._filter.set_ids(self.state.filter_categories, self.state.filter_operator)

    def on_update_operator(self, operator, **kwargs):
        self.state.filter_operator = operator

    def on_update_filter_not(self, filter_not):
        self.state.filter_not = filter_not

    def filter_options_ui(self):
        with html.Div(trame_server=self.server):
            FilterOptionsWidget(
                v_model=("filter_categories",),
                options=("categories",),
            )

    def filter_operator_ui(self):
        with html.Div(trame_server=self.server):
            FilterOperatorWidget(
                operator=("filter_operator",),
                invert=("filter_not",),
                **{
                    "update:operator": (self.on_update_operator, "[$event]"),
                    "update:invert": (self.on_update_filter_not, "[$event]"),
                },
            )

    def filter_apply_ui(self):
        with html.Div(trame_server=self.server):
            quasar.QBtn(
                "Apply",
                click=(self.on_apply_click,),
                flat=True,
            )

    @property
    def ui(self):
        if self._ui is None:
            with QLayout(self.server) as layout:
                self._ui = layout

                with quasar.QDrawer(
                    v_model=("leftDrawerOpen", True),
                    side="left",
                    elevated=True,
                ):
                    self.filter_operator_ui()

                    self.filter_options_ui()

                    self.filter_apply_ui()

                with quasar.QPageContainer():
                    with quasar.QPage():
                        with html.Div(classes="row", style="min-height: inherit;"):
                            with html.Div(classes="col q-pa-md"):
                                pass

        return self._ui


def filtering(server=None, *args, **kwargs):
    server = get_server()
    server.client_type = "vue3"

    app = FilteringApp(server)

    a, b, c = (0, 1, 2)

    test_values = [
        [],
        [a],
        [b],
        [c],
        [a, b],
        [a, c],
        [b, c],
        [a, b, c],
    ]

    def on_apply_filter(filter: FilterProtocol):
        result = list(map(filter.evaluate, test_values))

        for value, res in zip(test_values, result):
            print(value, res)

    app.set_on_apply_filter(on_apply_filter)

    app.ui

    server.start(**kwargs)


if __name__ == "__main__":
    filtering()
