from sklearn.decomposition import PCA

import json
import torch
import numpy as np
import umap


class Embeddings:
    def __init__(self, dims=3):
        self._dimensions = dims

    @property
    def dimensions(self):
        return self.dimensions

    @dimensions.setter
    def dimensions(self, dims):
        self._dimensions = dims

    def execute(self, features):
        pass


class PCAEmbeddings(Embeddings):
    def __init__(self, dims=3, whiten=False, solver="auto"):
        self._whiten = whiten
        self._solver = solver
        super().__init__(dims)

    def execute(self, features):
        pca = PCA(
            n_components=int(self._dimensions),
            whiten=self._whiten,
            svd_solver=self._solver,
        )
        x = pca.fit_transform(features)
        return x.tolist()


class UMAPEmbeddings(Embeddings):
    def execute(self, features):
        n_neighbors = 15
        if features.shape[0] - 1 < 15:
            n_neighbors = features.shape[0] - 1

        reducer = umap.UMAP(n_components=int(self._dimensions), n_neighbors=n_neighbors)
        embeddings = reducer.fit_transform(features)
        return embeddings.tolist()
