from cdao.widgets.cdao import ScatterPlot
from cdao.library import embeddings_extractor
from cdao.library import dimension_reducers

import json

from trame.widgets import quasar, html
from trame.ui.quasar import QLayout
from trame.decorators import TrameApp, change
from trame.app import get_server

import os

os.environ["TRAME_DISABLE_V3_WARNING"] = "1"

DIR_NAME = os.path.dirname(__file__)
DATASET_DIRS = [
    f"{DIR_NAME}/../../assets/OIRDS_v1_0/oirds_test.json",
    f"{DIR_NAME}/../../assets/OIRDS_v1_0/oirds_train.json",
]


def on_click(*args, **kwargs):
    print("ON CLICK", args, kwargs)


def on_select(*args, **kwargs):
    print("ON SELECT", args, kwargs)


@TrameApp()
class EmbbedingsApp:
    def __init__(self, name=None):
        self.server = get_server(name)
        self.server.client_type = "vue3"
        self._ui = None
        self.server.state.tab = "PCA"
        self.server.state.current_points = []
        self.ui

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller

    @change("current_model")
    def on_current_model_change(self, current_model, **kwargs):
        self.extractor = embeddings_extractor.EmbeddingsExtractor(current_model["value"])

    @change("current_dataset")
    def on_current_dataset_change(self, current_dataset, **kwargs):
        self.server.state.num_elements_disabled = True
        with open(self.server.state.current_dataset["value"]) as f:
            dataset = json.load(f)
            self.images = dataset["images"]
            self.server.state.num_elements_max = len(self.images)
        self.server.state.num_elements_disabled = False

    def on_run_clicked(self):
        if self.server.state.tab == "PCA":
            self.reducer = dimension_reducers.PCAReducer(
                self.server.state.dimensionality,
                self.server.state.pca_whiten,
                self.server.state.pca_solver,
            )

        elif self.server.state.tab == "UMAP":
            self.reducer = dimension_reducers.UMAPReducer(self.server.state.dimensionality)

        paths = list()

        for image_metadata in self.images:
            paths.append(
                os.path.join(
                    os.path.dirname(self.server.state.current_dataset["value"]),
                    image_metadata["file_name"],
                )
            )

        self.server.state.run_button_loading = True
        features = self.extractor.extract(
            paths=paths, n=self.server.state.num_elements, rand=self.server.state.random_sampling
        )
        self.server.state.current_points = self.reducer.reduce(features)
        self.server.state.run_button_loading = False

    def visualization_widget(self):
        ScatterPlot(
            points=("get('current_points')",),
            click=(on_click, "[$event]"),
            select=(on_select, "[$event]"),
        )

    def settings_widget(self):
        with html.Div(classes="column justify-center", style="padding:1rem"):
            with html.Div(classes="col"):
                quasar.QSeparator()
                quasar.QSelect(
                    label="Dataset",
                    v_model=("current_dataset", {"label": "oirds_test", "value": DATASET_DIRS[0]}),
                    options=(
                        "Path",
                        [
                            {"label": "oirds_test", "value": DATASET_DIRS[0]},
                            {"label": "oirds_train", "value": DATASET_DIRS[1]},
                        ],
                    ),
                    filled=True,
                )
            with html.Div(classes="col"):
                quasar.QSelect(
                    label="Model",
                    v_model=("current_model", {"label": "ResNet50", "value": "resnet50"}),
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
                )
                quasar.QSeparator(inset=True)
                html.P("Number of elements:", classes="text-body2")
                quasar.QSlider(
                    v_model=("num_elements", 15),
                    min=(0,),
                    max=("num_elements_max", 25),
                    disable=("num_elements_disabled", True),
                    step=(1,),
                    label=True,
                    label_always=True,
                )
                quasar.QToggle(
                    v_model=("random_sampling", True), label="Random selection", left_label=True
                )

                html.P("Dimensionality:", classes="text-body2")
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
                            v_model=("pca_whiten", False), label="Whiten", left_label=True
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

                with quasar.QDrawer(v_model=("leftDrawerOpen", True), side="left", elevated=True):
                    self.settings_widget()

                # Main content
                with quasar.QPageContainer():
                    with quasar.QPage():
                        with html.Div(classes="row", style="min-height: inherit;"):
                            with html.Div(classes="col q-pa-md"):
                                self.visualization_widget()

                self._ui = layout
        return self._ui


def main(server=None, *args, **kwargs):
    embbedings_app = EmbbedingsApp()
    embbedings_app.server.start(**kwargs)


if __name__ == "__main__":
    main()
