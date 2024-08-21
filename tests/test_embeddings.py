from nrtk_explorer.library import embeddings_extractor
from nrtk_explorer.library import dimension_reducers
from nrtk_explorer.library.dataset import get_dataset
import nrtk_explorer.test_data

from PIL import Image
from tabulate import tabulate
from itertools import product
from pathlib import Path

import os
import pytest
import timeit

CURRENT_DIR_NAME = os.path.dirname(nrtk_explorer.test_data.__file__)
inc_ds_path = Path(f"{CURRENT_DIR_NAME}/coco-od-2017/test_val2017.json")


def images_impl(file_name):
    dataset = get_dataset(file_name)
    images = dataset.imgs.values()

    paths = list()
    for image_metadata in images:
        paths.append(os.path.join(os.path.dirname(file_name), image_metadata["file_name"]))

    return [Image.open(path) for path in paths]


@pytest.fixture
def images(request):
    return images_impl(inc_ds_path)


@pytest.fixture
def images_external(request):
    return images_impl(request.config.getoption("--benchmark-dataset-file"))


def test_features_small(images):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(images[:10])
    assert len(features) == 10
    print(features)


def test_features_zero(images):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract([])
    assert len(features) == 0
    print(features)


@pytest.mark.benchmark
def test_features_all(images_external):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(images_external)
    assert len(features) == len(images_external)
    print(f"Number of features: {len(features)}")


def test_pca_2d(images):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(images[:10])
    model = dimension_reducers.PCAReducer(2)
    points = model.fit(features)
    points = model.reduce(features)
    assert len(points) > 0
    assert len(points[0]) == 2
    print(points)


def test_pca_3d(images):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(images[:10])
    model = dimension_reducers.PCAReducer(3)
    points = model.fit(features)
    points = model.reduce(features)
    assert len(points) > 0
    assert len(points[0]) == 3
    print(points)


def test_umap_2d(images):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(images[:10])
    model = dimension_reducers.UMAPReducer(2, n_neighbors=8)
    points = model.fit(features)
    points = model.reduce(features)
    assert len(points) > 0
    assert len(points[0]) == 2
    print(points)


def test_umap_3d(images):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(images[:10])
    model = dimension_reducers.UMAPReducer(3, n_neighbors=8)
    points = model.fit(features)
    points = model.reduce(features)
    assert len(points) > 0
    assert len(points[0]) == 3
    print(points)


def test_reducer_manager(images):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(images[:10])
    mgr = dimension_reducers.DimReducerManager()
    old_points = mgr.reduce(fit_features=features, features=features, name="PCA", dims=3)
    assert len(old_points) > 0
    assert len(old_points[0]) == 3

    new_points = mgr.reduce(fit_features=features, features=features, name="PCA", dims=3)
    assert id(old_points) == id(new_points)

    new_points_2d = mgr.reduce(fit_features=features, features=features, name="PCA", dims=2)
    assert id(old_points) != id(new_points_2d)


@pytest.mark.benchmark
def test_features_extractor_benchmark(images_external):
    repetitions = 3
    sampling = [10, 100]
    batch_size = [1, 8, 16, 32]
    setups = list(product(sampling, batch_size))
    setups.append([500, 1])
    setups.append([500, 64])
    table = list()

    for n, batch_size in setups:
        extractor = embeddings_extractor.EmbeddingsExtractor()
        output = timeit.repeat(
            stmt=lambda: extractor.extract(images_external[:n], batch_size=batch_size),
            number=repetitions,
            repeat=5,
        )
        table.append([n, batch_size, min(output) / 10 / n])

    print(tabulate(table, headers=["#Samples", "batch_size", "ExecTime(sec)"], tablefmt="github"))


@pytest.mark.benchmark
def test_reducer_manager_benchmark(images_external):
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
    features = extractor.extract(images_external)

    # Short benchmarks cached
    for name, n, cache, iterations in setups:
        output = timeit.timeit(
            lambda: mgr.reduce(
                fit_features=features[:n], features=features, name=name, cache=cache
            ),
            number=iterations,
        )

        print(
            f"{name} dims reductions of {n} images cached={cache} mean(FullExecTime)={output / iterations}s"
        )


@pytest.mark.benchmark
def test_pca_3d_large(images_external):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(images_external)
    model = dimension_reducers.PCAReducer(3)
    points = model.reduce(features)
    assert len(points) > 0
    assert len(points[0]) == 3
    print(f"Number of images: {len(points)}")
    print(points)


@pytest.mark.benchmark
def test_umap_3d_large(images_external):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(images_external)
    model = dimension_reducers.UMAPReducer(3)
    points = model.reduce(features)
    assert len(points) > 0
    assert len(points[0]) == 3
    print(f"Number of images: {len(points)}")
    print(points)
