r"""
Define your classes and create the instances that you need to expose
"""
import logging
from trame.app import get_server
from trame.ui.quasar import QLayout
from trame.widgets import quasar
from trame.widgets import html
from cdao.app.utils import image_to_base64_str
from cdao.library import transforms

from cdao.app.ui.image_list import image_list_component
from cdao.app.embeddings import EmbeddingsApp
from cdao.app.applet import Translator

from cdao.library.ml_models import (
    ClassificationResNet50,
    ClassificationAlexNet,
    ClassificationVgg16,
)

from PIL import Image as ImageModule
from PIL.Image import Image
import os

import json


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def image_id_to_data(image_id):
    return f"{image_id}"


def image_id_to_meta(image_id):
    return f"{image_id}_meta"


def image_id_to_result(image_id):
    return f"{image_id}_result"


def image_id_to_thumb(image_id):
    return f"{image_id}_thumb"


# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


DIR_NAME = os.path.dirname(__file__)
DATASET_DIRS = [
    f"{DIR_NAME}/../../assets/OIRDS_v1_0/oirds_test.json",
    f"{DIR_NAME}/../../assets/OIRDS_v1_0/oirds_train.json",
]

MAX_IMAGES = 35


class Engine:
    def __init__(self, server=None):
        if server is None:
            server = get_server()

        self._local_state = {
            "image_objects": {},
        }

        self._server = server

        self._ui = None

        embeddings_state_translator = Translator()
        embeddings_state_translator.add_translation("current_model", "current_embeddings_model")

        self._embeddings_app = EmbeddingsApp(server, embeddings_state_translator)
        self._embeddings_app.set_on_select(self.on_selected_images_change)

        # initialize state + controller
        state, ctrl = server.state, server.controller

        # Set state variable
        state.trame__title = "cdao"

        self.models = {
            "ClassificationResNet50": ClassificationResNet50(server),
            "ClassificationAlexNet": ClassificationAlexNet(server),
            "ClassificationVgg16": ClassificationVgg16(server),
        }

        state.models = [k for k in self.models.keys()]
        state.current_model = state.models[0]

        self._transforms = {
            "identity": transforms.IdentityTransform(),
            "blur": transforms.GaussianBlurTransform(),
            "invert": transforms.InvertTransform(),
            "downsample": transforms.DownSampleTransform(),
        }

        self._transform_params = {
            "identity": [],
            "blur": [4],
            "invert": [],
            "downsample": [4],
        }

        state.annotation_categories = {}

        state.source_image_ids = []
        state.transformed_image_ids = []
        state.transforms = [k for k in self._transforms.keys()]
        state.current_transform = state.transforms[0]

        state.current_dataset = DATASET_DIRS[0]

        # Bind instance methods to controller
        ctrl.on_server_reload = self.ui

        # Initialize images, transformed images, and models
        # self.on_current_dataset_change(state.current_dataset)

        # Bind instance methods to state change
        state.change("current_dataset")(self.on_current_dataset_change)
        state.change("current_transform")(self.on_current_transform_change)
        state.change("current_model")(self.on_current_model_change)

        # Generate UI
        self.ui()

    @property
    def server(self):
        return self._server

    @property
    def state(self):
        return self.server.state

    @property
    def local_state(self):
        return self._local_state

    @property
    def ctrl(self):
        return self.server.controller

    def show_in_jupyter(self, **kwargs):
        from trame.app import jupyter

        logger.setLevel(logging.WARNING)
        jupyter.show(self.server, **kwargs)
    
    def on_selected_images_change(self, selected_ids):
        print("on_selected_images_change", selected_ids)
        source_image_ids = []

        current_dir = os.path.dirname(self.state.current_dataset)

        with open(self.state.current_dataset) as f:
            dataset = json.load(f)
        
        for selected_id in selected_ids:
            if (selected_id >= len(dataset["images"])):
                continue

            image_metadata = dataset["images"][selected_id]

            image_id = f"img_{image_metadata['id']}"
            meta_id = image_id_to_meta(image_id)

            source_image_ids.append(image_id)

            print(image_id, meta_id)

            # Don't re-read an image that has already been opened
            if self.state[image_id] is not None:
                continue

            image_filename = os.path.join(current_dir, image_metadata["file_name"])

            print(image_filename)

            img = ImageModule.open(image_filename)

            self.state[image_id] = image_to_base64_str(img, "png")
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

    def on_current_model_change(self, current_model, **kwargs):
        logger.info(f">>> ENGINE(a): on_current_model_change change {self.state}")

        self.update_model_result(self.state.source_image_ids, current_model)
        self.update_model_result(self.state.transformed_image_ids, current_model)

    def update_model_result(self, image_ids, current_model):
        for image_id in image_ids:
            result_id = image_id_to_result(image_id)
            self.state[result_id] = self.local_state["annotations"].get(image_id, [])

        # model = self.models[current_model]

        # for image_id in image_ids:
        #     img = np.array(self.local_state["image_objects"][image_id])
        #     result = model.run(img)

        #     result_id = image_id_to_result(image_id)

        #     classes = result.get("classes", [])
        #     df = pd.DataFrame(classes, columns=["Class", "Score"])
        #     df.sort_values("Score", ascending=True, inplace=True)
        #     df = df[-4:]

        #     chart = px.bar(df, x="Score", y="Class")
        #     chart.update_layout(
        #         xaxis_title="",
        #         yaxis_title="",
        #         showlegend=False,
        #         margin=dict(b=0, l=0, r=0, t=0),
        #     )

        #     self.state[result_id] = encode(chart.to_plotly_json())

    def on_current_transform_change(self, current_transform, **kwargs):
        logger.info(f">>> ENGINE(a): on_current_transform_change change {self.state}")

        transform = self._transforms[current_transform]
        params = self._transform_params[current_transform]

        transformed_image_ids = []

        for image_id in self.state.source_image_ids:
            image = self.local_state["image_objects"][image_id]

            transformed_image_id = f"transformed_{image_id}"
            meta_id = image_id_to_meta(image_id)
            transformed_meta_id = image_id_to_meta(transformed_image_id)

            transformed_img = transform.execute(image, *params)

            self.local_state["image_objects"][transformed_image_id] = transformed_img

            transformed_image_ids.append(transformed_image_id)

            self.state[transformed_image_id] = image_to_base64_str(transformed_img, "png")
            self.state[transformed_meta_id] = self.state[meta_id]

        self.state.transformed_image_ids = transformed_image_ids

        self.update_model_result(self.state.transformed_image_ids, self.state.current_model)

    def ui(self, *args, **kwargs):
        if self._ui is None:
            with QLayout(
                self._server, view="lhh LpR lff", classes="shadow-2 rounded-borders bg-grey-2"
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
                        quasar.QToolbarTitle("CDAO")

                # # Main content
                with quasar.QPageContainer():
                    with quasar.QPage():
                        with html.Div(classes="row"):
                            with html.Div(classes="col-2 q-pa-md"):
                                self._embeddings_app.settings_widget()

                                quasar.QSelect(
                                    label="Dataset",
                                    v_model=("current_dataset",),
                                    options=(DATASET_DIRS,),
                                )

                                quasar.QSelect(
                                    label="Transform",
                                    v_model=("current_transform",),
                                    options=("transforms",),
                                )

                                quasar.QSelect(
                                    label="Model", v_model=("current_model",), options=("models",)
                                )

                            with html.Div(classes="col-5 q-pa-md"):
                                html.H5("Original Dataset", classes="text-h5")

                                with html.Div(classes="row", style="min-height: inherit; height: 30rem"):
                                    with html.Div(classes="col q-pa-md"):
                                        self._embeddings_app.visualization_widget()

                                with html.Div(classes="row"):
                                    with html.Div(classes="col q-pa-md"):
                                        image_list_component("source_image_ids")

                            with html.Div(
                                classes="col-5 q-pa-md",
                                style="background-color: #ffcdcd;",
                            ):
                                html.H5("Transformed Dataset", classes="text-h5")

                                with html.Div(classes="row", style="min-height: inherit; height: 30rem"):
                                    with html.Div(classes="col q-pa-md"):
                                        self._embeddings_app.visualization_widget()

                                with html.Div(classes="row"):
                                    with html.Div(classes="col q-pa-md"):
                                        image_list_component("transformed_image_ids")

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
