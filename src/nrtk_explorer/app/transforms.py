import logging
from typing import Dict, Callable

from trame.ui.quasar import QLayout
from trame.widgets import quasar
from trame.widgets import html
from trame.app import get_server, asynchronous
from trame_server import Server

import nrtk_explorer.library.transforms as trans
import nrtk_explorer.library.nrtk_transforms as nrtk_trans
import nrtk_explorer.library.yaml_transforms as nrtk_yaml
from nrtk_explorer.library import object_detector
from nrtk_explorer.app.applet import Applet
from nrtk_explorer.app.parameters import ParametersApp
from nrtk_explorer.app.images.image_meta import update_image_meta, dataset_id_to_meta
from nrtk_explorer.library.coco_utils import (
    compute_score,
)
from nrtk_explorer.app.trame_utils import change_checker, delete_state

from nrtk_explorer.app.images.image_ids import (
    dataset_id_to_image_id,
    dataset_id_to_transformed_image_id,
)
from nrtk_explorer.app.images.images import Images
from nrtk_explorer.app.images.stateful_annotations import (
    make_stateful_annotations,
    make_stateful_predictor,
)
from nrtk_explorer.app.ui import ImageList
from nrtk_explorer.app.ui.image_list import (
    TRANSFORM_COLUMNS,
    ORIGINAL_COLUMNS,
    init_visible_columns,
)


INFERENCE_MODELS_DEFAULT = [
    "facebook/detr-resnet-50",
    "hustvl/yolos-tiny",
    "valentinafeve/yolos-fashionpedia",
]


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ProcessingStep:
    def __init__(
        self,
        server: Server,
        feature_enabled_state_key: str,
        gui_switch_key: str,
        column_name: str,
        enabled_callback: Callable,
    ):
        self.state = server.state
        self.feature_enabled_state_key = feature_enabled_state_key
        self.gui_switch_key = gui_switch_key
        self.enabled_callback = enabled_callback
        self.column_name = column_name
        self.state.change(self.gui_switch_key)(self.on_gui_switch)
        self.update_feature_enabled_state()
        self.state.change("visible_columns", self.gui_switch_key)(
            self.update_feature_enabled_state
        )
        self.state.change(self.feature_enabled_state_key)(self.on_change_feature_enabled)

    def on_gui_switch(self, **kwargs):
        if self.state[self.gui_switch_key]:
            self.state.visible_columns = list(set([*self.state.visible_columns, self.column_name]))
        else:
            self.state.visible_columns = [
                col for col in self.state.visible_columns if col != self.column_name
            ]

    def update_feature_enabled_state(self, **kwargs):
        self.state[self.feature_enabled_state_key] = (
            self.column_name in self.state.visible_columns and self.state[self.gui_switch_key]
        )

    def on_change_feature_enabled(self, **kwargs):
        if self.state[self.feature_enabled_state_key]:
            self.enabled_callback()


