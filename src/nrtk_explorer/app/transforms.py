r"""
Define your classes and create the instances that you need to expose
"""

import logging
from typing import Dict
import asyncio
import functools

from trame.ui.quasar import QLayout
from trame.widgets import quasar
from trame.widgets import html
from trame.app import get_server, asynchronous

import nrtk_explorer.library.transforms as trans
import nrtk_explorer.library.nrtk_transforms as nrtk_trans
from nrtk_explorer.library import images_manager, object_detector
from nrtk_explorer.app import ui
from nrtk_explorer.app.applet import Applet
from nrtk.impls.score_detections.class_agnostic_pixelwise_iou_scorer import (
    ClassAgnosticPixelwiseIoUScorer,
)
from nrtk_explorer.app.parameters import ParametersApp
from nrtk_explorer.app.image_meta import (
    update_image_meta,
    delete_image_meta,
)
from nrtk_explorer.library.coco_utils import (
    convert_from_ground_truth_to_first_arg,
    convert_from_ground_truth_to_second_arg,
    convert_from_predictions_to_second_arg,
    convert_from_predictions_to_first_arg,
)
import nrtk_explorer.test_data
from nrtk_explorer.app.trame_utils import delete_state
from nrtk_explorer.app.image_ids import image_id_to_dataset_id, image_id_to_result_id


import json
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DIR_NAME = os.path.dirname(nrtk_explorer.test_data.__file__)
DATASET_DIRS = [
    f"{DIR_NAME}/OIRDS_v1_0/oirds.json",
    f"{DIR_NAME}/OIRDS_v1_0/oirds_test.json",
    f"{DIR_NAME}/OIRDS_v1_0/oirds_train.json",
]


