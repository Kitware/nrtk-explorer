import os
os.environ["TRAME_DISABLE_V3_WARNING"] = "1"

from trame.app import get_server
from trame.decorators import TrameApp, change
from trame.ui.quasar import QLayout
from trame.widgets import quasar, matplotlib, html

import numpy as np
import timm
import torch
import json

from PIL import Image as ImageModule
from PIL.Image import Image
from sklearn.decomposition import PCA


DATASET_DIRS = [
    "/tmp/OIRDS_v1_0/oirds_test.json",
    "/tmp/OIRDS_v1_0/oirds_train.json",
]

class Embeddings:
    def __init__(self, dims=3, model='resnet50d'):
        self._dimensions = dims
        self._model = timm.create_model(model, pretrained=True)
        for param in self._model.parameters():
            param.requires_grad = False

    @property
    def dimensions(self):
        return self.dimensions

    @dimensions.setter
    def dimensions(self, dims):
        self._dimensions = dims

    def make_tensor_from_img(self, path):
        img = ImageModule.open(path)
        img = img.resize((224, 224))
        img = img.convert("RGB")
        img_tensor = torch.as_tensor(np.array(img, dtype=np.float32)).transpose(2,0)[None]
        return img_tensor

    def extract_features(self, img):
        fs = self._model.forward_features(img)
        _, nx, ny, nz = fs.shape
        img_features = fs.reshape(_*nx,ny*nz)
        return img_features

    def execute_from_path(self, img_path):
        tensor = self.make_tensor_from_img(img_path)
        features = self.extract_features(tensor)
        return self.execute(features)

    def execute(self, features):
        pass

class PCAEmbeddings(Embeddings):
    def execute(self, features):
       pca = PCA(n_components=int(self._dimensions))
       x = pca.fit(features)
       return x.singular_values_

class UMAPEmbeddings(Embeddings):
    def execute(self, features):
        pass

@TrameApp()
class EmbbedingsApp:
    def __init__(self, name=None):
        self.server = get_server(name)
        self.server.client_type = "vue3"
        self._ui = None
        self.server.state.tab = "PCA"
        self.server.state.num_elements = "5"
        self.server.state.pca_dimensionality = "3"
        self.server.state.umap_dimensionality = "3"
        self.server.state.pca_mean_variance = 3
        self.server.state.current_model = "resnet50d"
        self.server.state.current_visualization_txt = "Wait for settings"
        self.server.state.current_dataset = DATASET_DIRS[0]

        self.ui

    @property
    def state(self):
        return self.server.state

    @property
    def ctrl(self):
        return self.server.controller


    def on_current_run_model_change(self):
        if self.server.state.tab == "PCA":
            self.embedding_type = PCAEmbeddings(
                    self.server.state.pca_dimensionality,
                    self.server.state.current_model)

        elif self.server.state.tab == "UMAP":
            self.embedding_type = UMAPEmbeddings(
                    self.server.state.pca_dimensionality,
                    self.server.state.current_model)

        with open(self.server.state.current_dataset) as f:
            dataset = json.load(f)

        images = dataset["images"][:int(self.server.state.num_elements)]
        
        X = [ ]
        for image_metadata in images:
            X.append(self.embedding_type.execute_from_path("/tmp/OIRDS_v1_0/" + image_metadata["file_name"]))

        output = [str(x) for x in X]
        
        self.server.state.current_visualization_txt = f"{output}"

    def visualization_widget(self):
        html.H5(v_text="current_visualization_txt", classes="text-h5")

    def settings_widget(self):
        with html.Div(classes="column"):
            with html.Div(classes="col justify-start"):
                quasar.QSeparator()
                html.P("Input file path:", classes="text-h6")
                quasar.QSelect(
                    label="Dataset",
                    v_model=("current_dataset",),
                    options=(DATASET_DIRS,),
                    filled=True,
                )
                quasar.QSelect(
                    label="Model",
                    v_model=("current_model",),
                    options=("resnet50d",),
                    filled=True,
                )
                html.P("Number of elements:", classes="text-h6")
                quasar.QSlider(v_model="num_elements", min=0, max=25, step=1,
                               label=True, label_always=True)
                quasar.QSeparator()
                quasar.QSeparator()
            with html.Div(classes="col justify-end"):
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
                         with html.Div(classes="row"):
                             with html.Div(classes="col-md-auto"):
                                 html.P("Dimensions", classes="text-body1 ")
                             with html.Div(classes="col-md-auto"):
                                 quasar.QRadio(v_model="pca_dimensionality", val="2", label="2D")
                                 quasar.QRadio(v_model="pca_dimensionality", val="3", label="3D")
                         html.P("Mean Variance:", classes="tex-h6")
                         quasar.QSlider(v_model="pca_mean_variance", min=0.0,
                                        max=3.0, step=0.1, label=True, label_always=True)

                     with quasar.QTabPanel(name="UMAP"):
                         with html.Div(classes="row"):
                             with html.Div(classes="col-md-auto"):
                                 html.P("Dimensions", classes="text-body1 ")
                             with html.Div(classes="col-md-auto"):
                                 quasar.QRadio(v_model="umap_dimensionality", val="2", label="2D")
                                 quasar.QRadio(v_model="umap_dimensionality", val="3", label="3D")

                quasar.QBtn(label="Run", flat=True, color="Primary",
                            click=self.on_current_run_model_change)

    # This is only used within when this module (file) is executed as an Standalone app.
    @property
    def ui(self):
        if self._ui is None:
            with QLayout(self.server) as layout:
                with quasar.QHeader():
                    with quasar.QToolbar(classes="shadow-4"):
                        quasar.QToolbarTitle("Embeddings")
                        quasar.QBtn("Reset")

                # Main content
                with quasar.QPageContainer():
                    with html.Div(classes="row"):
                        with html.Div(classes="col-2 q-pa-md"):
                            self.settings_widget()

                        with html.Div(classes="col-5 q-pa-md"):
                            self.visualization_widget()

                self._ui = layout
        return self._ui

def main(server=None, *args, **kwargs):
    embbedings_app= EmbbedingsApp()
    embbedings_app.server.start(**kwargs)

if __name__ == "__main__":
    main()
