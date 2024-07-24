from nrtk_explorer.widgets.nrtk_explorer import ScatterPlot
from nrtk_explorer.library import embeddings_extractor
from nrtk_explorer.library import dimension_reducers
from nrtk_explorer.library import images_manager
from nrtk_explorer.library.dataset import get_dataset
from nrtk_explorer.app.applet import Applet
import nrtk_explorer.test_data

import asyncio
import os

from trame.widgets import quasar, html
from trame.ui.quasar import QLayout
from trame.app import get_server, asynchronous


os.environ["TRAME_DISABLE_V3_WARNING"] = "1"

DIR_NAME = os.path.dirname(nrtk_explorer.test_data.__file__)
DATASET_DIRS = [
    f"{DIR_NAME}/OIRDS_v1_0/oirds.json",
    f"{DIR_NAME}/OIRDS_v1_0/oirds_test.json",
    f"{DIR_NAME}/OIRDS_v1_0/oirds_train.json",
]


class EmbeddingsApp(Applet):
    def __init__(self, server):
        super().__init__(server)

        self._ui = None
        self._on_select_fn = None
        self.reducer = dimension_reducers.DimReducerManager()
        self.is_standalone_app = self.server.state.parent is None
        if self.is_standalone_app:
            self.context.images_manager = images_manager.ImagesManager()

        if self.state.current_dataset is None:
            self.state.current_dataset = DATASET_DIRS[0]
        self.features = None

        self.state.client_only("camera_position")
        self.state.feature_extraction_model = "resnet50.a1_in1k"

        self.server.controller.add("on_server_ready")(self.on_server_ready)
        self.transformed_images_cache = {}

    def on_server_ready(self, *args, **kwargs):
        # Bind instance methods to state change
        self.on_current_dataset_change()
        self.on_feature_extraction_model_change()
        self.state.change("current_dataset")(self.on_current_dataset_change)
        self.state.change("feature_extraction_model")(self.on_feature_extraction_model_change)

    def on_feature_extraction_model_change(self, **kwargs):
        feature_extraction_model = self.state.feature_extraction_model
        self.extractor = embeddings_extractor.EmbeddingsExtractor(
            model_name=feature_extraction_model, manager=self.context.images_manager
        )

    def on_current_dataset_change(self, **kwargs):
        self.state.num_elements_disabled = True
        if self.context.dataset is None:
            self.context.dataset = get_dataset(self.state.current_dataset, force_reload=True)

        self.images = list(self.context.dataset.imgs.values())
        self.state.num_elements_max = len(self.images)
        self.state.num_elements_disabled = False

        if self.is_standalone_app:
            self.context.images_manager = images_manager.ImagesManager()

    def on_run_clicked(self):
        self.state.is_loading = True
        asynchronous.create_task(self.compute(self.compute_source_points))

    async def compute(self, method):
        # We need to yield twice for the is_loading=True to commit to the trame state
        # before this routine ends
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await method()
        with self.state:
            self.state.is_loading = False

    async def compute_source_points(self):
        self.features = self.extractor.extract(
            paths=self.context.paths,
            batch_size=int(self.state.model_batch_size),
        )

        if self.state.tab == "PCA":
            self.state.points_sources = self.reducer.reduce(
                name="PCA",
                fit_features=self.features,
                features=self.features,
                dims=self.state.dimensionality,
                whiten=self.state.pca_whiten,
                solver=self.state.pca_solver,
            )

        elif self.state.tab == "UMAP":
            args = {}
            if self.state.umap_random_seed:
                args["random_state"] = int(self.state.umap_random_seed_value)

            if self.state.umap_n_neighbors:
                args["n_neighbors"] = int(self.state.umap_n_neighbors_number)

            self.state.points_sources = self.reducer.reduce(
                name="UMAP",
                dims=self.state.dimensionality,
                fit_features=self.features,
                features=self.features,
                **args,
            )

        # Unselect current selection of images
        if self._on_select_fn:
            self._on_select_fn([])

        self.state.points_transformations = []
        self.state.user_selected_points_indices = []
        self.state.camera_position = []

    def on_run_transformations(self, transformed_image_ids):
        # Fillup the cache with the transformed images
        for img_id in transformed_image_ids:
            img = self.context.image_objects[img_id]
            img = self.context.images_manager.prepare_for_model(img)
            self.transformed_images_cache[img_id] = img

        transformation_features = self.extractor.extract(
            paths=transformed_image_ids,
            content=self.transformed_images_cache,
            batch_size=int(self.state.model_batch_size),
        )

        if self.state.tab == "PCA":
            self.state.points_transformations = self.reducer.reduce(
                name="PCA",
                fit_features=self.features,
                features=transformation_features,
                dims=self.state.dimensionality,
                whiten=self.state.pca_whiten,
                solver=self.state.pca_solver,
            )

        elif self.state.tab == "UMAP":
            args = {}
            if self.state.umap_random_seed:
                args["random_state"] = int(self.state.umap_random_seed_value)

            if self.state.umap_n_neighbors:
                args["n_neighbors"] = int(self.state.umap_n_neighbors_number)

            self.state.points_transformations = self.reducer.reduce(
                name="UMAP",
                dims=self.state.dimensionality,
                fit_features=self.features,
                features=transformation_features,
                **args,
            )

    def set_on_select(self, fn):
        self._on_select_fn = fn

    def on_select(self, indices):
        # remap transformed indices to original indices
        original_indices = set()
        for point_index in indices:
            original_image_point_index = point_index
            if point_index >= len(self.state.points_sources):
                original_image_point_index = self.state.user_selected_points_indices[
                    point_index - len(self.state.points_sources)
                ]
            original_indices.add(original_image_point_index)
        original_indices = list(original_indices)

        self.state.user_selected_points_indices = original_indices
        self.state.points_transformations = []
        ids = [self.state.images_ids[i] for i in original_indices]
        if self._on_select_fn:
            self._on_select_fn(ids)

    def on_move(self, camera_position):
        self.state.camera_position = camera_position

    def set_on_hover(self, fn):
        self._on_hover_fn = fn

    def on_point_hover(self, point_index):
        self.state.highlighted_point = point_index
        image_id = ""
        if point_index is not None:
            original_image_point_index = point_index
            if point_index >= len(self.state.points_sources):
                image_kind = "transformed_img_"
                original_image_point_index = self.state.user_selected_points_indices[
                    point_index - len(self.state.points_sources)
                ]
            else:
                image_kind = "img_"
            dataset_id = self.state.images_ids[original_image_point_index]
            image_id = f"{image_kind}{dataset_id}"

        if self._on_hover_fn:
            self._on_hover_fn(image_id)

    def on_image_hovered(self, id_):
        # If the point is in the list of selected points, we set it as the highlighted point
        is_transformation = id_.startswith("transformed_img_")
        try:
            dataset_id = int(id_.split("_")[-1])  # img_123 or transformed_img_123 -> 123
        except ValueError:
            # id_ probably is an empty string
            dataset_id = id_
        if dataset_id in self.state.images_ids:
            index = self.state.images_ids.index(dataset_id)
            if is_transformation:
                index_selected = self.state.user_selected_points_indices.index(index)
                self.state.highlighted_point = len(self.state.points_sources) + index_selected
            else:
                self.state.highlighted_point = index
        else:
            # If the point is not in the list of selected points, we set it to a negative point
            self.state.highlighted_point = -1

    def visualization_widget(self):
        ScatterPlot(
            cameraMove="camera_position=$event",
            cameraPosition=("camera_position",),
            highlightedPoint=("highlighted_point", -1),
            hover=(self.on_point_hover, "[$event]"),
            points=("points_sources", []),
            transformedPoints=("points_transformations", []),
            select=(self.on_select, "[$event]"),
            selectedPoints=("user_selected_points_indices", []),
        )

    def settings_widget(self):
        with html.Div(trame_server=self.server, classes="col"):
            with html.Div(classes="q-gutter-y-md"):
                quasar.QBtnToggle(
                    v_model=("dimensionality", "3"),
                    toggler_color="primary",
                    flat=True,
                    spread=True,
                    options=(
                        [
                            {"label": "2D", "value": "2"},
                            {"label": "3D", "value": "3"},
                        ],
                    ),
                )

            quasar.QSelect(
                label="Embeddings Model",
                v_model=("feature_extraction_model",),
                options=(
                    [
                        {"label": "ResNet50", "value": "resnet50.a1_in1k"},
                        {"label": "EfficientNet_b0", "value": "efficientnet_b0.ra_in1k"},
                        {
                            "label": "MobileNetV3Large",
                            "value": "mobilenetv3_large_100.ra_in1k",
                        },
                    ],
                ),
                filled=True,
                emit_value=True,
                map_options=True,
            )
            quasar.QInput(
                v_model=("model_batch_size", 32),
                filled=True,
                stack_label=True,
                label="Batch Size",
                type="number",
            )

        with html.Div(classes="col"):
            with quasar.QTabs(
                v_model=("tab", "PCA"),
                dense=True,
                narrow_indicator=True,
                active_color="primary",
                indicator_color="primary",
                align="justify",
            ):
                quasar.QTab(name="PCA", label="pca")
                quasar.QTab(name="UMAP", label="umap")
            quasar.QSeparator()
            with quasar.QTabPanels(v_model=("tab", "PCA")):
                with quasar.QTabPanel(name="PCA"):
                    quasar.QToggle(
                        v_model=("pca_whiten", False),
                        label="Whiten",
                        left_label=True,
                    )
                    quasar.QSelect(
                        v_model=("pca_solver", "auto"),
                        label="SVD Solver",
                        toggler_color="primary",
                        options=(
                            [
                                "auto",
                                "full",
                                "arpack",
                                "randomized",
                            ],
                        ),
                    )

                with quasar.QTabPanel(name="UMAP"):
                    quasar.QToggle(
                        v_model=("umap_n_neighbors", False),
                        label="Number of neighbors",
                        left_label=True,
                    )
                    quasar.QInput(
                        v_model=("umap_n_neighbors_number", 15),
                        disable=("!umap_n_neighbors",),
                        filled=True,
                        stack_label=True,
                        label="Neighbors amount",
                        type="number",
                    )
                    quasar.QToggle(
                        v_model=("umap_random_seed", True),
                        label="Random seed",
                        left_label=True,
                    )
                    quasar.QInput(
                        v_model=("umap_random_seed_value", 1),
                        disable=("!umap_random_seed",),
                        filled=True,
                        stack_label=True,
                        label="Seed value",
                        type="number",
                    )

    def compute_ui(self):
        with html.Div(trame_server=self.server):
            quasar.QBtn(
                label="Compute",
                loading=("is_loading", False),
                click=self.on_run_clicked,
                flat=True,
            )

    # This is only used within when this module (file) is executed as an Standalone app.
    @property
    def ui(self):
        if self._ui is None:
            with QLayout(self.server) as layout:
                with quasar.QHeader():
                    with quasar.QToolbar(classes="shadow-4"):
                        quasar.QToolbarTitle("Embeddings")
                        quasar.QBtn("Reset")

                with quasar.QDrawer(
                    v_model=("leftDrawerOpen", True),
                    side="left",
                    elevated=True,
                ):
                    with html.Div(classes="column justify-center", style="padding:1rem"):
                        with html.Div(classes="col"):
                            quasar.QSeparator()
                            quasar.QSelect(
                                label="Dataset",
                                v_model=("current_dataset",),
                                options=(
                                    [
                                        {"label": "oirds_test", "value": DATASET_DIRS[0]},
                                        {"label": "oirds_train", "value": DATASET_DIRS[1]},
                                    ],
                                ),
                                filled=True,
                                emit_value=True,
                                map_options=True,
                            )
                    self.settings_widget()
                    self.compute_ui()

                # Main content
                with quasar.QPageContainer():
                    with quasar.QPage():
                        with html.Div(classes="row", style="min-height: inherit;"):
                            with html.Div(classes="col q-pa-md"):
                                self.visualization_widget()

                self._ui = layout
        return self._ui


def embeddings(server=None, *args, **kwargs):
    server = get_server()
    server.client_type = "vue3"

    embeddings_app = EmbeddingsApp(server)
    embeddings_app.ui

    server.start(**kwargs)


if __name__ == "__main__":
    embeddings()
