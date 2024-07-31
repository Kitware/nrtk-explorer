# from typing import Sequence
# from trame_server.state import State
from trame.app import get_server
from nrtk_explorer.app.image_ids import (
    image_id_to_result_id,
    dataset_id_to_image_id,
    dataset_id_to_transformed_image_id,
)
from nrtk_explorer.library.dataset import get_image_path

server = get_server()
state, ctrl = server.state, server.controller


@state.change("image_ids")
def on_dataset_ids(**kwargs):
    dataset_ids = [str(id) for id in state.image_ids]
    # create reactive annotation variables so ImageDetection component has live Refs
    for id in dataset_ids:
        state[image_id_to_result_id(id)] = None
        state[image_id_to_result_id(dataset_id_to_image_id(id))] = None
        state[image_id_to_result_id(dataset_id_to_transformed_image_id(id))] = None
        state[dataset_id_to_transformed_image_id(id)] = None
    state.dataset_ids = dataset_ids
    state.hovered_id = None


# on_dataset_ids is not called on initial set of state.image_ids
ctrl.add("on_server_ready")(on_dataset_ids)


def get_image(images_manager, dataset_id: str):
    image_path = get_image_path(dataset_id)
    return images_manager.load_image(image_path)
