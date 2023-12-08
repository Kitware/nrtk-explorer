from nrtk_explorer.widgets.nrtk_explorer import ScatterPlot
from nrtk_explorer.library import embeddings_extractor
from nrtk_explorer.library import dimension_reducers
from nrtk_explorer.library import images_manager
from nrtk_explorer.app.applet import Applet

import json

from trame.widgets import quasar, html
from trame.ui.quasar import QLayout
from trame.app import get_server

import os

os.environ["TRAME_DISABLE_V3_WARNING"] = "1"

DIR_NAME = os.path.dirname(__file__)
DATASET_DIRS = [
    f"{DIR_NAME}/../../assets/OIRDS_v1_0/oirds.json",
    f"{DIR_NAME}/../../assets/OIRDS_v1_0/oirds_test.json",
    f"{DIR_NAME}/../../assets/OIRDS_v1_0/oirds_train.json",
]


def on_click(*args, **kwargs):
    pass


def on_select(*args, **kwargs):
    pass


class EmbeddingsApp(Applet):
    def __init__(
        self,
        server,
        state_translator=None,
        controller_translator=None,
        local_state_translator=None,
    ):
        super().__init__(server, state_translator, controller_translator, local_state_translator)

        self._ui = None

        self.state.tab = "PCA"
        self._on_select_fn = None
        self.reducer = dimension_reducers.DimReducerManager()
        self.is_standalone_app = state_translator is None
        if self.is_standalone_app:
            self.local_state["images_manager"] = images_manager.ImagesManager()

        if self.state.current_dataset is None:
            self.state.current_dataset = DATASET_DIRS[0]

        self.state.change("current_dataset")(self.on_current_dataset_change)
        self.state.change("current_model")(self.on_current_model_change)

        self.state.current_source_points = []
        self.state.current_transform_points = []

    def on_current_model_change(self, **kwargs):
        current_model = self.state.current_model
        self.extractor = embeddings_extractor.EmbeddingsExtractor(
            current_model, self.local_state["images_manager"]
        )

    def on_current_dataset_change(self, **kwargs):
        self.state.num_elements_disabled = True
        with open(self.state.current_dataset) as f:
            dataset = json.load(f)
            self.images = dataset["images"]
            self.state.num_elements_max = len(self.images)
        self.state.num_elements_disabled = False

        if self.is_standalone_app:
            self.local_state["images_manager"] = images_manager.ImagesManager()

    def on_run_clicked(self):
        paths = list()
        for image_metadata in self.images:
            paths.append(
                os.path.join(
                    os.path.dirname(self.state.current_dataset),
                    image_metadata["file_name"],
                )
            )

        self.state.run_button_loading = True
        features = self.extractor.extract(
            paths=paths, n=self.state.num_elements, rand=self.state.random_sampling
        )
        if self.state.tab == "PCA":
            self.state.current_source_points = self.reducer.reduce(
                features,
                name="PCA",
                dims=self.state.dimensionality,
                whiten=self.state.pca_whiten,
                solver=self.state.pca_solver,
            )

        elif self.state.tab == "UMAP":
            self.state.current_source_points = self.reducer.reduce(
                features, name="UMAP", dims=self.state.dimensionality
            )
        self.state.run_button_loading = False

    def on_run_transformations(self, transformed_image_ids):
        extractor_transform = embeddings_extractor.EmbeddingsExtractor(
            self.state.current_model, self.local_state["images_manager"]
        )

        features = extractor_transform.extract(
            paths=transformed_image_ids,
            n=self.state.num_elements,
            rand=self.state.random_sampling,
            content=self.local_state["image_objects"],
        )

        if self.state.tab == "PCA":
            self.state.current_transform_points = self.reducer.reduce(
                features,
                name="PCA",
                dims=self.state.dimensionality,
                whiten=self.state.pca_whiten,
                solver=self.state.pca_solver,
            )

        elif self.state.tab == "UMAP":
            self.state.current_transform_points = self.reducer.reduce(
                features, name="UMAP", dims=self.state.dimensionality
            )

    def set_on_select(self, fn):
        self._on_select_fn = fn

    def on_select(self, ids):
        if self._on_select_fn:
            self._on_select_fn(ids)

    def visualization_widget(self):
        ScatterPlot(
            points=("get('current_source_points')",),
            click=(on_click, "[$event]"),
            select=(self.on_select, "[$event]"),
        )

    def visualization_widget_transformation(self):
        ScatterPlot(
            points=("get('current_transform_points')",),
            click=(on_click, "[$event]"),
            select=(self.on_select, "[$event]"),
        )

    def settings_widget(self):
        with html.Div(classes="column justify-center", style="padding:1rem"):
            with html.Div(classes="col"):
                quasar.QSelect(
                    label="Embeddings Model",
                    v_model=(self.state_translator("current_model"), "resnet50.a1_in1k"),
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
                quasar.QSeparator(inset=True)
                html.P("Number of elements:", classes="text-body2")
                quasar.QSlider(
                    v_model=(self.state_translator("num_elements"), 15),
                    min=(0,),
                    max=(self.state_translator("num_elements_max"), 25),
                    disable=(self.state_translator("num_elements_disabled"), True),
                    step=(1,),
                    label=True,
                    label_always=True,
                )
                quasar.QToggle(
                    v_model=(self.state_translator("random_sampling"), False),
                    label="Random selection",
                    left_label=True,
                )

                html.P("Dimensionality:", classes="text-body2")
                with html.Div(classes="q-gutter-y-md"):
                    quasar.QBtnToggle(
                        v_model=(self.state_translator("dimensionality"), "3"),
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
            with html.Div(classes="col"):
                html.P("Method:", classes="text-body2")
                with quasar.QTabs(
                    v_model="tab",
                    dense=True,
                    narrow_indicator=True,
                    active_color="primary",
                    indicator_color="primary",
                    align="justify",
                ):
                    quasar.QTab(name="PCA", label="pca")
                    quasar.QTab(name="UMAP", label="umap")
                quasar.QSeparator()
                with quasar.QTabPanels(v_model="tab"):
                    with quasar.QTabPanel(name="PCA"):
                        quasar.QToggle(
                            v_model=(self.state_translator("pca_whiten"), False),
                            label="Whiten",
                            left_label=True,
                        )
                        quasar.QSelect(
                            v_model=(self.state_translator("pca_solver"), "auto"),
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
                        with html.Div(classes="row"):
                            html.Div(classes="col-md-auto")

                quasar.QBtn(
                    label="Run",
                    color="red",
                    loading=("run_button_loading", False),
                    click=self.on_run_clicked,
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
                    v_model=(self.state_translator("leftDrawerOpen"), True),
                    side="left",
                    elevated=True,
                ):
                    with html.Div(classes="column justify-center", style="padding:1rem"):
                        with html.Div(classes="col"):
                            quasar.QSeparator()
                            quasar.QSelect(
                                label="Dataset",
                                v_model=(self.state_translator("current_dataset"),),
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
