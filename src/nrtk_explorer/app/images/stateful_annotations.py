from functools import partial
from typing import Any, Union, Callable
from .annotations import GroundTruthAnnotations, DetectionAnnotations
from trame.decorators import TrameApp, change
from nrtk_explorer.library.annotations import to_annotation
from nrtk_explorer.app.images.image_ids import (
    image_id_to_result_id,
)
from nrtk_explorer.app.trame_utils import delete_state


def add_annotation_to_state(state: Any, model_name: str, image_id: str, annotations: Any):
    state[image_id_to_result_id(image_id, model_name)] = annotations


def delete_annotation_from_state(state: Any, model_name: str, image_id: str):
    delete_state(state, image_id_to_result_id(image_id, model_name))


def add_predictions_to_state(
    context: Any, state: Any, model_name: str, image_id: str, predictions: Any
):
    state_key = image_id_to_result_id(image_id, model_name)
    state[state_key] = [to_annotation(context.dataset, prediction) for prediction in predictions]


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
        model_name: str,
        add_to_cache_callback=None,
    ):
        self.server = server
        state = self.server.state
        add_to_cache_callback = add_to_cache_callback or partial(
            add_annotation_to_state, state, model_name
        )
        delete_from_cache_callback = partial(delete_annotation_from_state, state, model_name)
        self.annotations_factory = annotations_factory_constructor(
            add_to_cache_callback, delete_from_cache_callback
        )

    @change("current_dataset", "inference_models")
    def _cache_clear(self, **kwargs):
        self.annotations_factory.cache_clear()


def make_stateful_annotations(server, model_name):
    return StatefulAnnotations(partial(GroundTruthAnnotations, server.context), server, model_name)


def make_stateful_predictor(server, model_name):
    return StatefulAnnotations(
        DetectionAnnotations,
        server,
        model_name,
        add_to_cache_callback=partial(
            add_predictions_to_state, server.context, server.state, model_name
        ),
    )
