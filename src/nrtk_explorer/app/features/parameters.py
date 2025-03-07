from typing import Dict

from nrtk_explorer.app.applet import Applet

from trame.widgets import quasar, html
from trame.ui.quasar import QLayout

from trame.app import get_server

from nrtk_explorer.widgets.nrtk_explorer import TransformsWidget

from nrtk_explorer.library.transforms import (
    ImageTransform,
    GaussianBlurTransform,
    IdentityTransform,
    TestTransform,
)


class ParametersApp(Applet):
    def __init__(self, server):
        super().__init__(server)

        self.context.setdefault("transforms", [])
        self.state.setdefault("transforms", [])
        self.state.setdefault("transform_descriptions", {})

        self._transform_classes: Dict[str, type[ImageTransform]] = {
            "TestTransform": TestTransform,
            "GaussianBlurTransform": GaussianBlurTransform,
            "IdentityTransform": IdentityTransform,
        }

        self._default_transform = None

        self.server.controller.add("on_server_ready")(self.on_server_ready)

        self._ui = None

    def on_server_ready(self, *args, **kwargs):
        # Bind instance methods to state change
        self.update_transforms_descriptions()

    def on_add_transform(self, *args, **kwargs):
        if self._default_transform in self._transform_classes:
            transform_name, transform_class = (
                self._default_transform,
                self._transform_classes[self._default_transform],
            )
        else:
            transform_name, transform_class = next(iter(self._transform_classes.items()))

        self.context.transforms.append({"name": transform_name, "instance": transform_class()})

        self.update_transforms_values()

    def on_remove_transform(self, i, **kwargs):
        if i >= len(self.context.transforms):
            return

        self.context.transforms.pop(i)

        self.update_transforms_values()

    def on_type_changed(self, event):
        i = event["id"]
        transform_name = event["type"]
        transform_class = self._transform_classes.get(transform_name)

        if i >= len(self.context.transforms) or transform_class is None:
            return

        self.context.transforms[i] = {"name": transform_name, "instance": transform_class()}

        self.update_transforms_values()

    def on_params_changed(self, event):
        i = event["id"]
        params = event["params"]

        if i >= len(self.context.transforms):
            return

        transform: ImageTransform = self.context.transforms[i]["instance"]
        transform.set_parameters(params)

        self.update_transforms_values()

    def update_transforms_descriptions(self):
        transform_descriptions = {
            transform_name: transform_class.get_parameters_description()
            for transform_name, transform_class in self._transform_classes.items()
        }

        with self.state:
            self.state.transform_descriptions = transform_descriptions

    def update_transforms_values(self):
        def serialize_transform(item):
            name = item["name"]
            transform = item["instance"]
            return {"name": name, "parameters": transform.get_parameters()}

        state_transforms = list(map(serialize_transform, self.context.transforms))

        with self.state:
            self.state.transforms = state_transforms

    def transform_apply_ui(self):
        with html.Div(trame_server=self.server):
            quasar.QBtn(
                "Apply Transforms",
                click=(self.server.controller.apply_transform),
                classes="full-width",
                flat=True,
            )

    def transforms_ui(self):
        with html.Div(trame_server=self.server):
            TransformsWidget(
                values=("transforms",),
                descriptions=("transform_descriptions",),
                add_transform=(self.on_add_transform, "[$event]"),
                remove_transform=(self.on_remove_transform, "[$event]"),
                type_changed=(self.on_type_changed, "[$event]"),
                params_changed=(self.on_params_changed, "[$event]"),
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
                    width="500",
                ):
                    self.transforms_ui()

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
