import logging
from typing import Iterable

from pathlib import Path

from trame_server.utils.namespace import Translator
from nrtk_explorer.library.filtering import FilterProtocol
from nrtk_explorer.library.dataset import (
    get_dataset,
    expand_hugging_face_datasets,
    discover_datasets,
    dataset_select_options,
)
from nrtk_explorer.library.debounce import debounce
from nrtk_explorer.library.app_config import process_config


from nrtk_explorer.app.features import (
    EnabledFeatures,
    DEFAULT_FEATURES,
    validate_feature_name,
    validate_preset_name,
    config_features_to_enabled_features,
    config_preset_to_enabled_features,
)
from nrtk_explorer.app.images.images import Images
from nrtk_explorer.app.images.image_server import ImageServer
from nrtk_explorer.app.applet import Applet
from nrtk_explorer.app import ui
import nrtk_explorer.test_data

import os

import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DIR_NAME = os.path.dirname(nrtk_explorer.test_data.__file__)
DEFAULT_DATASETS = [
    f"{DIR_NAME}/coco-od-2017/test_val2017.json",
]
NUM_IMAGES_DEFAULT = os.environ.get("NRTK_EXPLORER_NUM_IMAGES", 500)
NUM_IMAGES_DEBOUNCE_TIME = 0.3  # seconds


def dir_path(arg):
    path = Path(arg).resolve()
    if path.is_dir():
        return path
    else:
        raise NotADirectoryError(arg)


# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------

config_options = {
    "dataset": {
        "flags": ["--dataset"],
        "params": {
            "nargs": "+",
            "default": DEFAULT_DATASETS,
            "help": "Path to the JSON file describing the image dataset",
        },
    },
    "download": {
        "flags": ["--download"],
        "params": {
            "action": "store_true",
            "default": False,
            "help": "Download Hugging Face Hub datasets instead of streaming them",
        },
    },
    "repository": {
        "flags": ["--repository"],
        "params": {
            "default": None,
            "required": False,
            "type": dir_path,
            "help": "Path to the directory where exported datasets will be saved to",
        },
    },
    "features": {
        "flags": ["--features"],
        "params": {
            "nargs": "+",
            "default": None,
            "required": False,
            "type": validate_feature_name,
            "help": "Space separated list of app features to enable.",
        },
    },
    "preset": {
        "flags": ["--preset"],
        "params": {
            "default": None,
            "required": False,
            "type": validate_preset_name,
            "help": "Choose which application features to enable based on a preset name.",
        },
    },
    "session_id": {
        "flags": ["--session-id"],
        "params": {
            "default": "",
            "required": False,
            "help": "Session ID for deploying to a remote server using Docker",
        },
    },
}


