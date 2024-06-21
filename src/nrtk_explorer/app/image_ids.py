def image_id_to_dataset_id(image_id: str) -> str:
    return image_id.split("_")[-1]


def image_id_to_result_id(image_id: str) -> str:
    return f"result_{image_id}"
