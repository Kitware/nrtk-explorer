r"""
Define your classes and create the instances that you need to expose
"""

import logging
from typing import Iterable
from trame.app import get_server
from trame.ui.quasar import QLayout
from trame.widgets import quasar
from trame.widgets import html
from trame_server.utils.namespace import Translator
from nrtk_explorer.library import images_manager
from nrtk_explorer.library.filtering import FilterProtocol

from nrtk_explorer.app.embeddings import EmbeddingsApp
from nrtk_explorer.app.transforms import TransformsApp
from nrtk_explorer.app.filtering import FilteringApp
from nrtk_explorer.app.applet import Applet
from pathlib import Path

import os

import json
import random


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def image_id_to_meta(image_id):
    return f"{image_id}_meta"


def image_id_to_result(image_id):
    return f"{image_id}_result"


def parse_dataset_dirs(datasets):
    return [{"label": Path(ds).name, "value": ds} for ds in datasets]


# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


class Engine(Applet):
    def __init__(self, server=None):
        if server is None:
            server = get_server()

        super().__init__(server)

        self.server.cli.add_argument(
            "--dataset",
            nargs="+",
            default=[f"{os.path.dirname(__file__)}/../../assets/OIRDS_v1_0/oirds.json"],
            help="Path of the json file describing the image dataset",
        )
        self.input_paths = self.server.cli.parse_args().dataset
        self.state.current_dataset = self.input_paths[0]

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

        filtering_translator = Translator()
        filtering_translator.add_translation("categories", "annotation_categories")
        self._filtering_app = FilteringApp(
            server=self.server.create_child_server(translator=filtering_translator),
        )

        self._embeddings_app.set_on_select(self._transforms_app.on_selected_images_change)
        self._transforms_app.set_on_transform(self._embeddings_app.on_run_transformations)
        self._embeddings_app.set_on_hover(self._transforms_app.on_image_hovered)
        self._transforms_app.set_on_hover(self._embeddings_app.on_image_hovered)
        self._filtering_app.set_on_apply_filter(self.on_filter_apply)

        # Set state variable
        self.state.trame__title = "nrtk_explorer"

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

    def on_filter_apply(self, filter: FilterProtocol[Iterable[int]], **kwargs):
        selected_indices = []

        for index, image_id in enumerate(self.state.images_ids):
            image_annotations_categories = map(
                lambda annotation: annotation["category_id"],
                self.context["annotations"].get(f"img_{image_id}", []),
            )

            include = filter.evaluate(image_annotations_categories)

            if include:
                selected_indices.append(index)

        self._embeddings_app.on_select(selected_indices)

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
                                html.P("Dataset Selection", classes="text-h6")

                                quasar.QSelect(
                                    label="Dataset",
                                    v_model=("current_dataset",),
                                    options=(parse_dataset_dirs(self.input_paths),),
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
                                )
                                html.P(
                                    "{{num_images}}/{{num_images_max}} images",
                                    classes="text-caption text-center",
                                )

                                quasar.QToggle(
                                    v_model=("random_sampling", False),
                                    dense=False,
                                    label="Random selection",
                                )

                                quasar.QSeparator(inset=True, spaced=True)

                                html.P("Embeddings", classes="text-h6")

                                self._embeddings_app.settings_widget()

                                quasar.QSeparator(inset=True, spaced=True)

                                self._filtering_app.filter_ui()
                                self._filtering_app.filter_apply_ui()

                                quasar.QSeparator(inset=True, spaced=True)

                                html.P("Transform Settings", classes="text-h6")

                                self._transforms_app.settings_widget()

                            with html.Div(classes="col-10 q-pa-md"):
                                with html.Div(
                                    classes="row", style="min-height: inherit; height: 40rem"
                                ):
                                    self._embeddings_app.visualization_widget()

                                with html.Div(classes="row"):
                                    with html.Div(classes="col-6 q-pa-md"):
                                        html.H5("Original Dataset", classes="text-h5")

                                        with html.Div(classes="row"):
                                            with html.Div(classes="col q-pa-md"):
                                                self._transforms_app.original_dataset_widget()

                                    with html.Div(
                                        classes="col-6 q-pa-md",
                                        style="background-color: #ffcdcd;",
                                    ):
                                        html.H5("Transformed Dataset", classes="text-h5")

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
