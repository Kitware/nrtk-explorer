r"""
Define your classes and create the instances that you need to expose
"""
import logging

from trame.ui.quasar import QLayout
from trame.widgets import quasar
from trame.widgets import html
from trame.app import get_server

import cdao.library.transforms as trans
from cdao.library import images_manager
from cdao.app.ui.image_list import image_list_component
from cdao.app.applet import Applet
from cdao.library.ml_models import (
    ClassificationResNet50,
    ClassificationAlexNet,
    ClassificationVgg16,
)

import json
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def image_id_to_meta(image_id):
    return f"{image_id}_meta"


def image_id_to_result(image_id):
    return f"{image_id}_result"


# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


DIR_NAME = os.path.dirname(__file__)
DATASET_DIRS = [
    f"{DIR_NAME}/../../assets/OIRDS_v1_0/oirds.json",
    f"{DIR_NAME}/../../assets/OIRDS_v1_0/oirds_test.json",
    f"{DIR_NAME}/../../assets/OIRDS_v1_0/oirds_train.json",
]


class TransformsApp(Applet):
    @property
    def state(self):
        return self.server.state

    @property
    def local_state(self):
        return self.server._local_state

    def __init__(
        self,
        server,
        state_translator=None,
        controller_translator=None,
        local_state_translator=None,
    ):
        super().__init__(server, state_translator, controller_translator, local_state_translator)
        self._ui = None

        self.is_standalone_app = state_translator == None
        if self.is_standalone_app:
            self.local_state["images_manager"] = images_manager.ImagesManager()

            self.server._local_state = {
                "image_objects": {},
            }

        self.models = {
            "ClassificationResNet50": ClassificationResNet50(server),
            "ClassificationAlexNet": ClassificationAlexNet(server),
            "ClassificationVgg16": ClassificationVgg16(server),
        }

        self._on_transform_fn = None
        self.state.models = [k for k in self.models.keys()]
        self.state.current_model = self.state.models[0]

        self._transforms = {
            "identity": trans.IdentityTransform(),
            "blur": trans.GaussianBlurTransform(),
            "invert": trans.InvertTransform(),
            "downsample": trans.DownSampleTransform(),
        }

        self._transform_params = {
            "identity": [],
            "blur": [4],
            "invert": [],
            "downsample": [4],
        }

        self.state.annotation_categories = {}

        self.state.source_image_ids = []
        self.state.transformed_image_ids = []
        self.state.transforms = [k for k in self._transforms.keys()]
        self.state.current_transform = self.state.transforms[0]

        if self.state.current_dataset is None:
            self.state.current_dataset = DATASET_DIRS[0]

        if self.state.current_num_elements is None and self.is_standalone_app:
            self.state.current_num_elements = 15
            self.state.change("current_num_elements")(self.on_current_num_elements_change)

        # Bind instance methods to state change
        self.state.change("current_transform")(self.on_current_transform_change)
        self.state.change("current_model")(self.on_current_model_change)
        self.state.change("current_dataset")(self.on_current_dataset_change)

        self.local_state["images_manager"] = images_manager.ImagesManager()

    def set_on_transform(self, fn):
        self._on_transform_fn = fn

    def on_transform(self, *args, **kwargs):
        if self._on_transform_fn:
            self._on_transform_fn(*args, **kwargs)

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
            if selected_id >= len(dataset["images"]):
                continue

            image_metadata = dataset["images"][selected_id]

            image_id = f"img_{image_metadata['id']}"
            meta_id = image_id_to_meta(image_id)

            source_image_ids.append(image_id)

            image_filename = os.path.join(current_dir, image_metadata["file_name"])

            img = self.local_state["images_manager"].LoadImage(image_filename)

            self.state[image_id] = self.local_state["images_manager"].ComputeBase64(image_id, img)
            self.state[meta_id] = {
                "width": image_metadata["width"],
                "height": image_metadata["height"],
            }
            self.local_state["image_objects"][image_id] = img

        self.state.source_image_ids = source_image_ids

        self.update_model_result(self.state.source_image_ids, self.state.current_model)
        self.on_current_transform_change(self.state.current_transform)

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

            if image_id in self.local_state["image_objects"]:
                del self.local_state["image_objects"][image_id]

        for image_id in transformed_image_ids:
            result_id = image_id_to_result(image_id)
            meta_id = image_id_to_meta(image_id)

            if self.state.has(image_id) and self.state[image_id] is not None:
                self.state[image_id] = None

            if self.state.has(result_id) and self.state[result_id] is not None:
                self.state[result_id] = None

            if self.state.has(meta_id) and self.state[meta_id] is not None:
                self.state[meta_id] = None

            if image_id in self.local_state["image_objects"]:
                del self.local_state["image_objects"][image_id]

    def on_current_dataset_change(self, current_dataset, **kwargs):
        logger.info(f">>> ENGINE(a): on_current_dataset_change change {self.state}")

        self.reset_data()

        i = 0

        image_ids = []

        current_dir = os.path.dirname(current_dataset)

        with open(current_dataset) as f:
            dataset = json.load(f)

        categories = {}

        for category in dataset["categories"]:
            categories[category["id"]] = category

        self.state.annotation_categories = categories

        self.local_state["annotations"] = {}

        for annotation in dataset["annotations"]:
            image_id = f"img_{annotation['image_id']}"
            image_annotations = self.local_state["annotations"].setdefault(image_id, [])
            image_annotations.append(annotation)

            transformed_image_id = f"transformed_{image_id}"
            image_annotations = self.local_state["annotations"].setdefault(
                transformed_image_id, []
            )
            image_annotations.append(annotation)

        self.local_state["images_manager"] = images_manager.ImagesManager()

    def on_current_model_change(self, current_model, **kwargs):
        logger.info(f">>> ENGINE(a): on_current_model_change change {self.state}")

        self.update_model_result(self.state.source_image_ids, current_model)
        self.update_model_result(self.state.transformed_image_ids, current_model)

    def update_model_result(self, image_ids, current_model):
        for image_id in image_ids:
            result_id = image_id_to_result(image_id)
            self.state[result_id] = self.local_state["annotations"].get(image_id, [])

    def on_current_transform_change(self, current_transform, **kwargs):
        logger.info(f">>> ENGINE(a): on_current_transform_change change {self.state}")

        transformed_image_ids = []
        transform = self._transforms[current_transform]
        params = self._transform_params[current_transform]

        for image_id in self.state.source_image_ids:
            image = self.local_state["image_objects"][image_id]

            transformed_image_id = f"transformed_{image_id}"
            meta_id = image_id_to_meta(image_id)
            transformed_meta_id = image_id_to_meta(transformed_image_id)

            transformed_img = transform.execute(image, *params)

            self.local_state["image_objects"][transformed_image_id] = transformed_img

            transformed_image_ids.append(transformed_image_id)

            self.state[transformed_image_id] = self.local_state["images_manager"].ComputeBase64(
                transformed_image_id, transformed_img
            )
            self.state[transformed_meta_id] = self.state[meta_id]

        self.state.transformed_image_ids = transformed_image_ids

        self.update_model_result(self.state.transformed_image_ids, self.state.current_model)

        # Only invoke callbacks when we transform images
        if len(transformed_image_ids) > 0:
            self.on_transform(transformed_image_ids)

    def settings_widget(self):
        with html.Div(classes="column justify-center", style="padding:1rem"):
            with html.Div(classes="col"):
                quasar.QSelect(
                    label="Transform",
                    v_model=("current_transform",),
                    options=("transforms",),
                    filled=True,
                    emit_value=True,
                    map_options=True,
                )

                quasar.QSelect(
                    label="Model",
                    v_model=("current_model",),
                    options=("models",),
                    filled=True,
                    emit_value=True,
                    map_options=True,
                )

    def original_dataset_widget(self):
        image_list_component("source_image_ids")

    def transformed_dataset_widget(self):
        image_list_component("transformed_image_ids")

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
                                            v_model=("current_num_elements", 15),
                                            min=(0,),
                                            max=(25,),
                                            step=(1,),
                                            label=True,
                                            label_always=True,
                                        )
                                self.settings_widget()

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
