from nrtk_explorer.app.images.image_meta import dataset_id_to_meta

GROUND_TRUTH_MODEL = "ground-truth"


def image_id_to_dataset_id(image_id: str):
    return image_id.split("_")[-1]


def dataset_id_to_image_id(dataset_id: str):
    return f"img_{dataset_id}"


def dataset_id_to_transformed_image_id(dataset_id: str):
    return f"transformed_img_{dataset_id}"


def image_id_to_result_id(image_id: str, model_name: str):
    return f"result_{image_id}_{model_name}"


def image_id_to_score_id(image_id: str, model_name: str):
    return f"score_{image_id}_{model_name}"


def is_transformed(image_id: str):
    return image_id.startswith("transformed_img_")


def get_image_state_keys(dataset_id: str, annotation_models: list[str]):
    image_id = dataset_id_to_image_id(dataset_id)
    transformed_image_id = dataset_id_to_transformed_image_id(dataset_id)

    keys = {
        "original_image": image_id,
        "ground_truth": image_id_to_result_id(image_id, GROUND_TRUTH_MODEL),
        "transformed_image": transformed_image_id,
        "meta_id": dataset_id_to_meta(dataset_id),
    }

    for model in annotation_models:
        original_key = f"original_image_detection_{model}"
        original_key_value = image_id_to_result_id(image_id, model)

        transformed_key = f"transformed_image_detection_{model}"
        transformed_key_value = image_id_to_result_id(transformed_image_id, model)

        keys[original_key] = original_key_value
        keys[transformed_key] = transformed_key_value

    return keys
