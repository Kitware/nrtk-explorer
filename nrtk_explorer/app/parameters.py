from typing import Dict

from nrtk_explorer.app.applet import Applet

from trame.widgets import quasar, html
from trame.ui.quasar import QLayout

from trame.app import get_server

from nrtk_explorer.widgets.nrtk_explorer import ParamsWidget

from nrtk_explorer.library.transforms import (
    ImageTransform,
    GaussianBlurTransform,
    IdentityTransform,
    TestTransform,
)


def on_change(*args, **kwargs):
    print(args, kwargs)


transforms: Dict[str, ImageTransform] = {
    "TestTransform": TestTransform(),
    "GaussianBlurTransform": GaussianBlurTransform(),
    "IdentityTransform": IdentityTransform(),
}


class TransformsApp(Applet):
    def __init__(self, server, state_translator=None, controller_translator=None):
        super().__init__(server, state_translator, controller_translator)

        self.state.current_transform = "TestTransform"

        self.on_current_transform_change()

        self.state.change("current_transform")(self.on_current_transform_change)

        self._ui = None

    def on_current_transform_change(self, **kwargs):
        print("current transform changed", self.state.current_transform)
        transform = transforms[self.state.current_transform]
        self.state.params_values = transform.get_parameters()
        self.state.params_descriptions = transform.get_parameters_description()

    def on_transform_parameters_changed(self, parameters, **kwargs):
        print("on_transform_parameters_changed", parameters, kwargs)
        transform = transforms[self.state.current_transform]
        transform.set_parameters(parameters)
        self.state.params_values = transform.get_parameters()

    def transform_select_ui(self):
        quasar.QSelect(
            label="Dataset",
            v_model=(self.state_translator("current_transform"),),
            options=(list(transforms.keys()),),
            filled=True,
            emit_value=True,
            map_options=True,
        )

    def transform_params_ui(self):
        ParamsWidget(
            values=("params_values",),
            descriptions=("params_descriptions",),
            valuesChanged=(self.on_transform_parameters_changed, "[$event]"),
        )

    @property
    def ui(self):
        if self._ui is None:
            with QLayout(self.server) as layout:
                self._ui = layout

                with quasar.QDrawer(
                    v_model=(self.state_translator("leftDrawerOpen"), True),
                    side="left",
                    elevated=True,
                ):
                    self.transform_select_ui()

                    with html.Div(
                        classes="q-pa-md q-ma-md",
                        style="border-style: solid; border-width: thin; border-radius: 0.5rem; border-color: lightgray;",
                    ):
                        self.transform_params_ui()

                with quasar.QPageContainer():
                    with quasar.QPage():
                        with html.Div(classes="row", style="min-height: inherit;"):
                            with html.Div(classes="col q-pa-md"):
                                pass

        return self._ui


def main(server=None, *args, **kwargs):
    server = get_server()
    server.client_type = "vue3"

    app = TransformsApp(server)
    app.ui

    server.start(**kwargs)


if __name__ == "__main__":
    main()
