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
from nrtk_explorer.app.ui.collapsible_card import collapsible_card
import nrtk_explorer.test_data
from pathlib import Path

import os

import json
import random


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

html.Template.slot_names.add("before")
html.Template.slot_names.add("after")

HORIZONTAL_SPLIT_DEFAULT_VALUE = 17
VERTICAL_SPLIT_DEFAULT_VALUE = 40

DIR_NAME = os.path.dirname(nrtk_explorer.test_data.__file__)
DEFAULT_DATASETS = [
    f"{DIR_NAME}/OIRDS_v1_0/oirds.json",
    f"{DIR_NAME}/OIRDS_v1_0/oirds_test.json",
    f"{DIR_NAME}/OIRDS_v1_0/oirds_train.json",
]


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
            default=DEFAULT_DATASETS,
            help="Path of the json file describing the image dataset",
        )

        known_args, _ = self.server.cli.parse_known_args()
        self.input_paths = known_args.dataset
        self.state.current_dataset = self.input_paths[0]

        self.context["image_objects"] = {}
        self.context["images_manager"] = images_manager.ImagesManager()
        self.context["annotations"] = {}

        self._ui = None

        self.state.collapse_dataset = False
        self.state.collapse_embeddings = False
        self.state.collapse_filter = False
        self.state.collapse_transforms = False
        self.state.client_only(
            "collapse_dataset", "collapse_embeddings", "collapse_filter", "collapse_transforms"
        )

        self.state.horizontal_split = HORIZONTAL_SPLIT_DEFAULT_VALUE
        self.state.vertical_split = VERTICAL_SPLIT_DEFAULT_VALUE
        self.state.client_only("horizontal_split", "vertical_split")

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
                        quasar.QToolbarTitle("NRTK_EXPLORER")

                # # Main content
                with quasar.QPageContainer():
                    with quasar.QPage():
                        with quasar.QSplitter(
                            model_value=("horizontal_split",),
                            classes="inherit-height",
                            before_class="inherit-height zero-height scroll",
                            after_class="inherit-height zero-height",
                        ):
                            with html.Template(v_slot_before=True):
                                with html.Div(classes="q-pa-md q-gutter-md"):
                                    (
                                        dataset_title_slot,
                                        dataset_content_slot,
                                        dataset_actions_slot,
                                    ) = collapsible_card("collapse_dataset")

                                    with dataset_title_slot:
                                        html.Span("Dataset Selection", classes="text-h6")

                                    with dataset_content_slot:
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

                                    (
                                        embeddings_title_slot,
                                        embeddings_content_slot,
                                        embeddings_actions_slot,
                                    ) = collapsible_card("collapse_embeddings")

                                    with embeddings_title_slot:
                                        html.Span("Embeddings", classes="text-h6")

                                    with embeddings_content_slot:
                                        self._embeddings_app.settings_widget()

                                    with embeddings_actions_slot:
                                        self._embeddings_app.compute_ui()

                                    filter_title_slot, filter_content_slot, filter_actions_slot = (
                                        collapsible_card("collapse_filter")
                                    )

                                    with filter_title_slot:
                                        html.Span("Category Filter", classes="text-h6")

                                    with filter_content_slot:
                                        self._filtering_app.filter_operator_ui()
                                        self._filtering_app.filter_options_ui()

                                    with filter_actions_slot:
                                        self._filtering_app.filter_apply_ui()

                                    (
                                        transforms_title_slot,
                                        transforms_content_slot,
                                        transforms_actions_slot,
                                    ) = collapsible_card("collapse_transforms")

                                    with transforms_title_slot:
                                        html.Span("Transform Settings", classes="text-h6")

                                    with transforms_content_slot:
                                        self._transforms_app.settings_widget()

                                    with transforms_actions_slot:
                                        self._transforms_app.apply_ui()

                            with html.Template(v_slot_after=True):
                                with quasar.QSplitter(
                                    v_model=("vertical_split",),
                                    horizontal=True,
                                    classes="inherit-height zero-height",
                                    before_class="q-pa-md",
                                    after_class="q-pa-md",
                                ):
                                    with html.Template(v_slot_before=True):
                                        self._embeddings_app.visualization_widget()

                                    with html.Template(v_slot_after=True):
                                        with html.Div(classes="row q-col-gutter-md"):
                                            with html.Div(classes="col-6"):
                                                with quasar.QCard(flat=True, bordered=True):
                                                    with quasar.QCardSection():
                                                        html.Span(
                                                            "Original Dataset", classes="text-h5"
                                                        )

                                                    with quasar.QCardSection():
                                                        self._transforms_app.original_dataset_widget()

                                            with html.Div(classes="col-6"):
                                                with quasar.QCard(
                                                    flat=True,
                                                    bordered=True,
                                                    style="background-color: #ffcdd2;",
                                                ):
                                                    with quasar.QCardSection():
                                                        html.Span(
                                                            "Transformed Dataset",
                                                            classes="text-h5",
                                                        )

                                                    with quasar.QCardSection():
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
