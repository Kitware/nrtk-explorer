r"""
Define your classes and create the instances that you need to expose
"""

import logging
from typing import Dict
from PIL.Image import Image

from trame.ui.quasar import QLayout
from trame.widgets import quasar
from trame.widgets import html
from trame.app import get_server, asynchronous

import nrtk_explorer.library.transforms as trans
import nrtk_explorer.library.nrtk_transforms as nrtk_trans
from nrtk_explorer.library import object_detector
from nrtk_explorer.app.ui import ImageList
from nrtk_explorer.app.applet import Applet
from nrtk_explorer.app.parameters import ParametersApp
from nrtk_explorer.app.images.image_meta import (
    update_image_meta,
)
from nrtk_explorer.library.coco_utils import (
    convert_from_ground_truth_to_first_arg,
    convert_from_ground_truth_to_second_arg,
    convert_from_predictions_to_second_arg,
    convert_from_predictions_to_first_arg,
    compute_score,
)
from nrtk_explorer.app.trame_utils import SetStateAsync, change_checker
from nrtk_explorer.app.images.image_ids import (
    dataset_id_to_image_id,
    dataset_id_to_transformed_image_id,
)
from nrtk_explorer.library.dataset import get_dataset
from nrtk_explorer.app.images.images import (
    get_image,
    get_transformed_image,
    get_annotations,
    get_ground_truth_annotations,
)

import nrtk_explorer.app.images.image_server  # noqa module level side effects


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TransformsApp(Applet):
    def __init__(self, server):
        super().__init__(server)

        self._parameters_app = ParametersApp(
            server=server,
        )

        self._ui = None

        self._on_transform_fn = None

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

        self.state.transforms = [k for k in self._transforms.keys()]
        self.state.current_transform = self.state.transforms[0]

        # Transform enabled control ##
        self.state.transform_enabled = True

        def update_transform_enabled(**kwargs):
            self.state.transform_enabled = "transformed" in self.state.visible_columns

        self.state.change("visible_columns")(update_transform_enabled)

        def transform_became_enabled(old, new):
            return not old and new

        change_checker(self.state, "transform_enabled", transform_became_enabled)(
            self.schedule_transformed_images
        )
        # end Transform enabled control ##

        self.server.controller.add("on_server_ready")(self.on_server_ready)
        self.server.controller.apply_transform.add(self.schedule_transformed_images)
        self._on_hover_fn = None

    @property
    def get_image_fpath(self):
        return self.server.controller.get_image_fpath

    def on_server_ready(self, *args, **kwargs):
        self.state.change("object_detection_model")(self.on_object_detection_model_change)
        self.on_object_detection_model_change(self.state.object_detection_model)
        self.state.change("current_dataset")(self.reset_detector)

    def on_object_detection_model_change(self, model_name, **kwargs):
        self.detector = object_detector.ObjectDetector(model_name=model_name)
        # TODO clear detection results and rerun detection

    def reset_detector(self, **kwargs):
        self.detector.reset()

    def set_on_transform(self, fn):
        self._on_transform_fn = fn

    def on_transform(self, *args, **kwargs):
        if self._on_transform_fn:
            self._on_transform_fn(*args, **kwargs)

    def schedule_transformed_images(self, *args, **kwargs):
        logger.debug("schedule_transformed_images")
        if self._updating_images():
            if self._updating_transformed_images:
                # computing stale transformed images, restart task
                self._update_task.cancel()
            else:
                return  # update_images will call update_transformed_images() at the end
        self._update_task = asynchronous.create_task(
            self.update_transformed_images(self.visible_ids)
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

        transform = self._transforms[self.state.current_transform]

        id_to_matching_size_img = {}
        for id in dataset_ids:
            async with SetStateAsync(self.state):
                transformed = get_transformed_image(transform, id)
                id_to_matching_size_img[dataset_id_to_transformed_image_id(id)] = transformed

        async with SetStateAsync(self.state):
            annotations = self.compute_annotations(id_to_matching_size_img)

        predictions = convert_from_predictions_to_second_arg(annotations)
        scores = compute_score(
            dataset_ids,
            self.predictions_source_images,
            predictions,
        )
        for id, score in scores:
            update_image_meta(
                self.state,
                id,
                {"original_detection_to_transformed_detection_score": score},
            )

        ground_truth_annotations = get_ground_truth_annotations(dataset_ids)
        ground_truth_predictions = convert_from_ground_truth_to_first_arg(ground_truth_annotations)
        scores = compute_score(
            dataset_ids,
            ground_truth_predictions,
            predictions,
        )
        for id, score in scores:
            update_image_meta(
                self.state, id, {"ground_truth_to_transformed_detection_score": score}
            )

        id_to_image = {
            dataset_id_to_transformed_image_id(id): get_transformed_image(transform, id)
            for id in dataset_ids
        }

        self.on_transform(id_to_image)

        self.state.flush()  # needed cuz in async func and modifying state or else UI does not update

    def compute_annotations(self, id_to_image: Dict[str, Image]):
        """Compute annotations for the given image ids using the object detector model."""
        return get_annotations(self.detector, id_to_image)

    def compute_predictions_source_images(self, dataset_ids):
        image_id_to_image = {dataset_id_to_image_id(id): get_image(id) for id in dataset_ids}
        annotations = self.compute_annotations(image_id_to_image)
        dataset = get_dataset(self.state.current_dataset)
        self.predictions_source_images = convert_from_predictions_to_first_arg(
            annotations,
            dataset,
            dataset_ids,
        )

        ground_truth_annotations = get_ground_truth_annotations(dataset_ids)
        ground_truth_predictions = convert_from_ground_truth_to_second_arg(
            ground_truth_annotations, self.context.dataset
        )
        scores = compute_score(
            dataset_ids,
            self.predictions_source_images,
            ground_truth_predictions,
        )
        for dataset_id, score in scores:
            update_image_meta(
                self.state, dataset_id, {"original_ground_to_original_detection_score": score}
            )

    async def _update_images(self, dataset_ids):
        async with SetStateAsync(self.state):
            get_ground_truth_annotations(dataset_ids)  # updates state

        async with SetStateAsync(self.state):
            self.compute_predictions_source_images(dataset_ids)

        async with SetStateAsync(self.state):
            await self.update_transformed_images(dataset_ids)

    def _start_update_images(self, priority_ids):
        if hasattr(self, "_update_task"):
            self._update_task.cancel()
        self._update_task = asynchronous.create_task(self._update_images(priority_ids))

    def _updating_images(self):
        return hasattr(self, "_update_task") and not self._update_task.done()

    def on_scroll(self, visible_ids):
        self.visible_ids = visible_ids
        self._start_update_images(self.visible_ids)

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


def transforms(server=None, *args, **kwargs):
    server = get_server()
    server.client_type = "vue3"

    transforms_app = TransformsApp(server)
    transforms_app.ui

    server.start(**kwargs)


if __name__ == "__main__":
    transforms()
