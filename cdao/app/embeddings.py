from cdao.widgets.cdao import ScatterPlot
from cdao.library import embeddings
from cdao.library import imageutils

import json
import torch
import timm
import numpy as np
import umap
import cdao

from trame.widgets import quasar, html
from trame.ui.quasar import QLayout
from trame.decorators import TrameApp, change
from trame.app import get_server

import os

os.environ["TRAME_DISABLE_V3_WARNING"] = "1"


ROOT_DATASET_DIR = "/home/alessandro/Documents"
if os.environ.get("ROOT_DATASET_DIR") is not None:
    ROOT_DATASET_DIR = os.environ.get("ROOT_DATASET_DIR")

DATASET_DIRS = [
    f"{ROOT_DATASET_DIR}/OIRDS_v1_0/oirds_test.json",
    f"{ROOT_DATASET_DIR}/OIRDS_v1_0/oirds_train.json",
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
        self.dataset_loader = imageutils.DataSetLoader(current_model["value"])

    def on_run_clicked(self):
        if self.server.state.tab == "PCA":
            self.embedding_type = embeddings.PCAEmbeddings(
                self.server.state.dimensionality,
                self.server.state.pca_whiten,
                self.server.state.pca_solver,
            )

        elif self.server.state.tab == "UMAP":
            self.embedding_type = embeddings.UMAPEmbeddings(self.server.state.dimensionality)

        with open(self.server.state.current_dataset) as f:
            dataset = json.load(f)

        images = dataset["images"]

        paths = list()

        for image_metadata in images:
            paths.append(
                os.path.join(
                    os.path.dirname(self.server.state.current_dataset), image_metadata["file_name"]
                )
            )

        features = self.dataset_loader.load(paths, self.server.state.num_elements)
        self.server.state.current_points = self.embedding_type.execute(features)
        print(self.server.state.current_points)

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
                    v_model=("current_dataset", DATASET_DIRS[0]),
                    options=(DATASET_DIRS,),
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
                    max=(25,),
                    step=(1,),
                    label=True,
                    label_always=True,
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

                quasar.QBtn(label="Run", flat=True, color="Primary", click=self.on_run_clicked)

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
                    v_model=("leftDrawerOpen", True), side="left", overlay=True, elevated=True
                ):
                    self.settings_widget()

                # Main content
                with quasar.QPageContainer():
                    self.visualization_widget()

                self._ui = layout
        return self._ui


def main(server=None, *args, **kwargs):
    embbedings_app = EmbbedingsApp()
    embbedings_app.server.start(**kwargs)


if __name__ == "__main__":
    main()
