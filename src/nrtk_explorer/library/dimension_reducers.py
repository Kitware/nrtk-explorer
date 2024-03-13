import hashlib

from sklearn.decomposition import PCA


class DimReducerManager:
    def __init__(self):
        self.cached_reducers = {}
        self.cached_reductions = {}

    def reduce(self, name, fit_features, features=None, cache=True, **kwargs):
        fit_features_id = hashlib.md5(fit_features.data).hexdigest()
        reducer_id = (
            fit_features_id + ":" + name + ":" + ":".join("%s=%r" % x for x in kwargs.items())
        )

        reduction_id = reducer_id
        if features is not None:
            features_id = hashlib.md5(features.data).hexdigest()
            reduction_id = reducer_id + ":" + features_id

        if cache is False or reducer_id not in self.cached_reducers:
            reducer = None
            if name.upper() == "PCA":
                reducer = PCAReducer(**kwargs)
            elif name.upper() == "UMAP":
                reducer = UMAPReducer(**kwargs)
            else:
                raise TypeError

            # Train the model
            reducer.fit(fit_features)
            self.cached_reducers[reducer_id] = reducer

        if features is None or len(features) == 0:
            return None
        else:
            if cache is False or reduction_id not in self.cached_reductions:
                # Perform reduction without modifying the model
                self.cached_reductions[reduction_id] = self.cached_reducers[reducer_id].reduce(
                    features
                )
            return self.cached_reductions[reduction_id]


class DimReducer:
    def reduce(self, features):
        raise NotImplementedError

    def fit(self, features):
        raise NotImplementedError


class PCAReducer(DimReducer):
    def __init__(self, dims=3, whiten=False, solver="auto"):
        self._dims = dims
        self._whiten = whiten
        self._solver = solver
        self.pca = PCA(
            n_components=int(self._dims),
            whiten=self._whiten,
            svd_solver=self._solver,
        )

    def reduce(self, features):
        x = self.pca.transform(features)
        return x.tolist()

    def fit(self, features):
        self.pca.fit(features)


class UMAPReducer(DimReducer):
    def __init__(self, dims=3, **kwargs):
        import umap

        self.umap = umap.UMAP(n_components=int(dims), **kwargs)

    def reduce(self, features):
        embeddings = self.umap.transform(features)
        return embeddings.tolist()

    def fit(self, features):
        self.umap.fit(features)
