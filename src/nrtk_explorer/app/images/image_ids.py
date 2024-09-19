from nrtk_explorer.app.images.image_meta import dataset_id_to_meta


def image_id_to_dataset_id(image_id: str):
    return image_id.split("_")[-1]


def dataset_id_to_image_id(dataset_id: str):
    return f"img_{dataset_id}"


def dataset_id_to_transformed_image_id(dataset_id: str):
    return f"transformed_img_{dataset_id}"


def image_id_to_result_id(image_id: str):
    return f"result_{image_id}"


def is_transformed(image_id: str):
    return image_id.startswith("transformed_img_")


def get_image_state_keys(dataset_id: str):
    return {
        "original_image": dataset_id_to_image_id(dataset_id),
        "ground_truth": image_id_to_result_id(dataset_id),
        "original_image_detection": image_id_to_result_id(dataset_id_to_image_id(dataset_id)),
        "transformed_image": dataset_id_to_transformed_image_id(dataset_id),
        "transformed_image_detection": image_id_to_result_id(
            dataset_id_to_transformed_image_id(dataset_id)
        ),
        "meta_id": dataset_id_to_meta(dataset_id),
    }