class TransformsApp(Applet):
    def __init__(self, server):
        super().__init__(server)

        self.update_image_meta = functools.partial(update_image_meta, self.server.state)

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

        self._on_transform_fn = None
        self.state.models = [
            "ClassificationResNet50",
            "ClassificationAlexNet",
            "ClassificationVgg16",
        ]
        self.state.feature_extraction_model = self.state.models[0]

        self._transforms: Dict[str, trans.ImageTransform] = {
            "identity": trans.IdentityTransform(),
            "blur": trans.GaussianBlurTransform(),
            "invert": trans.InvertTransform(),
            "downsample": trans.DownSampleTransform(),
        }

        if nrtk_trans.nrtk_transforms_available():
            self._transforms["nrtk_blur"] = nrtk_trans.NrtkGaussianBlurTransform()
            self._transforms["nrtk_pybsm"] = nrtk_trans.NrtkPybsmTransform()

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
        self.detector = object_detector.ObjectDetector(model_name="facebook/detr-resnet-50")

    def on_server_ready(self, *args, **kwargs):
        # Bind instance methods to state change
        self.state.change("feature_extraction_model")(self.on_feature_extraction_model_change)
        self.state.change("current_dataset")(self.on_current_dataset_change)
        self.state.change("current_num_elements")(self.on_current_num_elements_change)
        self.state.change("enabled_model_images")(self.on_detection_model_change)

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
            transformed_img = transform.execute(image)
            if image.size != transformed_img.size:
                # Resize so pixel-wise annotation similarity score works
                transformed_img = transformed_img.resize(image.size)
            self.context["image_objects"][transformed_image_id] = transformed_img
            transformed_image_ids.append(transformed_image_id)
            self.state[transformed_image_id] = images_manager.convert_to_base64(transformed_img)

        self.state.transformed_image_ids = transformed_image_ids
        if len(self.state.source_image_ids) > 0:
            self.state.hovered_id = ""

        if len(transformed_image_ids) > 0:
            with open(self.state.current_dataset) as f:
                dataset = json.load(f)

                # Erase current annotations
                ids = [int(image_id_to_dataset_id(id)) for id in self.state.source_image_ids]
                for ann in dataset["annotations"]:
                    if ann["image_id"] in ids:
                        transformed_id = f"transformed_img_{ann['image_id']}"
                        if transformed_id in self.context["annotations"]:
                            del self.context["annotations"][transformed_id]

                # Compute new annotations
                if "transformation" in self.state.enabled_model_images:
                    predictions = convert_from_predictions_to_second_arg(
                        self.compute_annotations(transformed_image_ids)
                    )
                else:
                    for ann in dataset["annotations"]:
                        if ann["image_id"] in ids:
                            image_annotations = self.context["annotations"].setdefault(
                                f"transformed_img_{ann['image_id']}", []
                            )
                            image_annotations.append(ann)

                    predictions = convert_from_ground_truth_to_second_arg(
                        [
                            self.context["annotations"][id_]
                            for id_ in self.state.transformed_image_ids
                        ],
                        dataset,
                    )

                self.compute_score(
                    self.state.source_image_ids, self.predictions_source_images, predictions
                )

            self.update_model_result(transformed_image_ids)

            # Only invoke callbacks when we transform images
            self.on_transform(transformed_image_ids)

    def compute_score(self, ids, predictions_source_images, predictions_trans_images):
        """Compute score for image ids."""
        score_output = ClassAgnosticPixelwiseIoUScorer().score(
            predictions_source_images, predictions_trans_images
        )

        for image_id, score in zip(ids, score_output):
            update_image_meta(self.state, image_id.split("_")[-1], {"distance": score})

    def compute_annotations(self, ids):
        """Compute annotations for the given image ids using the object detector model."""
        if len(ids) == 0:
            return

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
                        "id": None,
                        "bbox": [
                            bbox["xmin"],
                            bbox["ymin"],
                            bbox["xmax"] - bbox["xmin"],
                            bbox["ymax"] - bbox["ymin"],
                        ],
                    }
                )

        return predictions

    def on_current_num_elements_change(self, current_num_elements, **kwargs):
        with open(self.state.current_dataset) as f:
            dataset = json.load(f)
        ids = [img["id"] for img in dataset["images"]]
        return self.set_source_images(ids[:current_num_elements])

    def on_detection_model_change(self, enabled_model_images, **kwargs):
        """Update the model result when the detection model changes."""
        self.compute_predictions_source_images(self.state.source_image_ids)
        self.update_model_result(self.state.source_image_ids)
        self.on_apply_transform()

    def compute_predictions_source_images(self, ids):
        """Compute the predictions for the source images."""
        if len(ids) > 0:
            with open(self.state.current_dataset) as f:
                dataset = json.load(f)
                for id_ in ids:
                    del self.context["annotations"][id_]

                if "source" in self.state.enabled_model_images:
                    self.predictions_source_images = convert_from_predictions_to_first_arg(
                        self.compute_annotations(ids),
                        dataset,
                        ids,
                    )
                else:
                    for annotation in dataset["annotations"]:
                        image_id = f"img_{annotation['image_id']}"
                        image_annotations = self.context["annotations"].setdefault(image_id, [])
                        image_annotations.append(annotation)

                    self.predictions_source_images = convert_from_ground_truth_to_first_arg(
                        [self.context["annotations"][id_] for id_ in ids]
                    )

    def _update_images(self, selected_ids):
        source_image_ids = []

        current_dir = os.path.dirname(self.state.current_dataset)

        dataset = None
        with open(self.state.current_dataset) as f:
            dataset = json.load(f)

        for selected_id in selected_ids:
            image_index = self.context.image_id_to_index[selected_id]
            if image_index >= len(dataset["images"]):
                continue

            image_metadata = dataset["images"][image_index]

            image_id = f"img_{image_metadata['id']}"

            source_image_ids.append(image_id)

            image_filename = os.path.join(current_dir, image_metadata["file_name"])

            img = self.context.images_manager.load_image(image_filename)

            self.state[image_id] = images_manager.convert_to_base64(img)
            self.update_image_meta(
                image_metadata["id"],
                {"width": image_metadata["width"], "height": image_metadata["height"]},
            )

            self.context.image_objects[image_id] = img

        if len(selected_ids) > 0:
            self.state.hovered_id = ""

        self.state.source_image_ids = source_image_ids
        self.compute_predictions_source_images(self.state.source_image_ids)

        self.update_model_result(source_image_ids)
        self.on_apply_transform()

    async def _set_source_images(self, selected_ids):
        # We need to yield twice for the self.state.loading_images=True to
        # commit to the trame state to show a spinner
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        self._update_images(selected_ids)
        with self.state:
            self.state.loading_images = False

    def set_source_images(self, selected_ids):
        if len(selected_ids):
            self.state.loading_images = True
        if hasattr(self, "_set_source_images_task"):
            self._set_source_images_task.cancel()
        self._set_source_images_task = asynchronous.create_task(
            self._set_source_images(selected_ids)
        )

    def reset_data(self):
        source_and_transformed = self.state.source_image_ids + self.state.transformed_image_ids
        for image_id in source_and_transformed:
            delete_state(self.state, image_id)
            if image_id in self.context["image_objects"]:
                del self.context["image_objects"][image_id]
            result_id = image_id_to_result_id(image_id)
            delete_state(self.state, result_id)

        for image_id in self.state.source_image_ids:
            dataset_id = image_id_to_dataset_id(image_id)
            delete_image_meta(self.server.state, dataset_id)

        self.state.source_image_ids = []
        self.state.transformed_image_ids = []
        self.state.annotation_categories = {}

    def on_current_dataset_change(self, current_dataset, **kwargs):
        logger.debug(f"on_current_dataset_change change {self.state}")

        self.reset_data()

        with open(current_dataset) as f:
            dataset = json.load(f)

        categories = {}

        for category in dataset["categories"]:
            categories[category["id"]] = category

        self.state.annotation_categories = categories

        if "source" not in self.state.enabled_model_images:
            for annotation in dataset["annotations"]:
                image_id = f"img_{annotation['image_id']}"
                image_annotations = self.context["annotations"].setdefault(image_id, [])
                image_annotations.append(annotation)

        self.context.image_id_to_index = {}
        for i, image in enumerate(dataset["images"]):
            self.context.image_id_to_index[image["id"]] = i

        if self.is_standalone_app:
            self.context.images_manager = images_manager.ImagesManager()

    def on_feature_extraction_model_change(self, **kwargs):
        logger.debug(f">>> on_feature_extraction_model_change change {self.state}")

        self.update_model_result(self.state.source_image_ids)
        self.update_model_result(self.state.transformed_image_ids)

    def update_model_result(self, image_ids):
        for image_id in image_ids:
            result_id = image_id_to_result_id(image_id)
            self.state[result_id] = self.context["annotations"].get(image_id, [])

    def on_image_hovered(self, id):
        self.state.hovered_id = id

    def set_on_hover(self, fn):
        self._on_hover_fn = fn

    def on_hover(self, hover_event):
        id_ = hover_event["id"]
        self.on_image_hovered(id_)
        if self._on_hover_fn:
            self._on_hover_fn(id_)

    def settings_widget(self):
        with html.Div(trame_server=self.server):
            with html.Div(classes="col"):
                self._parameters_app.transform_select_ui()

                with html.Div(
                    classes="q-pa-md q-ma-md",
                    style="border-style: solid; border-width: thin; border-radius: 0.5rem; border-color: lightgray;",
                ):
                    self._parameters_app.transform_params_ui()

    def apply_ui(self):
        with html.Div(trame_server=self.server):
            self._parameters_app.transform_apply_ui()

    def dataset_widget(self):
        ui.ImageList(self.on_hover)

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

                            self.dataset_widget()

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
