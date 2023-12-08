from sklearn.decomposition import PCA

import numpy as np
import umap
import hashlib
import time


class DimReducerManager:
    def __init__(self):
        self.cached_reductions = {}

    def reduce(self, features, name, cache=True, **kwargs):
        features_id = hashlib.md5(features.data).hexdigest()
        reduction_id = (
            features_id + ":" + name + ":" + ":".join("%s=%r" % x for x in kwargs.items())
        )

        if cache == False or reduction_id not in self.cached_reductions:
            reducer = None
            if name.upper() == "PCA":
                reducer = PCAReducer(**kwargs)
            elif name.upper() == "UMAP":
                reducer = UMAPReducer(**kwargs)
            else:
                raise TypeError

            self.cached_reductions[reduction_id] = reducer.reduce(features)

        return self.cached_reductions[reduction_id]


class DimReducer:
    def reduce(self, features):
        raise NotImplementedError


class PCAReducer(DimReducer):
    def __init__(self, dims=3, whiten=False, solver="auto"):
        self._dims = dims
        self._whiten = whiten
        self._solver = solver

    def reduce(self, features):
        pca = PCA(
            n_components=int(self._dims),
            whiten=self._whiten,
            svd_solver=self._solver,
        )
        x = pca.fit_transform(features)
        return x.tolist()


class UMAPReducer(DimReducer):
    def __init__(self, dims=3):
        self._dims = dims

    def reduce(self, features):
        n_neighbors = 15
        if features.shape[0] - 1 < 15:
            n_neighbors = features.shape[0] - 1

        reducer = umap.UMAP(n_components=int(self._dims), n_neighbors=n_neighbors)
        embeddings = reducer.fit_transform(features)
        return embeddings.tolist()