class TransformsApp(Applet):
    def __init__(
        self,
        server,
        images=None,
        ground_truth_annotations=None,
        original_detection_annotations=None,
        transformed_detection_annotations=None,
    ):
        super().__init__(server)

        self.server.cli.add_argument(
            "--models",
            nargs="+",
            default=INFERENCE_MODELS_DEFAULT,
            help="Space separated list of inference models",
        )

        known_args, _ = self.server.cli.parse_known_args()
        self.state.inference_models = known_args.models
        self.state.object_detection_model = self.state.inference_models[0]
        self.state.setdefault("image_list_ids", [])
        self.state.setdefault("dataset_ids", [])
        self.state.setdefault("user_selected_ids", [])

        self.images = images or Images(server)

        ground_truth_annotations = ground_truth_annotations or make_stateful_annotations(server)
        self.ground_truth_annotations = ground_truth_annotations.annotations_factory

        original_detection_annotations = original_detection_annotations or make_stateful_predictor(
            server
        )
        self.original_detection_annotations = original_detection_annotations.annotations_factory

        transformed_detection_annotations = (
            transformed_detection_annotations or make_stateful_predictor(server)
        )
        self.transformed_detection_annotations = (
            transformed_detection_annotations.annotations_factory
        )

        def clear_transformed(**kwargs):
            self.transformed_detection_annotations.cache_clear()
            for id in self.state.dataset_ids:
                update_image_meta(
                    self.state,
                    id,
                    {
                        "original_detection_to_transformed_detection_score": 0,
                        "ground_truth_to_transformed_detection_score": 0,
                    },
                )

        server.controller.apply_transform.add(clear_transformed)

        # delete score from state of old ids that are not in new
        def delete_meta_state(old_ids, new_ids):
            if old_ids is not None:
                to_clean = set(old_ids) - set(new_ids)
                for id in to_clean:
                    delete_state(self.state, dataset_id_to_meta(id))

        change_checker(self.state, "dataset_ids")(delete_meta_state)

        self._parameters_app = ParametersApp(
            server=server,
        )

        self._ui = None

        self._on_transform_fn = None

        self._transform_classes: Dict[str, type[trans.ImageTransform]] = {
            "blur": trans.GaussianBlurTransform,
            "invert": trans.InvertTransform,
            "downsample": trans.DownSampleTransform,
            "identity": trans.IdentityTransform,
        }

        if nrtk_trans.nrtk_transforms_available():
            self._transform_classes["nrtk_pybsm"] = nrtk_trans.NrtkPybsmTransform

        # Add transform from YAML definition
        self._transform_classes.update(nrtk_yaml.generate_transforms())

        self._parameters_app._transform_classes = self._transform_classes

        # Initialize the transforms pipeline to the identity
        self._parameters_app._default_transform = "blur"
        self._parameters_app.on_add_transform()

        init_visible_columns(self.state)

        # On annotations enabled, run whole pipeline to possibly compute transforms. Why? Transforms compute scores are based on original images
        self.annotations_enable_control = ProcessingStep(
            server,
            feature_enabled_state_key="predictions_original_images_enabled",
            gui_switch_key="annotations_enabled_switch",
            column_name=ORIGINAL_COLUMNS[0],
            enabled_callback=self._start_update_images,
        )

        self.transform_enable_control = ProcessingStep(
            server,
            feature_enabled_state_key="transform_enabled",
            gui_switch_key="transform_enabled_switch",
            column_name=TRANSFORM_COLUMNS[0],
            enabled_callback=self._start_transformed_images,
        )

        self.server.controller.on_server_ready.add(self.on_server_ready)
        self.server.controller.apply_transform.add(self.on_apply_transform)
        self._on_hover_fn = None

        self.visible_dataset_ids = []  # set by ImageList via self.on_scroll callback

    def on_server_ready(self, *args, **kwargs):
        self.state.change("object_detection_model")(self.on_object_detection_model_change)
        self.on_object_detection_model_change()
        self.state.change("current_dataset")(self._cancel_update_images)
        self.state.change("current_dataset")(self.reset_detector)

    def on_object_detection_model_change(self, **kwargs):
        self.original_detection_annotations.cache_clear()
        self.transformed_detection_annotations.cache_clear()
        self.detector = object_detector.ObjectDetector(
            model_name=self.state.object_detection_model
        )
        self._start_update_images()

    def reset_detector(self, **kwargs):
        self.detector.reset()

    def set_on_transform(self, fn):
        self._on_transform_fn = fn

    def on_transform(self, *args, **kwargs):
        if self._on_transform_fn:
            self._on_transform_fn(*args, **kwargs)

    def on_apply_transform(self, **kwargs):
        # Turn on switch if user clicked lower apply button
        self.state.transform_enabled_switch = True
        self._start_transformed_images()

    def _start_transformed_images(self, *args, **kwargs):
        logger.debug("_start_transformed_images")
        if self._updating_images():
            if self._updating_transformed_images:
                # computing stale transformed images, restart task
                self._cancel_update_images()
            else:
                return  # update_images will call update_transformed_images() at the end
        self._update_task = asynchronous.create_task(
            self.update_transformed_images(self.visible_dataset_ids)
        )

    async def update_transformed_images(self, dataset_ids):
        self._updating_transformed_images = True
        try:
            await self._update_transformed_images(dataset_ids)
        finally:
            self._updating_transformed_images = False

    async def _update_transformed_images(self, dataset_ids):
        if not self.state.transform_enabled:
            return

        transforms = list(map(lambda t: t["instance"], self.context.transforms))
        transform = trans.ChainedImageTransform(transforms)

        id_to_matching_size_img = {}
        for id in dataset_ids:
            with self.state:
                transformed = self.images.get_stateful_transformed_image(transform, id)
                id_to_matching_size_img[dataset_id_to_transformed_image_id(id)] = transformed
            await self.server.network_completion

        with self.state:
            annotations = self.transformed_detection_annotations.get_annotations(
                self.detector, id_to_matching_size_img
            )
        await self.server.network_completion

        # depends on original images predictions
        if self.state.predictions_original_images_enabled:
            scores = compute_score(
                self.context.dataset,
                {
                    "annotations": self.predictions_original_images,
                    "type": "predictions",
                },
                {
                    "annotations": annotations,
                    "type": "predictions",
                },
            )
            for id, score in scores:
                update_image_meta(
                    self.state,
                    id,
                    {"original_detection_to_transformed_detection_score": score},
                )

            ground_truth_annotations = self.ground_truth_annotations.get_annotations(dataset_ids)
            scores = compute_score(
                self.context.dataset,
                {
                    "annotations": ground_truth_annotations,
                    "type": "truth",
                },
                {
                    "annotations": annotations,
                    "type": "predictions",
                },
            )
            for id, score in scores:
                update_image_meta(
                    self.state, id, {"ground_truth_to_transformed_detection_score": score}
                )

        id_to_image = {
            dataset_id_to_transformed_image_id(id): self.images.get_transformed_image(
                transform, id
            )
            for id in dataset_ids
        }

        self.on_transform(id_to_image)

        self.state.flush()  # needed cuz in async func and modifying state or else UI does not update

    def compute_predictions_original_images(self, dataset_ids):
        if not self.state.predictions_original_images_enabled:
            return

        image_id_to_image = {
            dataset_id_to_image_id(id): self.images.get_image_without_cache_eviction(id)
            for id in dataset_ids
        }
        self.predictions_original_images = self.original_detection_annotations.get_annotations(
            self.detector, image_id_to_image
        )

        ground_truth_annotations = self.ground_truth_annotations.get_annotations(dataset_ids)

        scores = compute_score(
            self.context.dataset,
            {
                "annotations": ground_truth_annotations,
                "type": "truth",
            },
            {
                "annotations": self.predictions_original_images,
                "type": "predictions",
            },
        )
        for dataset_id, score in scores:
            update_image_meta(
                self.state, dataset_id, {"original_ground_to_original_detection_score": score}
            )

    async def _update_images(self, dataset_ids):
        # load images on state for ImageList
        for id in dataset_ids:
            with self.state:
                self.images.get_stateful_image(id)
            await self.server.network_completion

        with self.state:
            self.ground_truth_annotations.get_annotations(dataset_ids)
        await self.server.network_completion

        with self.state:
            self.compute_predictions_original_images(dataset_ids)
        await self.server.network_completion

        with self.state:
            await self.update_transformed_images(dataset_ids)
        await self.server.network_completion

    def _cancel_update_images(self, **kwargs):
        if hasattr(self, "_update_task"):
            self._update_task.cancel()

    def _start_update_images(self):
        self._cancel_update_images()
        self._update_task = asynchronous.create_task(self._update_images(self.visible_dataset_ids))

    def _updating_images(self):
        return hasattr(self, "_update_task") and not self._update_task.done()

    def on_scroll(self, visible_ids):
        self.visible_dataset_ids = visible_ids
        self._start_update_images()

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
        with html.Div(classes="col"):
            self._parameters_app.transforms_ui()

    def apply_ui(self):
        with html.Div():
            self._parameters_app.transform_apply_ui()

    def dataset_widget(self):
        ImageList(self.on_scroll, self.on_hover)

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
                                            options=([],),
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


def main(server=None, *args, **kwargs):
    server = get_server(client_type="vue3")

    transforms_app = TransformsApp(server)
    transforms_app.ui

    server.start(**kwargs)


if __name__ == "__main__":
    main()
