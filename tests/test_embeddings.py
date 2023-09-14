from cdao.library import imageutils
from cdao.library import embeddings

import json
import os

DATASET = "tests/assets/dataset.json"


def get_features():
    with open(DATASET) as f:
        dataset = json.load(f)
    images = dataset["images"]

    paths = list()
    for image_metadata in images:
        paths.append(os.path.join(os.path.dirname(DATASET), image_metadata["file_name"]))
    loader = imageutils.DataSetLoader()
    features = loader.load(paths, 10)
    return features


def test_LoadDataSet():
    features = get_features()
    print(features)


def test_pca():
    features = get_features()
    model = embeddings.PCAEmbeddings(3)
    points = model.execute(features)
    print(points)


def test_umap():
    features = get_features()
    model = embeddings.UMAPEmbeddings(3)
    points = model.execute(features)
    print(points)
