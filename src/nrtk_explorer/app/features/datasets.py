import logging

from trame.widgets import quasar
from trame.widgets import html
from trame.app import get_server

from nrtk_explorer.app.applet import Applet

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DatasetsApp(Applet):
    def __init__(
        self,
        server,
        **kwargs,
    ):
        super().__init__(server)

        self._ui = None

        self.server.controller.on_server_ready.add(self.on_server_ready)

    def on_server_ready(self, *args, **kwargs):
        pass

    def settings_widget(self):
        quasar.QSelect(
            label="Dataset",
            v_model=("current_dataset",),
            options=("all_datasets_options",),
            filled=True,
            emit_value=True,
            map_options=True,
            dense=True,
        )
        quasar.QSlider(
            v_model=("num_images", 15),
            min=(0,),
            max=("num_images_max", 25),
            disable=("num_images_disabled", True),
            step=(1,),
            classes="q-pt-sm",
        )
        html.P(
            "{{num_images}}/{{num_images_max}} images",
            classes="text-center",
        )
        quasar.QToggle(
            v_model=("random_sampling", False),
            dense=False,
            label="Random sampling",
        )

    # This is only used within when this module (file) is executed as an Standalone app.
    @property
    def ui(self):
        pass


def main(server=None, *args, **kwargs):
    server = get_server(client_type="vue3")

    datasets_app = DatasetsApp(server)
    datasets_app.ui

    server.start(**kwargs)


if __name__ == "__main__":
    main()
