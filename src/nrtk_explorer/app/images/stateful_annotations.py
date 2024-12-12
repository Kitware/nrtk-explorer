from functools import partial
from typing import Any, Union, Callable
from .annotations import GroundTruthAnnotations, DetectionAnnotations
from trame.decorators import TrameApp, change
from nrtk_explorer.library.annotations import to_annotation
from nrtk_explorer.app.images.image_ids import (
    image_id_to_result_id,
)
from nrtk_explorer.app.trame_utils import delete_state


def add_annotation_to_state(state: Any, image_id: str, annotations: Any):
    state[image_id_to_result_id(image_id)] = annotations


def delete_annotation_from_state(state: Any, image_id: str):
    delete_state(state, image_id_to_result_id(image_id))


def add_predictions_to_state(context: Any, state: Any, image_id: str, predictions: Any):
    state[image_id_to_result_id(image_id)] = [
        to_annotation(context.dataset, prediction) for prediction in predictions
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

    @change("current_dataset", "inference_model")
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
        add_to_cache_callback=partial(add_predictions_to_state, server.context, server.state),
    )
