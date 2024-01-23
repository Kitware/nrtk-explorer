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

        # Set state variable
        self.state.trame__title = "nrtk_explorer"

        self.state.source_image_ids = []
        self.state.current_dataset = DATASET_DIRS[0]

        # Bind instance methods to controller
        self.ctrl.on_server_reload = self.ui
        self.ctrl.add("on_server_ready")(self.on_server_ready)

        # Generate UI
        self.ui()

    def on_server_ready(self, *args, **kwargs):
        # Bind instance methods to state change
        self.on_current_dataset_change()
        self.state.change("current_dataset")(self.on_current_dataset_change)

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

    def on_current_dataset_change(self, **kwargs):
        logger.info(f">>> ENGINE(a): on_current_dataset_change change {self.state}")

        self.reset_data()

        current_dataset = self.state.current_dataset

        with open(current_dataset) as f:
            dataset = json.load(f)

        categories = {}

        for category in dataset["categories"]:
            categories[category["id"]] = category

        self.state.annotation_categories = categories

        self.context["annotations"] = {}

        for annotation in dataset["annotations"]:
            image_id = f"img_{annotation['image_id']}"
            image_annotations = self.context["annotations"].setdefault(image_id, [])
            image_annotations.append(annotation)

            transformed_image_id = f"transformed_{image_id}"
            image_annotations = self.context["annotations"].setdefault(transformed_image_id, [])
            image_annotations.append(annotation)

        self.context["images_manager"] = images_manager.ImagesManager()

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
