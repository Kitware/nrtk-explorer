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


class ParametersApp(Applet):
    def __init__(self, server):
        super().__init__(server)

        self.state.current_transform = "TestTransform"

        self._transforms: Dict[str, ImageTransform] = {
            "TestTransform": TestTransform(),
            "GaussianBlurTransform": GaussianBlurTransform(),
            "IdentityTransform": IdentityTransform(),
        }

        self.state.transforms = [k for k in self._transforms.keys()]
        self.state.current_transform = self.state.transforms[0]

        self.on_apply_transform = lambda: None

        self.server.controller.add("on_server_ready")(self.on_server_ready)

        self._ui = None

    def on_server_ready(self, *args, **kwargs):
        # Bind instance methods to state change
        self.on_current_transform_change()
        self.state.change("current_transform")(self.on_current_transform_change)

    def on_current_transform_change(self, **kwargs):
        transform = self._transforms[self.state.current_transform]
        self.state.params_values = transform.get_parameters()
        self.state.params_descriptions = transform.get_parameters_description()

    def on_transform_parameters_changed(self, parameters, **kwargs):
        transform = self._transforms[self.state.current_transform]
        transform.set_parameters(parameters)
        self.state.params_values = transform.get_parameters()

    def transform_select_ui(self):
        with html.Div(trame_server=self.server):
            quasar.QSelect(
                label="Transform",
                v_model=("current_transform",),
                options=(self.state.transforms,),
                filled=True,
                emit_value=True,
                map_options=True,
            )

    def transform_params_ui(self):
        with html.Div(trame_server=self.server):
            ParamsWidget(
                values=("params_values",),
                descriptions=("params_descriptions",),
                valuesChanged=(self.on_transform_parameters_changed, "[$event]"),
            )

    def transform_apply_ui(self):
        with html.Div(trame_server=self.server):
            quasar.QBtn(
                "Apply",
                click=(self.on_apply_transform,),
                classes="full-width",
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
                    self.transform_select_ui()

                    with html.Div(
                        classes="q-pa-md q-ma-md",
                        style="border-style: solid; border-width: thin; border-radius: 0.5rem; border-color: lightgray;",
                    ):
                        self.transform_params_ui()

                    self.transform_apply_ui()

                with quasar.QPageContainer():
                    with quasar.QPage():
                        with html.Div(classes="row", style="min-height: inherit;"):
                            with html.Div(classes="col q-pa-md"):
                                pass

        return self._ui


def main(server=None, *args, **kwargs):
    server = get_server()
    server.client_type = "vue3"

    app = ParametersApp(server)
    app.ui

    server.start(**kwargs)


if __name__ == "__main__":
    main()
