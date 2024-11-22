from functools import partial
from typing import Any, Union, Callable
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


def prediction_to_annotations(state, predictions):
    annotations = []
    for prediction in predictions:
        # find matching category id if it exists
        category_id = next(
            (
                cat_id
                for cat_id, cat in state.annotation_categories.items()
                if cat["name"] == prediction["label"]
            ),
            None,
        )

        annotation = {"category_id": category_id}

        if "label" in prediction:
            annotation["label"] = prediction["label"]

        if "box" in prediction:
            bbox = prediction["box"]
            annotation["bbox"] = [
                bbox["xmin"],
                bbox["ymin"],
                bbox["xmax"] - bbox["xmin"],
                bbox["ymax"] - bbox["ymin"],
            ]

        annotations.append(annotation)
    return annotations


def add_prediction_to_state(state: Any, image_id: str, prediction: Any):
    state[image_id_to_result_id(image_id)] = prediction_to_annotations(state, prediction)


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
        add_to_cache_callback=partial(add_prediction_to_state, server.state),
    )
