import logging
from collections.abc import MutableMapping

from trame.ui.quasar import QLayout
from trame.widgets import quasar
from trame.widgets import html
from trame.app import get_server, asynchronous

from nrtk_explorer.library.scoring import (
    compute_score,
)

from nrtk_explorer.app.applet import Applet
from nrtk_explorer.app.trame_utils import ProcessingStep
from nrtk_explorer.app.images.image_meta import update_image_meta, dataset_id_to_meta
from nrtk_explorer.app.trame_utils import change_checker, delete_state
from nrtk_explorer.app.images.image_ids import (
    dataset_id_to_image_id,
    dataset_id_to_transformed_image_id,
    image_id_to_score_id,
    GROUND_TRUTH_MODEL,
)
from nrtk_explorer.app.images.images import Images
from nrtk_explorer.app.images.stateful_annotations import (
    make_stateful_annotations,
)
from nrtk_explorer.app.ui import ImageList
from nrtk_explorer.app.ui.image_list import (
    ORIGINAL_COLUMNS,
    init_always_visible_columns,
    add_visible_columns,
)


IMAGE_UPDATE_BATCH_SIZE = 16

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LazyDict(MutableMapping):
    """If function provided for value, run function when value is accessed"""

    def __init__(self, *args, **kw):
        self._raw_dict = dict(*args, **kw)

    def __getitem__(self, key):
        val = self._raw_dict[key]
        return val() if callable(val) else val

    def __setitem__(self, key, value):
        self._raw_dict[key] = value

    def __delitem__(self, key):
        del self._raw_dict[key]

    def __iter__(self):
        return iter(self._raw_dict)

    def __len__(self):
        return len(self._raw_dict)

    def values(self):
        return (self[k] for k in self._raw_dict)

    def items(self):
        return ((k, self[k]) for k in self._raw_dict)


