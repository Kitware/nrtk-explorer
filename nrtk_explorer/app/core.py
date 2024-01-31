r"""
Define your classes and create the instances that you need to expose
"""

import logging
from trame.app import get_server
from trame.ui.quasar import QLayout
from trame.widgets import quasar
from trame.widgets import html
from trame_server.utils.namespace import Translator
from nrtk_explorer.library import images_manager

from nrtk_explorer.app.embeddings import EmbeddingsApp
from nrtk_explorer.app.transforms import TransformsApp
from nrtk_explorer.app.applet import Applet

import os

import json
import random


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def image_id_to_meta(image_id):
    return f"{image_id}_meta"


def image_id_to_result(image_id):
    return f"{image_id}_result"


DIR_NAME = os.path.dirname(__file__)
DATASET_DIRS = [
    f"{DIR_NAME}/../../assets/OIRDS_v1_0/oirds.json",
    f"{DIR_NAME}/../../assets/OIRDS_v1_0/oirds_test.json",
    f"{DIR_NAME}/../../assets/OIRDS_v1_0/oirds_train.json",
]

# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


class Engine(Applet):
    def __init__(self, server=None):
        if server is None:
            server = get_server()

        super().__init__(server)

        self.context["image_objects"] = {}
        self.context["images_manager"] = images_manager.ImagesManager()
        self.context["annotations"] = {}

        self._ui = None

        transforms_translator = Translator()
        transforms_translator.add_translation("current_model", "current_transforms_model")

        self._transforms_app = TransformsApp(
            server=self.server.create_child_server(translator=transforms_translator)
        )

        embeddings_translator = Translator()
        embeddings_translator.add_translation("current_model", "current_embeddings_model")

        self._embeddings_app = EmbeddingsApp(
            server=self.server.create_child_server(translator=embeddings_translator),
        )

        self._embeddings_app.set_on_select(self._transforms_app.on_selected_images_change)
        self._transforms_app.set_on_transform(self._embeddings_app.on_run_transformations)
        self._embeddings_app.set_on_hover(self._transforms_app.on_image_selected)
        self._transforms_app.set_on_hover(self._embeddings_app.on_image_selected)

        # Set state variable
        self.state.trame__title = "nrtk_explorer"

        self.state.current_dataset = DATASET_DIRS[0]

        # Bind instance methods to controller
        self.ctrl.on_server_reload = self.ui
        self.ctrl.add("on_server_ready")(self.on_server_ready)

        self.state.num_images_max = 0
        self.state.num_images_disabled = True
        self.state.random_sampling = False
        self.state.random_sampling_disabled = True
        self.state.images_id = []

        # Generate UI
        self.ui()
        self.context.images_manager = images_manager.ImagesManager()

    def on_server_ready(self, *args, **kwargs):
        # Bind instance methods to state change
        self.state.change("current_dataset")(self.on_dataset_change)
        self.state.change("num_images")(self.on_num_images_change)
        self.state.change("random_sampling")(self.on_random_sampling_change)

        self.on_dataset_change()

    def on_dataset_change(self, **kwargs):
        # Reset cache
        self.context.images_manager = images_manager.ImagesManager()

        with open(self.state.current_dataset) as f:
            dataset = json.load(f)

        self.state.num_images_max = len(dataset["images"])
        self.state.random_sampling_disabled = False
        self.state.num_images_disabled = False

        self.reload_images()

    def on_num_images_change(self, **kwargs):
        self.reload_images()

    def on_random_sampling_change(self, **kwargs):
        self.reload_images()

    def reload_images(self):
        with open(self.state.current_dataset) as f:
            dataset = json.load(f)

        categories = {}
        for category in dataset["categories"]:
            categories[category["id"]] = category

        images = dataset["images"]

        selected_images = []
        if self.state.num_images:
            if self.state.random_sampling:
                selected_images = random.sample(images, self.state.num_images)
            else:
                selected_images = images[: self.state.num_images]
        else:
            selected_images = images

        paths = list()
        for image in selected_images:
            paths.append(
                os.path.join(
                    os.path.dirname(self.state.current_dataset),
                    image["file_name"],
                )
            )

        self.context.paths = paths
        self.state.annotation_categories = categories
        self.state.images_ids = [img["id"] for img in selected_images]

    def ui(self, *args, **kwargs):
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
                        quasar.QToolbarTitle("NRTK_EXPLORER")

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
                                            options=(DATASET_DIRS,),
                                            filled=True,
                                            emit_value=True,
                                            map_options=True,
                                        )

                                        quasar.QSeparator(inset=True)
                                        quasar.QSeparator(inset=True)
                                        html.P("Number of images:", classes="text-body2")
                                        quasar.QSlider(
                                            v_model=("num_images", 15),
                                            min=(0,),
                                            max=("num_images_max", 25),
                                            disable=("num_images_disabled", True),
                                            step=(1,),
                                            label=True,
                                            label_always=True,
                                        )
                                        quasar.QToggle(
                                            v_model=("random_sampling", False),
                                            label="Random selection",
                                            left_label=True,
                                        )
                                self._embeddings_app.settings_widget()
                                self._transforms_app.settings_widget()

                            with html.Div(classes="col-5 q-pa-md"):
                                html.H5("Original Dataset", classes="text-h5")
                                with html.Div(
                                    classes="row", style="min-height: inherit; height: 30rem"
                                ):
                                    with html.Div(classes="col q-pa-md"):
                                        self._embeddings_app.visualization_widget()

                                with html.Div(classes="row"):
                                    with html.Div(classes="col q-pa-md"):
                                        self._transforms_app.original_dataset_widget()

                            with html.Div(
                                classes="col-5 q-pa-md",
                                style="background-color: #ffcdcd;",
                            ):
                                html.H5("Transformed Dataset", classes="text-h5")
                                with html.Div(
                                    classes="row", style="min-height: inherit; height: 30rem"
                                ):
                                    with html.Div(classes="col q-pa-md"):
                                        self._embeddings_app.visualization_widget_transformation()

                                with html.Div(classes="row"):
                                    with html.Div(classes="col q-pa-md"):
                                        self._transforms_app.transformed_dataset_widget()

            self._ui = layout

        return self._ui


def create_engine(server=None):
    # Get or create server
    if server is None:
        server = get_server()

    if isinstance(server, str):
        server = get_server(server)

    server.client_type = "vue3"

    return Engine(server)
