from typing import Dict

from trame.ui.quasar import QLayout
from trame.widgets import quasar
from trame.widgets import html
from trame.app import get_server
from trame_client.widgets.trame import Getter

from trame_annotations.widgets.annotations import ImageDetection
from nrtk_explorer.app.images.image_server import ImageServer
from nrtk_explorer.widgets.nrtk_explorer import AnnotationAggregator

from nrtk_explorer.library.app_config import process_config
from nrtk_explorer.library.dataset import (
    get_dataset,
    expand_hugging_face_datasets,
    dataset_select_options,
)

import nrtk_explorer.library.transforms as trans
import nrtk_explorer.library.yaml_transforms as nrtk_yaml
import nrtk_explorer.library.serialization_helpers as serialization_helpers

from nrtk_explorer.app.applet import Applet
from nrtk_explorer.app.features.parameters import ParametersApp
from nrtk_explorer.app.images.images import Images

from nrtk_explorer.app.images.stateful_annotations import (
    make_stateful_annotations,
)

from nrtk_explorer.app.images.image_ids import (
    GROUND_TRUTH_MODEL,
)


class PreviewApp(Applet):
    def __init__(
        self,
        server,
        images=None,
        ground_truth_annotations=None,
        **kwargs,
    ):
        super().__init__(server)

        self.images = images or Images(server)

        self._image_server = ImageServer(server=self.server, images=self.images)

        self.ground_truth_annotations = ground_truth_annotations or make_stateful_annotations(
            server, GROUND_TRUTH_MODEL
        )
        self.context.ground_truth_annotations = self.ground_truth_annotations.annotations_factory

        if self.context.parameters_app is None:
            self.context.parameters_app = ParametersApp(
                server=server,
            )

        self._parameters_app = self.context.parameters_app

        self.state.dataset_ids = []
        self.state.preview_inference_models_obj = {0: {"name": "groundtruth"}}
        self.state.preview_image_id = None
        self.state.transformed_preview_image = None

        self._ui = None

        self._transform_classes: Dict[str, type[trans.ImageTransform]] = {
            "blur": trans.GaussianBlurTransform,
            "invert": trans.InvertTransform,
            "downsample": trans.DownSampleTransform,
            "identity": trans.IdentityTransform,
        }

        # Add transform from YAML definition
        self._transform_classes.update(nrtk_yaml.generate_transforms())

        self._parameters_app._transform_classes = self._transform_classes

        # Initialize the transforms pipeline to the identity
        self._parameters_app._default_transform = "blur"
        self._parameters_app.on_add_transform()

        self.server.controller.on_server_ready.add(self.on_server_ready)

    def on_server_ready(self, *args, **kwargs):
        self.server.controller.preview_transform.add(self.on_preview_transform)
        self.state.change("preview_image_id")(self.on_preview_transform)
        self.on_preview_transform()

    def on_preview_transform(self, **kwargs):
        preview_id = self.state.preview_image_id
        if preview_id is None:
            return

        transforms = list(map(lambda t: t["instance"], self.context.transforms))

        for transform in transforms:
            params = transform.get_parameters()
            for key, value in transform.get_parameters_description().items():
                if "deserialize_func" in value.keys():
                    params[key] = getattr(serialization_helpers, value["deserialize_func"])(
                        params[key]
                    )
            transform.set_parameters(params)

        chained_transform = trans.ChainedImageTransform(transforms)

        image = self.images.get_image_without_cache_eviction(preview_id)
        transformed_image = chained_transform.execute(image)
        import base64
        from io import BytesIO

        buffered = BytesIO()
        transformed_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        img_base64 = bytes("data:image/jpeg;base64,", encoding="utf-8") + img_str
        img_base64_str = img_base64.decode("utf-8")
        self.state.transformed_preview_image = img_base64_str

    def settings_widget(self):
        with html.Div(classes="col"):
            self._parameters_app.transforms_ui()

    def preview_ui(self):
        with html.Div():
            self._parameters_app.transform_preview_ui()

    def carousel_ui(self):
        with quasar.QCarousel(
            v_model=("preview_image_id",),
            style="padding-bottom: 6rem;",
            classes="fit",
            control_color="primary",
            animated=True,
            infinite=True,
            swipeable=True,
            navigation=True,
            thumbnails=True,
            arrows=True,
            padding=True,
            transition_prev="slide-right",
            transition_next="slide-left",
        ):
            with html.Template(
                raw_attrs=['v-slot:navigation-icon="{ index, name, active, btnProps, onClick }"']
            ):
                with Getter(name=("`img_${name}`",)):
                    quasar.QImg(
                        key=("name",),
                        classes="rounded-borders q-mr-md",
                        style=(
                            "active ? 'width: 6rem; height: 6rem; border-style: solid; border-width: 0.125rem; border-color: red;' : 'width: 6rem; height: 6rem;'",
                        ),
                        fit="cover",
                        src=("value",),
                        click="onClick",
                    )

            with html.Template(v_for=("identifier in dataset_ids",)):
                with quasar.QCarouselSlide(
                    name=("identifier",),
                    key=("identifier",),
                ):
                    with html.Div(
                        classes="row fit justify-start items-center q-gutter-xs q-col-gutter no-wrap",
                    ):
                        with AnnotationAggregator(
                            image_id=("identifier",),
                            transformed=False,
                            models=("preview_inference_models_obj",),
                        ):
                            with Getter(name=("`img_${identifier}`",)):
                                with html.Div(
                                    classes="rounded-borders col-6 full-height",
                                ):
                                    ImageDetection(
                                        identifier=("identifier",),
                                        src=("value",),
                                        models=("preview_inference_models_obj",),
                                        annotations=("aggregateAnnotations",),
                                        categories=("annotation_categories",),
                                        container_selector=".row",
                                        score_threshold=("confidence_score_threshold", 0.8),
                                        color_by="model",
                                    )

                        with AnnotationAggregator(
                            image_id=("identifier",),
                            transformed=True,
                            models=("preview_inference_models_obj",),
                        ):
                            with html.Div(
                                classes="rounded-borders col-6 full-height",
                            ):
                                ImageDetection(
                                    identifier=("identifier",),
                                    src=("transformed_preview_image",),
                                    models=("preview_inference_models_obj",),
                                    # annotations=("groundtruth_annotations",),
                                    annotations=("aggregateAnnotations",),
                                    categories=("annotation_categories",),
                                    container_selector=".row",
                                    score_threshold=("confidence_score_threshold", 0.8),
                                    color_by="model",
                                )

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
                    with quasar.QPage(classes="row"):
                        with html.Div(classes="col-2 q-pa-md"):
                            self.settings_widget()
                            self.preview_ui()

                        with html.Div(classes="col-10 q-pa-md bg-grey-3 shadow-2 rounded-borders"):
                            self.carousel_ui()

                self._ui = layout
        return self._ui


