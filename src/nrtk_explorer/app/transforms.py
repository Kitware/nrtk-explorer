r"""
Define your classes and create the instances that you need to expose
"""

import logging
from typing import Dict

from trame.ui.quasar import QLayout
from trame.widgets import quasar
from trame.widgets import html
from trame.app import get_server

import nrtk_explorer.library.transforms as trans
import nrtk_explorer.library.nrtk_transforms as nrtk_trans
from nrtk_explorer.library import images_manager, object_detector
from nrtk_explorer.app import ui
from nrtk_explorer.app.applet import Applet
from nrtk_explorer.app.parameters import ParametersApp
from nrtk_explorer.library.ml_models import (
    ClassificationResNet50,
    ClassificationAlexNet,
    ClassificationVgg16,
)
import nrtk_explorer.test_data

import json
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def image_id_to_meta(image_id):
    return f"{image_id}_meta"


def image_id_to_result(image_id):
    return f"{image_id}_result"


DIR_NAME = os.path.dirname(nrtk_explorer.test_data.__file__)
DATASET_DIRS = [
    f"{DIR_NAME}/OIRDS_v1_0/oirds.json",
    f"{DIR_NAME}/OIRDS_v1_0/oirds_test.json",
    f"{DIR_NAME}/OIRDS_v1_0/oirds_train.json",
]


