from typing import Any
from collections import OrderedDict
from trame.app import get_server
from nrtk_explorer.app.images.image_ids import (
    image_id_to_result_id,
    dataset_id_to_image_id,
    dataset_id_to_transformed_image_id,
)
from nrtk_explorer.library.dataset import get_image_path

server = get_server()
state, ctrl = server.state, server.controller


@state.change("image_ids")
def init_state(**kwargs):
    dataset_ids = [str(id) for id in state.image_ids]
    # create reactive annotation variables so ImageDetection component has live Refs
    for id in dataset_ids:
        state[image_id_to_result_id(id)] = None
        state[image_id_to_result_id(dataset_id_to_image_id(id))] = None
        state[image_id_to_result_id(dataset_id_to_transformed_image_id(id))] = None
        state[dataset_id_to_transformed_image_id(id)] = None
    state.dataset_ids = dataset_ids
    state.hovered_id = None


# state.change does not trigger callback on initial set of state.image_ids
ctrl.add("on_server_ready")(init_state)


def get_image(images_manager, dataset_id: str):
    image_path = get_image_path(dataset_id)
    return images_manager.load_image(image_path)


def get_transformed_image(images_manager, transform, dataset_id: str):
    image = get_image(images_manager, dataset_id)
    return transform.execute(image)
