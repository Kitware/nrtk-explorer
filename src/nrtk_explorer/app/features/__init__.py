from typing import TypedDict


class EnabledFeatures(TypedDict):
    datasets: bool
    inference: bool
    images: bool
    embeddings: bool
    transforms: bool
    export: bool
    filtering: bool


ALL_FEATURES: EnabledFeatures = {
    "datasets": True,
    "inference": True,
    "images": True,
    "embeddings": True,
    "transforms": True,
    "export": True,
    "filtering": True,
}

NO_FEATURES: EnabledFeatures = {
    "datasets": False,
    "inference": False,
    "images": False,
    "embeddings": False,
    "transforms": False,
    "export": False,
    "filtering": False,
}

DEFAULT_FEATURES = ALL_FEATURES

VIEWER_PRESET: EnabledFeatures = {
    "datasets": True,
    "inference": False,
    "images": True,
    "embeddings": False,
    "transforms": False,
    "export": False,
    "filtering": True,
}

FEATURE_PRESETS = {
    "all": ALL_FEATURES,
    "none": NO_FEATURES,
    "viewer": VIEWER_PRESET,
}


def validate_feature_name(feature: str) -> str:
    known_features = set(DEFAULT_FEATURES.keys())

    if feature not in known_features:
        raise ValueError(f"Unknown feature '{feature}'. Known features are {known_features}")

    return feature


def validate_preset_name(preset: str) -> str:
    known_presets = set(FEATURE_PRESETS.keys())

    if preset not in known_presets:
        raise ValueError(f"Unknown preset '{preset}'. Known presets are {known_presets}")

    return preset


def config_features_to_enabled_features(features: list[str] | None) -> EnabledFeatures:
    if features is None:
        return DEFAULT_FEATURES

    enabled_features = NO_FEATURES.copy()

    for feature in features:
        enabled_features[feature] = True

    return enabled_features


def config_preset_to_enabled_features(preset: str | None) -> EnabledFeatures:
    if preset is None:
        return DEFAULT_FEATURES

    return FEATURE_PRESETS[preset]
