def image_id_to_dataset_id(image_id: str):
    return image_id.split("_")[-1]


def dataset_id_to_image_id(dataset_id: str):
    return f"img_{dataset_id}"


def dataset_id_to_transformed_image_id(dataset_id: str):
    return f"transformed_img_{dataset_id}"


def image_id_to_result_id(image_id: str):
    return f"result_{image_id}"