class TransformsApp(Applet):
    def __init__(self, server):
        super().__init__(server)

        self._parameters_app = ParametersApp(
            server=server,
        )

        self._parameters_app.on_apply_transform = self.on_apply_transform

        self._ui = None

        self.is_standalone_app = self.server.state.parent is None
        if self.is_standalone_app:
            self.context.images_manager = images_manager.ImagesManager()

        if self.context["image_objects"] is None:
            self.context["image_objects"] = {}

        self.models = {
            "ClassificationResNet50": ClassificationResNet50(server),
            "ClassificationAlexNet": ClassificationAlexNet(server),
            "ClassificationVgg16": ClassificationVgg16(server),
        }

        self._on_transform_fn = None
        self.state.models = [k for k in self.models.keys()]
        self.state.feature_extraction_model = self.state.models[0]

        self._transforms: Dict[str, trans.ImageTransform] = {
            "identity": trans.IdentityTransform(),
            "blur": trans.GaussianBlurTransform(),
            "invert": trans.InvertTransform(),
            "downsample": trans.DownSampleTransform(),
            "nrtk_blur": nrtk_trans.NrtkGaussianBlurTransform(),
            "nrtk_pybsm": nrtk_trans.NrtkPybsmTransform(),
        }

        self._parameters_app._transforms = self._transforms

        self.state.annotation_categories = {}

        self.state.source_image_ids = []
        self.state.transformed_image_ids = []
        self.state.transforms = [k for k in self._transforms.keys()]
        self.state.current_transform = self.state.transforms[0]

        if self.state.current_dataset is None:
            self.state.current_dataset = DATASET_DIRS[0]

        self.state.current_num_elements = 15

        self.server.controller.add("on_server_ready")(self.on_server_ready)
        self._on_hover_fn = None
        self.detector = object_detector.ObjectDetector(model_name="hustvl/yolos-tiny")

    def on_server_ready(self, *args, **kwargs):
        # Bind instance methods to state change
        self.state.change("feature_extraction_model")(self.on_feature_extraction_model_change)
        self.state.change("current_dataset")(self.on_current_dataset_change)
        self.state.change("current_num_elements")(self.on_current_num_elements_change)

        self.on_current_dataset_change(self.state.current_dataset)

    def set_on_transform(self, fn):
        self._on_transform_fn = fn

    def on_transform(self, *args, **kwargs):
        if self._on_transform_fn:
            self._on_transform_fn(*args, **kwargs)

    def on_apply_transform(self, *args, **kwargs):
        logger.debug("on_apply_transform")

        current_transform = self.state.current_transform
        transformed_image_ids = []
        transform = self._transforms[current_transform]
        for image_id in self.state.source_image_ids:
            image = self.context["image_objects"][image_id]

            transformed_image_id = f"transformed_{image_id}"
            meta_id = image_id_to_meta(image_id)
            transformed_meta_id = image_id_to_meta(transformed_image_id)

            transformed_img = transform.execute(image)

            self.context["image_objects"][transformed_image_id] = transformed_img

            transformed_image_ids.append(transformed_image_id)

            self.state[transformed_image_id] = images_manager.convert_to_base64(transformed_img)
            self.state[transformed_meta_id] = self.state[meta_id]

            self.state.hovered_id = -1

        self.state.transformed_image_ids = transformed_image_ids
        self.compute_annotations(transformed_image_ids)

        # Only invoke callbacks when we transform images
        if len(transformed_image_ids) > 0:
            self.on_transform(transformed_image_ids)

    def compute_annotations(self, ids):
        """Compute annotations for the given image ids using the object detector model."""
        if len(ids) == 0:
            return

        for id_ in ids:
            self.context["annotations"][id_] = []

        predictions = self.detector.eval(paths=ids, content=self.context.image_objects)

        for id_, annotations in predictions:
            image_annotations = self.context["annotations"].setdefault(id_, [])
            for prediction in annotations:
                category_id = 0
                for cat_id, cat in self.state.annotation_categories.items():
                    if cat["name"] == prediction["label"]:
                        category_id = cat_id

                bbox = prediction["box"]
                image_annotations.append(
                    {
                        "category_id": category_id,
                        "id": category_id,
                        "bbox": [
                            bbox["xmin"],
                            bbox["ymin"],
                            bbox["xmax"] - bbox["xmin"],
                            bbox["ymax"] - bbox["ymin"],
                        ],
                    }
                )

        self.update_model_result(ids, self.state.feature_extraction_model)

    def on_current_num_elements_change(self, current_num_elements, **kwargs):
        with open(self.state.current_dataset) as f:
            dataset = json.load(f)
        ids = [img["id"] for img in dataset["images"]]
        return self.on_selected_images_change(ids[:current_num_elements])

    def on_selected_images_change(self, selected_ids):
        source_image_ids = []

        current_dir = os.path.dirname(self.state.current_dataset)

        with open(self.state.current_dataset) as f:
            dataset = json.load(f)

        for selected_id in selected_ids:
            image_index = self.context.image_id_to_index[selected_id]
            if image_index >= len(dataset["images"]):
                continue

            image_metadata = dataset["images"][image_index]

            image_id = f"img_{image_metadata['id']}"
            meta_id = image_id_to_meta(image_id)

            source_image_ids.append(image_id)

            image_filename = os.path.join(current_dir, image_metadata["file_name"])

            img = self.context.images_manager.load_image(image_filename)

            self.state[image_id] = images_manager.convert_to_base64(img)
            self.state[meta_id] = {
                "width": image_metadata["width"],
                "height": image_metadata["height"],
            }
            self.state.hovered_id = -1

            self.context.image_objects[image_id] = img

        self.state.source_image_ids = source_image_ids
        self.compute_annotations(source_image_ids)
        self.update_model_result(self.state.source_image_ids, self.state.feature_extraction_model)
        self.on_apply_transform()

    def reset_data(self):
        source_image_ids = self.state.source_image_ids
        transformed_image_ids = self.state.transformed_image_ids

        self.state.source_image_ids = []
        self.state.transformed_image_ids = []
        self.state.annotation_categories = {}

        for image_id in source_image_ids:
            result_id = image_id_to_result(image_id)
            meta_id = image_id_to_meta(image_id)

            if self.state.has(image_id) and self.state[image_id] is not None:
                self.state[image_id] = None

            if self.state.has(result_id) and self.state[result_id] is not None:
                self.state[result_id] = None

            if self.state.has(meta_id) and self.state[meta_id] is not None:
                self.state[meta_id] = None

            if image_id in self.context["image_objects"]:
                del self.context["image_objects"][image_id]

        for image_id in transformed_image_ids:
            result_id = image_id_to_result(image_id)
            meta_id = image_id_to_meta(image_id)

            if self.state.has(image_id) and self.state[image_id] is not None:
                self.state[image_id] = None

            if self.state.has(result_id) and self.state[result_id] is not None:
                self.state[result_id] = None

            if self.state.has(meta_id) and self.state[meta_id] is not None:
                self.state[meta_id] = None

            if image_id in self.context["image_objects"]:
                del self.context["image_objects"][image_id]

    def on_current_dataset_change(self, current_dataset, **kwargs):
        logger.debug(f"on_current_dataset_change change {self.state}")

        self.reset_data()

        with open(current_dataset) as f:
            dataset = json.load(f)

        categories = {}

        for category in dataset["categories"]:
            categories[category["id"]] = category

        self.state.annotation_categories = categories

        self.context["annotations"] = {}

        self.context.image_id_to_index = {}
        for i, image in enumerate(dataset["images"]):
            self.context.image_id_to_index[image["id"]] = i

        if self.is_standalone_app:
            self.context.images_manager = images_manager.ImagesManager()

    def on_feature_extraction_model_change(self, **kwargs):
        logger.debug(f">>> on_feature_extraction_model_change change {self.state}")

        feature_extraction_model = self.state.feature_extraction_model

        self.update_model_result(self.state.source_image_ids, feature_extraction_model)
        self.update_model_result(self.state.transformed_image_ids, feature_extraction_model)

    def update_model_result(self, image_ids, feature_extraction_model):
        for image_id in image_ids:
            result_id = image_id_to_result(image_id)
            self.state[result_id] = self.context["annotations"].get(image_id, [])

    def on_image_hovered(self, index):
        self.state.hovered_id = index

    def set_on_hover(self, fn):
        self._on_hover_fn = fn

    def on_hover(self, hover_event):
        id_ = int(hover_event["id"])
        is_transformation = bool(hover_event["isTransformation"])
        self.on_image_hovered(id_)
        if self._on_hover_fn:
            self._on_hover_fn(id_, is_transformation)

    def settings_widget(self):
        with html.Div(trame_server=self.server):
            with html.Div(classes="col"):
                quasar.QSelect(
                    label="Object detection Model",
                    v_model=("object_detection_model", "facebook/detr-resnet-50"),
                    options=(
                        [
                            {
                                "label": "facebook/detr-resnet-50",
                                "value": "facebook/detr-resnet-50",
                            },
                        ],
                    ),
                    filled=True,
                    emit_value=True,
                    map_options=True,
                )

                self._parameters_app.transform_select_ui()

                with html.Div(
                    classes="q-pa-md q-ma-md",
                    style="border-style: solid; border-width: thin; border-radius: 0.5rem; border-color: lightgray;",
                ):
                    self._parameters_app.transform_params_ui()

    def apply_ui(self):
        with html.Div(trame_server=self.server):
            self._parameters_app.transform_apply_ui()

    def original_dataset_widget(self):
        with html.Div(trame_server=self.server):
            ui.image_list_component("source_image_ids", self.on_hover)

    def transformed_dataset_widget(self):
        with html.Div(trame_server=self.server):
            ui.image_list_component("transformed_image_ids", self.on_hover, is_transformation=True)

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
                                            options=(DATASET_DIRS,),
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

                            with html.Div(classes="col-5 q-pa-md"):
                                with html.Div(classes="row"):
                                    with html.Div(classes="col q-pa-md"):
                                        self.original_dataset_widget()

                            with html.Div(
                                classes="col-5 q-pa-md",
                                style="background-color: #ffcdcd;",
                            ):
                                with html.Div(classes="row"):
                                    with html.Div(classes="col q-pa-md"):
                                        self.transformed_dataset_widget()

                self._ui = layout
        return self._ui


def transforms(server=None, *args, **kwargs):
    server = get_server()
    server.client_type = "vue3"

    transforms_app = TransformsApp(server)
    transforms_app.ui

    server.start(**kwargs)


if __name__ == "__main__":
    transforms()
