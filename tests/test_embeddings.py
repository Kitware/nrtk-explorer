from nrtk_explorer.library import embeddings_extractor
from nrtk_explorer.library import dimension_reducers

import json
import os
import pytest
import timeit

CURRENT_DIR_NAME = os.path.dirname(__file__)
DATASET = f"{CURRENT_DIR_NAME}/../assets/OIRDS_v1_0/oirds.json"


def image_paths_impl():
    with open(DATASET) as f:
        dataset = json.load(f)
    images = dataset["images"]

    paths = list()
    for image_metadata in images:
        paths.append(os.path.join(os.path.dirname(DATASET), image_metadata["file_name"]))
    return paths


@pytest.fixture
def image_paths():
    return image_paths_impl()


def test_features_small(image_paths):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths, 10)
    assert len(features) == 10
    print(features)


def test_features_zero(image_paths):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths, 0)
    assert features is None
    print(features)


@pytest.mark.slow
def test_features_all(image_paths):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths)
    assert len(features) == len(image_paths)
    print(f"Number of features: {len(features)}")


def test_features_rand(image_paths):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths, 10, rand=True)
    assert len(features) == 10
    print(features)


def test_pca_2d(image_paths):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths, 10)
    model = dimension_reducers.PCAReducer(2)
    points = model.reduce(features)
    assert len(points) > 0
    assert len(points[0]) == 2
    print(points)


def test_pca_3d(image_paths):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths, 10)
    model = dimension_reducers.PCAReducer(3)
    points = model.reduce(features)
    assert len(points) > 0
    assert len(points[0]) == 3
    print(points)


def test_umap_2d(image_paths):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths, 10, rand=True)
    model = dimension_reducers.UMAPReducer(2)
    points = model.reduce(features)
    assert len(points) > 0
    assert len(points[0]) == 2
    print(points)


def test_umap_3d(image_paths):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths, 10, rand=True)
    model = dimension_reducers.UMAPReducer(3)
    points = model.reduce(features)
    assert len(points) > 0
    assert len(points[0]) == 3
    print(points)


def test_reducer_manager(image_paths):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths, 10)
    mgr = dimension_reducers.DimReducerManager()
    old_points = mgr.reduce(features, name="PCA", dims=3)
    assert len(old_points) > 0
    assert len(old_points[0]) == 3

    new_points = mgr.reduce(features, name="PCA", dims=3)
    assert id(old_points) == id(new_points)

    new_points_2d = mgr.reduce(features, name="PCA", dims=2)
    assert id(old_points) != id(new_points_2d)


@pytest.mark.slow
def test_features_extractor_benchmark(image_paths):
    setups = [
        (10, True, 100),
        (10, False, 100),
        (100, True, 10),
        (100, False, 10),
    ]

    extractor = embeddings_extractor.EmbeddingsExtractor()
    for n, cache, iterations in setups:
        output = timeit.timeit(
            lambda: extractor.extract(image_paths, n=n, cache=cache), number=iterations
        )
        print(
            f"Extract embeddings of {n} images cached={cache} mean(TotalExecTime)={output / iterations}s"
        )


@pytest.mark.slow
def test_reducer_manager_benchmark(image_paths):
    setups = [
        ("PCA", 10, True, 100),
        ("PCA", 10, False, 100),
        ("PCA", 100, True, 10),
        ("PCA", 100, False, 10),
        ("UMAP", 10, True, 100),
        ("UMAP", 10, False, 100),
        ("UMAP", 100, True, 10),
        ("UMAP", 100, False, 10),
    ]

    mgr = dimension_reducers.DimReducerManager()
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths)

    # Short benchmarks cached
    for name, n, cache, iterations in setups:
        output = timeit.timeit(
            lambda: mgr.reduce(features[:n], name=name, cache=cache), number=iterations
        )

        print(
            f"{name} dims reductions of {n} images cached={cache} mean(FullExecTime)={output / iterations}s"
        )


@pytest.mark.slow
def test_pca_3d_large(image_paths):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths, rand=True)
    model = dimension_reducers.PCAReducer(3)
    points = model.reduce(features)
    assert len(points) > 0
    assert len(points[0]) == 3
    print(f"Number of images: {len(points)}")
    print(points)


@pytest.mark.slow
def test_umap_3d_large(image_paths):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths, rand=True)
    model = dimension_reducers.UMAPReducer(3)
    points = model.reduce(features)
    assert len(points) > 0
    assert len(points[0]) == 3
    print(f"Number of images: {len(points)}")
    print(points)
