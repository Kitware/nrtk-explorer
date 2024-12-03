from functools import partial
from typing import Any, Union, Callable, TypedDict, List
from .annotations import GroundTruthAnnotations, DetectionAnnotations
from trame.decorators import TrameApp, change
from nrtk_explorer.app.images.image_ids import (
    image_id_to_result_id,
)
from nrtk_explorer.app.trame_utils import delete_state


def add_annotation_to_state(state: Any, image_id: str, annotations: Any):
    state[image_id_to_result_id(image_id)] = annotations


def delete_annotation_from_state(state: Any, image_id: str):
    delete_state(state, image_id_to_result_id(image_id))


# from hugging face transformers.pipeline output
class Prediction(TypedDict, total=False):
    box: List[float]
    label: str
    score: float


class Annotation(TypedDict, total=False):
    category_id: int
    label: str
    score: float
    bbox: List[float]


def to_annotation(state: Any, prediction: Prediction) -> Annotation:

    annotation = {}

    if "label" in prediction:
        annotation["label"] = prediction["label"]
        # find matching category id if it exists
        category_id = next(
            (
                cat_id
                for cat_id, cat in state.annotation_categories.items()
                if cat["name"] == prediction["label"]
            ),
            None,
        )
        annotation["category_id"] = category_id

    if "score" in prediction:
        annotation["score"] = prediction["score"]

    if "box" in prediction:
        bbox = prediction["box"]
        annotation["bbox"] = [
            bbox["xmin"],
            bbox["ymin"],
            bbox["xmax"] - bbox["xmin"],
            bbox["ymax"] - bbox["ymin"],
        ]

    return annotation


def add_predictions_to_state(state: Any, image_id: str, predictions: Any):
    state[image_id_to_result_id(image_id)] = [
        to_annotation(state, prediction) for prediction in predictions
    ]


AnnotationsFactoryConstructorType = Union[
    Callable[[Callable, Callable], GroundTruthAnnotations],
    Callable[[Callable, Callable], DetectionAnnotations],
]


@TrameApp()
class StatefulAnnotations:
    def __init__(
        self,
        annotations_factory_constructor: AnnotationsFactoryConstructorType,
        server,
        add_to_cache_callback=None,
    ):
        self.server = server
        state = self.server.state
        add_to_cache_callback = add_to_cache_callback or partial(add_annotation_to_state, state)
        delete_from_cache_callback = partial(delete_annotation_from_state, state)
        self.annotations_factory = annotations_factory_constructor(
            add_to_cache_callback, delete_from_cache_callback
        )

    @change("current_dataset", "object_detection_model")
    def _cache_clear(self, **kwargs):
        self.annotations_factory.cache_clear()


def make_stateful_annotations(server):
    return StatefulAnnotations(
        partial(GroundTruthAnnotations, server.context),
        server,
    )


def make_stateful_predictor(server):
    return StatefulAnnotations(
        DetectionAnnotations,
        server,
        add_to_cache_callback=partial(add_predictions_to_state, server.state),
    )