class ImagesApp(Applet):
    def __init__(
        self,
        server,
        images=None,
        ground_truth_annotations=None,
        **kwargs,
    ):
        super().__init__(server)

        self.state.setdefault("image_list_ids", [])
        self.state.setdefault("dataset_ids", [])
        self.state.setdefault("user_selected_ids", [])

        self.images = images or Images(server)

        ground_truth_annotations = ground_truth_annotations or make_stateful_annotations(
            server, GROUND_TRUTH_MODEL
        )
        self.context.ground_truth_annotations = ground_truth_annotations.annotations_factory

        def clear_transformed(*args, **kwargs):
            if self.context.models:
                for obj in self.context.models.values():
                    transformed_annotations = obj["transformed_annotations"]
                    transformed_annotations.cache_clear()

            for id in self.state.dataset_ids:
                update_image_meta(
                    self.state,
                    id,
                    {
                        "original_detection_to_transformed_detection_score": 0,
                        "ground_truth_to_transformed_detection_score": 0,
                    },
                )

        self.ctrl.apply_transform.add(clear_transformed)
        self.ctrl.run_transform.add(self._start_update_images)
        self.ctrl.start_update_images.add(self._start_update_images)
        self.ctrl.scroll_images.add(self.on_scroll)
        self.ctrl.hover_image.add(self.on_hover)

        # delete score from state of old ids that are not in new
        def delete_meta_state(old_ids, new_ids):
            if old_ids is not None:
                to_clean = set(old_ids) - set(new_ids)
                for id in to_clean:
                    delete_state(self.state, dataset_id_to_meta(id))

        change_checker(self.state, "dataset_ids")(delete_meta_state)
        # clear score when changing model
        # clear score when changing transform

        self._ui = None

        init_always_visible_columns(self.state)
        add_visible_columns(self.state, ORIGINAL_COLUMNS)

        # On annotations enabled, run whole pipeline to possibly compute transforms. Why? Transforms compute scores are based on original images
        self.annotations_enable_control = ProcessingStep(
            server,
            feature_enabled_state_key="predictions_images_enabled",
            gui_switch_key="inference_enabled_switch",
            column_name=ORIGINAL_COLUMNS[0],
            enabled_callback=self._start_update_images,
        )

        self.server.controller.on_server_ready.add(self.on_server_ready)

        self.visible_dataset_ids = []  # updated when ImageList invokes ctrl.scroll_images

    def on_server_ready(self, *args, **kwargs):
        self.state.change("current_dataset")(self._cancel_update_images)

    async def update_transformed_images(self, dataset_ids, predictions_original_images):
        if not self.state.transform_enabled:
            return

        skip_inference = False

        if not self.state.predictions_images_enabled:
            skip_inference = True

        if not self.context.models:
            skip_inference = True

        id_to_image = LazyDict()
        for id in dataset_ids:
            id_to_image[dataset_id_to_transformed_image_id(id)] = (
                lambda id=id: self.images.get_transformed_image_without_cache_eviction(id)
            )

        if not skip_inference:
            ground_truth_annotations = self.context.ground_truth_annotations.get_annotations(
                dataset_ids
            )

            for model_name, obj in self.context.models.items():
                predictor = obj["predictor"]
                transformed_annotations = obj["transformed_annotations"]

                with self.state:
                    annotations = await transformed_annotations.get_annotations(
                        predictor, id_to_image
                    )
                await self.server.network_completion

                scores = compute_score(
                    self.context.dataset,
                    ground_truth_annotations,
                    annotations,
                    self.state.confidence_score_threshold,
                )

                for dataset_id, score in scores:
                    score_id = image_id_to_score_id(
                        dataset_id_to_transformed_image_id(dataset_id), model_name
                    )
                    self.state[score_id] = score

                await self.server.network_completion

            # sortable score value may have changed which images that are in view
            self.server.controller.check_images_in_view()

        if self.ctrl.transform_applied.exists():
            self.ctrl.transform_applied(id_to_image)  # inform embeddings app

        self.state.flush()

    async def compute_predictions_original_images(self, dataset_ids):
        if not self.state.predictions_images_enabled:
            return

        if not self.context.models:
            return

        image_id_to_image = LazyDict(
            {
                dataset_id_to_image_id(
                    id
                ): lambda id=id: self.images.get_image_without_cache_eviction(id)
                for id in dataset_ids
            }
        )

        ground_truth_annotations = self.context.ground_truth_annotations.get_annotations(
            dataset_ids
        )

        predictions_original_images = {}

        for model_name, obj in self.context.models.items():
            predictor = obj["predictor"]
            original_annotations = obj["original_annotations"]

            with self.state:
                annotations = await original_annotations.get_annotations(
                    predictor, image_id_to_image
                )
            await self.server.network_completion

            predictions_original_images[model_name] = annotations

            scores = compute_score(
                self.context.dataset,
                ground_truth_annotations,
                annotations,
                self.state.confidence_score_threshold,
            )

            for dataset_id, score in scores:
                score_id = image_id_to_score_id(dataset_id_to_image_id(dataset_id), model_name)
                self.state[score_id] = score

        return predictions_original_images

    async def _update_images(self, dataset_ids, visible=False):
        if visible:
            # load images on state for ImageList
            with self.state:
                self.context.ground_truth_annotations.get_annotations(dataset_ids)
            await self.server.network_completion

        # always push to state because compute_predictions_original_images updates score metadata
        with self.state:
            predictions_original_images = await self.compute_predictions_original_images(
                dataset_ids
            )
        await self.server.network_completion
        # sortable score value may have changed which may have changed images that are in view
        self.server.controller.check_images_in_view()

        await self.update_transformed_images(dataset_ids, predictions_original_images)

    async def _batch_process_images(self, dataset_ids, visible=False):
        ids = list(dataset_ids)
        for i in range(0, len(ids), IMAGE_UPDATE_BATCH_SIZE):
            chunk = ids[i : i + IMAGE_UPDATE_BATCH_SIZE]
            await self._update_images(chunk, visible=visible)

    async def _update_all_images(self, visible_images):
        with self.state:
            self.state.updating_images = True

        await self._batch_process_images(visible_images, visible=True)

        other_images = set(self.state.user_selected_ids) - set(visible_images)
        await self._batch_process_images(other_images, visible=False)

        with self.state:
            self.state.updating_images = False

    def _cancel_update_images(self, **kwargs):
        if hasattr(self, "_update_task"):
            self._update_task.cancel()

    def _start_update_images(self, **kwargs):
        """
        After updating the images visible in the image list, all other selected
        images are updated and their scores computed. After images are scored,
        the table sort may have changed the images that are visible, so
        ImageList is asked to send visible image IDs again, which may trigger
        a new _update_all_images if the set of images in view has changed.
        """
        self._cancel_update_images()
        self._update_task = asynchronous.create_task(
            self._update_all_images(self.visible_dataset_ids)
        )

    def on_scroll(self, visible_ids):
        self.visible_dataset_ids = visible_ids
        self._start_update_images()

    def on_hover(self, id_):
        self.state.hovered_id = id_

    def dataset_widget(self):
        ImageList()

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

                            self.dataset_widget()

                self._ui = layout
        return self._ui


def main(server=None, *args, **kwargs):
    server = get_server(client_type="vue3")

    transforms_app = ImagesApp(server)
    transforms_app.ui

    server.start(**kwargs)


if __name__ == "__main__":
    main()
