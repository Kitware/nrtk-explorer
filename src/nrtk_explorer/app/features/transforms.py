from typing import Dict

from trame.ui.quasar import QLayout
from trame.widgets import quasar
from trame.widgets import html
from trame.app import get_server

import nrtk_explorer.library.transforms as trans
import nrtk_explorer.library.yaml_transforms as nrtk_yaml
import nrtk_explorer.library.serialization_helpers as serialization_helpers

from nrtk_explorer.app.applet import Applet
from nrtk_explorer.app.trame_utils import ProcessingStep
from nrtk_explorer.app.features.parameters import ParametersApp
from nrtk_explorer.app.images.images import Images

from nrtk_explorer.app.ui.image_list import (
    TRANSFORM_COLUMNS,
    init_always_visible_columns,
    add_visible_columns,
)


class TransformsApp(Applet):
    def __init__(
        self,
        server,
        images=None,
        **kwargs,
    ):
        super().__init__(server)

        self.images = images or Images(server)

        self._parameters_app = ParametersApp(
            server=server,
        )

        self._ui = None

        self._transform_classes: Dict[str, type[trans.ImageTransform]] = {
            "blur": trans.GaussianBlurTransform,
            "invert": trans.InvertTransform,
            "downsample": trans.DownSampleTransform,
            "identity": trans.IdentityTransform,
        }

        # Add transform from YAML definition
        self._transform_classes.update(nrtk_yaml.generate_transforms())

        self._parameters_app._transform_classes = self._transform_classes

        # Initialize the transforms pipeline to the identity
        self._parameters_app._default_transform = "blur"
        self._parameters_app.on_add_transform()

        init_always_visible_columns(self.state)
        add_visible_columns(self.state, TRANSFORM_COLUMNS)

        self.transform_enable_control = ProcessingStep(
            server,
            feature_enabled_state_key="transform_enabled",
            gui_switch_key="transform_enabled_switch",
            column_name=TRANSFORM_COLUMNS[0],
            enabled_callback=self.on_apply_transform,
        )

        self.server.controller.apply_transform.add(self.on_apply_transform)
        self.server.controller.on_server_ready.add(self.on_server_ready)

    def on_server_ready(self, *args, **kwargs):
        pass

    def on_apply_transform(self, **kwargs):
        # Turn on switch if user clicked lower apply button
        self.state.transform_enabled_switch = True
        transforms = list(map(lambda t: t["instance"], self.context.transforms))

        for transform in transforms:
            params = transform.get_parameters()
            for key, value in transform.get_parameters_description().items():
                if "deserialize_func" in value.keys():
                    params[key] = getattr(serialization_helpers, value["deserialize_func"])(
                        params[key]
                    )
            transform.set_parameters(params)

        chained_transform = trans.ChainedImageTransform(transforms)
        self.images.set_transform(chained_transform)
        if self.ctrl.run_transform.exists():
            self.ctrl.run_transform()

    def settings_widget(self):
        with html.Div(classes="col"):
            self._parameters_app.transforms_ui()

    def apply_ui(self):
        with html.Div():
            self._parameters_app.transform_apply_ui()

    # This is only used within when this module (file) is executed as an Standalone app.
    @property
    def ui(self):
        if self._ui is None:
            with QLayout(
                self.server, view="lhh LpR lff", classes="shadow-2 rounded-borders bg-grey-2"
            ) as layout:
                # # Toolbar
                with quasar.QHeader():
                    with quasar.QToolbar(classes="shadow-4"):
                        quasar.QBtn(
                            flat=True,
                            click="drawerLeft = !drawerLeft",
                            round=True,
                            dense=False,
                            icon="menu",
                        )
                        quasar.QToolbarTitle("Transforms")

                # # Main content
                with quasar.QPageContainer():
                    with quasar.QPage():
                        with html.Div(classes="row"):
                            with html.Div(classes="col-2 q-pa-md"):
                                with html.Div(
                                    classes="column justify-center", style="padding:1rem"
                                ):
                                    with html.Div(classes="col"):
                                        quasar.QSelect(
                                            label="Dataset",
                                            v_model=("current_dataset",),
                                            options=([],),
                                            filled=True,
                                            emit_value=True,
                                            map_options=True,
                                        )

                                        html.P("Number of elements:", classes="text-body2")
                                        quasar.QSlider(
                                            v_model=("current_num_elements",),
                                            min=(0,),
                                            max=(25,),
                                            step=(1,),
                                            label=True,
                                            label_always=True,
                                        )
                                self.settings_widget()
                                self.apply_ui()

                self._ui = layout
        return self._ui


def main(server=None, *args, **kwargs):
    server = get_server(client_type="vue3")

    transforms_app = TransformsApp(server)
    transforms_app.ui

    server.start(**kwargs)


if __name__ == "__main__":
    main()