def load_dataset(server, **kwargs):
    import os
    import nrtk_explorer.test_data

    DIR_NAME = os.path.dirname(nrtk_explorer.test_data.__file__)
    DEFAULT_DATASETS = [
        f"{DIR_NAME}/coco-od-2017/test_val2017.json",
    ]
    NUM_IMAGES_DEFAULT = 500

    config_options = {
        "dataset": {
            "flags": ["--dataset"],
            "params": {
                "nargs": "+",
                "default": DEFAULT_DATASETS,
                "help": "Path to the JSON file describing the image dataset",
            },
        },
    }
    config = process_config(server.cli, config_options, **kwargs)

    server.state.input_datasets = expand_hugging_face_datasets(config["dataset"])

    server.state.all_datasets = server.state.input_datasets
    server.state.all_datasets_options = dataset_select_options(server.state.all_datasets)

    with server.state:
        server.state.num_images = NUM_IMAGES_DEFAULT
        server.state.num_images_max = 0
        server.state.dataset_ids = []  # sampled images
        server.state.user_selected_ids = []  # ensure image update in transforms app via image list
        server.context.dataset = get_dataset(server.state.all_datasets[0])
        server.state.num_images_max = len(server.context.dataset.imgs)
        server.state.num_images = min(server.state.num_images_max, server.state.num_images)
        server.state.dirty("num_images")  # Trigger resample_images()
        server.state.random_sampling_disabled = False
        server.state.num_images_disabled = False

        server.state.annotation_categories = {
            category["id"]: category for category in server.context.dataset.cats.values()
        }


def resample_images(server, images, **kwargs):
    import random

    ids = [image["id"] for image in server.context.dataset.imgs.values()]

    selected_images = []
    if server.state.num_images:
        if server.state.random_sampling:
            selected_images = random.sample(ids, min(len(ids), server.state.num_images))
        else:
            selected_images = ids[: server.state.num_images]
    else:
        selected_images = ids

    with server.state:
        server.context.dataset_ids = selected_images
        server.state.dataset_ids = [str(id) for id in server.context.dataset_ids]
        server.state.user_selected_ids = server.state.dataset_ids
        if len(server.state.dataset_ids) > 0:
            server.state.preview_image_id = server.state.dataset_ids[0]
        else:
            server.state.preview_image_id = None

        server.context.ground_truth_annotations.get_annotations(server.state.dataset_ids)


def main(server=None, *args, **kwargs):
    server = get_server(client_type="vue3")
    images = Images(server)

    load_dataset(server)

    transforms_app = PreviewApp(server, images)
    transforms_app.ui

    resample_images(server, images)

    server.start(**kwargs)


if __name__ == "__main__":
    main()
