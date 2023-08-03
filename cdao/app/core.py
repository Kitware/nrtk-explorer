r"""
Define your classes and create the instances that you need to expose
"""
import logging
from trame.app import get_server
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets  import html
from trame.widgets import vuetify3 as vuetify
from cdao.widgets import cdao as my_widgets
from cdao.app.utils import image_to_base64_str
from cdao.library import transforms

from cdao.app.ui.image_list import image_list_component

from cdao.library.ml_models import ClassificationResNet50, ClassificationAlexNet, ClassificationVgg16

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

DATASET_DIRS = [
    "/home/alessandro/Documents/OIRDS_v1_0/oirds_test.json",
    "/home/alessandro/Documents/OIRDS_v1_0/oirds_train.json",
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

        # initialize state + controller
        state, ctrl = server.state, server.controller

        # Set state variable
        state.trame__title = "cdao"

        self.models = {
            "ClassificationResNet50": ClassificationResNet50(server),
            "ClassificationAlexNet": ClassificationAlexNet(server),
            "ClassificationVgg16": ClassificationVgg16(server)
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

    def reset_data(self):
        source_image_ids = self.state.source_image_ids
        transformed_image_ids = self.state.transformed_image_ids

        self.state.source_image_ids = []
        self.state.transformed_image_ids = []

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
        
        for image_metadata in dataset["images"]:
            if i > MAX_IMAGES:
                break

            image_id = f"img_{image_metadata['id']}"
            meta_id = image_id_to_meta(image_id)
            image_filename = os.path.join(current_dir, image_metadata["file_name"])

            i += 1

            image_ids.append(image_id)

            img = ImageModule.open(image_filename)

            self.state[image_id] = image_to_base64_str(img, "png")
            self.state[meta_id] = {"width": image_metadata["width"], "height": image_metadata["height"]}
            self.local_state["image_objects"][image_id] = img

        self.local_state["annotations"] = {}

        for annotation in dataset["annotations"]:
            image_id = f"img_{annotation['image_id']}"
            image_annotations = self.local_state["annotations"].setdefault(image_id, [])
            image_annotations.append(annotation)

            transformed_image_id = f"transformed_{image_id}"
            image_annotations = self.local_state["annotations"].setdefault(transformed_image_id, [])
            image_annotations.append(annotation)

        self.state.source_image_ids = image_ids

        self.update_model_result(self.state.source_image_ids, self.state.current_model)
        self.on_current_transform_change(self.state.current_transform)

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
        with SinglePageLayout(self._server) as layout:
            # Toolbar
            layout.title.set_text("CDAO")
            with layout.toolbar:
                pass

            # Main content
            with layout.content:
                with vuetify.VRow():
                    with vuetify.VCol(cols=2):
                        with html.Div(classes="pa-2"):
                            vuetify.VSelect(
                                label="Dataset",
                                v_model=("current_dataset",),
                                items=(DATASET_DIRS,)
                            )

                            vuetify.VSelect(
                                label="Transform",
                                v_model=("current_transform",),
                                items=("transforms",)
                            )

                            vuetify.VSelect(
                                label="Model",
                                v_model=("current_model",),
                                items=("models",)
                            )

                    with vuetify.VCol(cols= 5):
                        html.H5("Original Dataset", classes="text-h5 pa-2")

                        with vuetify.VRow():
                            with vuetify.VCol(cols=12):
                                image_list_component("source_image_ids")

                    with vuetify.VCol(cols= 5, style="background-color: #ffcdcd;", v_if=("show_blue", True)):
                        html.H5("Transformed Dataset", classes="text-h5 pa-2")
                        
                        with vuetify.VRow():
                            with vuetify.VCol(cols=12):
                                image_list_component("transformed_image_ids")

            # Footer
            # layout.footer.hide()


def create_engine(server=None):
    # Get or create server
    if server is None:
        server = get_server()
    
    if isinstance(server, str):
        server = get_server(server)

    server.client_type = "vue3"

    return Engine(server)
