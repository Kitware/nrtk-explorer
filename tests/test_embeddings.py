from cdao.library import embeddings_extractor
from cdao.library import dimension_reducers

import json
import os
import pytest

CURRENT_DIR_NAME = os.path.dirname(__file__)
DATASET = f"{CURRENT_DIR_NAME}/../assets/OIRDS_v1_0/oirds_test.json"


@pytest.fixture
def image_paths():
    with open(DATASET) as f:
        dataset = json.load(f)
    images = dataset["images"]

    paths = list()
    for image_metadata in images:
        paths.append(os.path.join(os.path.dirname(DATASET), image_metadata["file_name"]))
    return paths


def test_features_features_small(image_paths):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths, 10)
    assert len(features) == 10
    print(features)


def test_features_features_zero(image_paths):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths, 0)
    assert features is None
    print(features)


def test_features_features_all(image_paths):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths)
    assert len(features) == len(image_paths)
    print(features)


def test_features_features_rand(image_paths):
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


@pytest.mark.slow
def test_pca_3d_large(image_paths):
    extractor = embeddings_extractor.EmbeddingsExtractor()
    features = extractor.extract(image_paths)
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