class Engine(Applet):
    def __init__(self, server=None, **kwargs):
        super().__init__(server)

        config = process_config(self.server.cli, config_options, **kwargs)

        self.state.input_datasets = expand_hugging_face_datasets(
            config["dataset"], not config["download"]
        )

        self.context.repository = config["repository"]
        self.context.session = config["session_id"]
        self.state.repository_datasets = [
            str(path) for path in discover_datasets(self.context.repository)
        ]

        if config["preset"] is not None:
            self.ctx.enabled_features = config_preset_to_enabled_features(config["preset"])
        else:
            self.ctx.enabled_features = config_features_to_enabled_features(config["features"])

        self.ctx.enabled_features

        self.state.all_datasets = self.state.input_datasets + self.state.repository_datasets
        self.state.all_datasets_options = dataset_select_options(self.state.all_datasets)
        self.state.current_dataset = self.state.all_datasets[0]

        images = Images(server=self.server)
        self._image_server = ImageServer(server=self.server, images=images)

        self._datasets_app = None
        if self.datasets_enabled:
            from nrtk_explorer.app.features.datasets import DatasetsApp

            self._datasets_app = DatasetsApp(server=self.server.create_child_server(), **kwargs)
        else:
            # If datasets selection is disabled, we don't have a way to tweak the sampling
            # the images in a dataset. Hence include all images
            global NUM_IMAGES_DEFAULT
            NUM_IMAGES_DEFAULT = float("inf")

        self._transforms_app = None
        self.state.transform_enabled = False
        if self.transforms_enabled:
            from nrtk_explorer.app.features.transforms import TransformsApp

            self._transforms_app = TransformsApp(
                server=self.server.create_child_server(), images=images, **kwargs
            )

        self._images_app = None
        if self.images_enabled:
            from nrtk_explorer.app.features.images import ImagesApp

            self._images_app = ImagesApp(
                server=self.server.create_child_server(), images=images, **kwargs
            )

        self._inference_app = None
        if self.inference_enabled:
            from nrtk_explorer.app.features.inference import InferenceApp

            self._inference_app = InferenceApp(server=self.server.create_child_server(), **kwargs)

        self._embeddings_app = None
        if self.embeddings_enabled:
            from nrtk_explorer.app.features.embeddings import EmbeddingsApp

            self._embeddings_app = EmbeddingsApp(
                server=self.server.create_child_server(),
                images=images,
            )

        self._filtering_app = None
        if self.filtering_enabled:
            from nrtk_explorer.app.features.filtering import FilteringApp

            filtering_translator = Translator()
            filtering_translator.add_translation("categories", "annotation_categories")
            self._filtering_app = FilteringApp(
                server=self.server.create_child_server(translator=filtering_translator),
            )
            self.ctrl.apply_filter.add(self.on_filter_apply)

        self._export_app = None
        if self.export_enabled and self.context.repository is not None:
            from nrtk_explorer.app.features.export import ExportApp

            self._export_app = ExportApp(
                server=self.server.create_child_server(),
            )

        # Bind instance methods to controller
        self.ctrl.on_server_reload = self._build_ui
        self.ctrl.add("on_server_ready")(self.on_server_ready)

        self.state.num_images = NUM_IMAGES_DEFAULT
        self.state.num_images_max = 0
        self.state.num_images_disabled = True
        self.state.random_sampling = False
        self.state.random_sampling_disabled = True
        self.state.dataset_ids = []
        self.state.hovered_id = None
        self.state.maximised_id = None

        def clear_hovered(**kwargs):
            self.state.hovered_id = None

        self.state.change("dataset_ids")(clear_hovered)

        self._build_ui()

    def on_server_ready(self, *args, **kwargs):
        # Bind instance methods to state change
        self.state.change("current_dataset")(self.on_dataset_change)
        self.state.change("num_images")(
            debounce(NUM_IMAGES_DEBOUNCE_TIME, self.state)(self.resample_images)
        )
        self.state.change("random_sampling")(self.resample_images)

        self.on_dataset_change()

        # Capture errors emitted by wslink and display them in the UI
        self.server.protocol.log_emitter.add_event_listener("error", self.handle_errors)
        self.server.protocol.log_emitter.add_event_listener("exception", self.handle_exceptions)

    def handle_errors(self, message):
        self.ctrl.create_error_alert(
            text=message,
            persistent=True,
        )

    def handle_exceptions(self, e: Exception):
        e_str = str(e)
        self.ctrl.create_error_alert(
            title="An uncaught exception occurred",
            text=f"Exception type: {e.__class__.__name__}\n{e_str}",
            persistent=True,
        )

    @property
    def enabled_features(self) -> EnabledFeatures:
        enabled_features = self.ctx.enabled_features
        if enabled_features is None:
            return DEFAULT_FEATURES
        else:
            return enabled_features

    @property
    def datasets_enabled(self) -> bool:
        return self.enabled_features.get("datasets", DEFAULT_FEATURES["datasets"])

    @property
    def images_enabled(self) -> bool:
        return self.enabled_features.get("images", DEFAULT_FEATURES["images"])

    @property
    def embeddings_enabled(self) -> bool:
        return self.enabled_features.get("embeddings", DEFAULT_FEATURES["embeddings"])

    @property
    def transforms_enabled(self) -> bool:
        return self.enabled_features.get("transforms", DEFAULT_FEATURES["transforms"])

    @property
    def filtering_enabled(self) -> bool:
        return self.enabled_features.get("filtering", DEFAULT_FEATURES["filtering"])

    @property
    def export_enabled(self) -> bool:
        return self.enabled_features.get("export", DEFAULT_FEATURES["export"])

    @property
    def inference_enabled(self) -> bool:
        return self.enabled_features.get("inference", DEFAULT_FEATURES["inference"])

    def on_dataset_change(self, **kwargs):
        with self.state:
            self.state.dataset_ids = []  # sampled images
            self.state.user_selected_ids = (
                []
            )  # ensure image update in transforms app via image list
            self.context.dataset = get_dataset(self.state.current_dataset)
            self.state.num_images_max = len(self.context.dataset.imgs)
            self.state.num_images = min(self.state.num_images_max, self.state.num_images)
            self.state.dirty("num_images")  # Trigger resample_images()
            self.state.random_sampling_disabled = False
            self.state.num_images_disabled = False

            self.state.annotation_categories = {
                category["id"]: category for category in self.context.dataset.cats.values()
            }

    def on_filter_apply(self, filter: FilterProtocol[Iterable[int]], **kwargs):
        selected_ids = []
        for dataset_id in self.state.dataset_ids:
            image_annotations_categories = [
                annotation["category_id"]
                for annotation in self.context.dataset.anns.values()
                if annotation["image_id"] == int(dataset_id)
            ]
            include = filter.evaluate(image_annotations_categories)
            if include:
                selected_ids.append(dataset_id)

        self.state.user_selected_ids = selected_ids

    def resample_images(self, **kwargs):
        ids = [image["id"] for image in self.context.dataset.imgs.values()]

        selected_images = []
        if self.state.num_images:
            if self.state.random_sampling:
                selected_images = random.sample(ids, min(len(ids), self.state.num_images))
            else:
                selected_images = ids[: self.state.num_images]
        else:
            selected_images = ids

        self.context.dataset_ids = selected_images
        self.state.dataset_ids = [str(id) for id in self.context.dataset_ids]
        self.state.user_selected_ids = self.state.dataset_ids

    def _build_ui(self):
        extra_args = {}
        if self.server.hot_reload:
            ui.reload(ui)
            extra_args["reload"] = self._build_ui

        self.ui = ui.NrtkExplorerLayout(
            server=self.server,
            datasets_app=self._datasets_app,
            images_app=self._images_app,
            embeddings_app=self._embeddings_app,
            filtering_app=self._filtering_app,
            inference_app=self._inference_app,
            transforms_app=self._transforms_app,
            export_app=self._export_app,
            **extra_args,
        )
