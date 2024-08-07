import logging
from typing import Iterable
from pathlib import Path

from trame.widgets import html
from trame_server.utils.namespace import Translator
from nrtk_explorer.library import images_manager
from nrtk_explorer.library.filtering import FilterProtocol
from nrtk_explorer.library.dataset import get_dataset

from nrtk_explorer.app.embeddings import EmbeddingsApp
from nrtk_explorer.app.transforms import TransformsApp
from nrtk_explorer.app.filtering import FilteringApp
from nrtk_explorer.app.applet import Applet
from nrtk_explorer.app import ui
import nrtk_explorer.test_data

import os

import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

html.Template.slot_names.add("before")
html.Template.slot_names.add("after")

HORIZONTAL_SPLIT_DEFAULT_VALUE = 17
VERTICAL_SPLIT_DEFAULT_VALUE = 40

DIR_NAME = os.path.dirname(nrtk_explorer.test_data.__file__)
DEFAULT_DATASETS = [
    f"{DIR_NAME}/coco-od-2017/test_val2017.json",
]


# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


class Engine(Applet):
    def __init__(self, server=None):
        super().__init__(server)

        self.server.cli.add_argument(
            "--dataset",
            nargs="+",
            default=DEFAULT_DATASETS,
            help="Path of the json file describing the image dataset",
        )

        known_args, _ = self.server.cli.parse_known_args()
        self.input_paths = known_args.dataset
        self.state.current_dataset = str(Path(self.input_paths[0]).resolve())

        self.context["image_objects"] = {}
        self.context["images_manager"] = images_manager.ImagesManager()

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
        transforms_translator.add_translation(
            "feature_extraction_model", "current_transforms_model"
        )

        self._transforms_app = TransformsApp(
            server=self.server.create_child_server(translator=transforms_translator)
        )

        embeddings_translator = Translator()
        embeddings_translator.add_translation(
            "feature_extraction_model", "current_embeddings_model"
        )

        self._embeddings_app = EmbeddingsApp(
            server=self.server.create_child_server(translator=embeddings_translator),
        )

        filtering_translator = Translator()
        filtering_translator.add_translation("categories", "annotation_categories")
        self._filtering_app = FilteringApp(
            server=self.server.create_child_server(translator=filtering_translator),
        )

        self._embeddings_app.set_on_select(self._transforms_app.set_selected_dataset_ids)
        self._transforms_app.set_on_transform(self._embeddings_app.on_run_transformations)
        self._embeddings_app.set_on_hover(self._transforms_app.on_image_hovered)
        self._transforms_app.set_on_hover(self._embeddings_app.on_image_hovered)
        self._filtering_app.set_on_apply_filter(self.on_filter_apply)

        # Set state variable
        self.state.trame__title = "nrtk_explorer"

        # Bind instance methods to controller
        self.ctrl.on_server_reload = self._build_ui
        self.ctrl.add("on_server_ready")(self.on_server_ready)

        self.state.num_images_max = 0
        self.state.num_images_disabled = True
        self.state.random_sampling = False
        self.state.random_sampling_disabled = True
        self.state.images_id = []

        self._build_ui()

    def on_server_ready(self, *args, **kwargs):
        # Bind instance methods to state change
        self.state.change("current_dataset")(self.on_dataset_change)
        self.state.change("num_images")(self.on_num_images_change)
        self.state.change("random_sampling")(self.on_random_sampling_change)

        self.on_dataset_change()

    def on_dataset_change(self, **kwargs):
        # Reset cache
        self.context.images_manager = images_manager.ImagesManager()
        self.context.dataset = get_dataset(self.state.current_dataset, force_reload=True)
        self.state.num_images_max = len(self.context.dataset.imgs)
        self.state.random_sampling_disabled = False
        self.state.num_images_disabled = False

        self.reload_images()

    def on_filter_apply(self, filter: FilterProtocol[Iterable[int]], **kwargs):
        selected_indices = []
        for index, image_id in enumerate(self.state.images_ids):
            image_annotations_categories = [
                annotation["category_id"]
                for annotation in self.context.dataset.anns.values()
                if annotation["image_id"] == image_id
            ]
            include = filter.evaluate(image_annotations_categories)
            if include:
                selected_indices.append(index)

        self._embeddings_app.on_select(selected_indices)

    def on_num_images_change(self, **kwargs):
        self.reload_images()

    def on_random_sampling_change(self, **kwargs):
        self.reload_images()

    def reload_images(self):
        categories = {}
        for category in self.context.dataset.cats.values():
            categories[category["id"]] = category

        images = list(self.context.dataset.imgs.values())

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

    def _build_ui(self):
        extra_args = {}
        if self.server.hot_reload:
            ui.reload(ui)
            extra_args["reload"] = self._build_ui

        self.ui = ui.build_layout(
            server=self.server,
            dataset_paths=self.input_paths,
            embeddings_app=self._embeddings_app,
            filtering_app=self._filtering_app,
            transforms_app=self._transforms_app,
            **extra_args,
        )
