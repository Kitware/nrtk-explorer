import logging

from trame.widgets import quasar
from trame.widgets import html
from trame.app import get_server

from nrtk_explorer.library.multiprocess_predictor import MultiprocessPredictor
from nrtk_explorer.library.app_config import process_config

from nrtk_explorer.app.applet import Applet
from nrtk_explorer.app.images.stateful_annotations import (
    make_stateful_predictor,
)

INFERENCE_MODELS_DEFAULT = [
    "facebook/detr-resnet-50",
    "hustvl/yolos-tiny",
    "valentinafeve/yolos-fashionpedia",
]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config_options = {
    "models": {
        "flags": ["--models"],
        "params": {
            "nargs": "+",
            "default": INFERENCE_MODELS_DEFAULT,
            "help": "Space separated list of inference models",
        },
    },
}


class InferenceApp(Applet):
    def __init__(
        self,
        server,
        **kwargs,
    ):
        super().__init__(server)

        config = process_config(self.server.cli, config_options, **kwargs)
        self.state.inference_models_options = config["models"]
        self.state.inference_models = [self.state.inference_models_options[0]]
        self.state.inference_multi_model = False

        inference_models_obj = {0: {"name": "ground-truth"}}
        for i, model in enumerate(self.state.inference_models):
            inference_models_obj[i + 1] = {"name": model}

        self.state.inference_models_obj = inference_models_obj

        self.context.models = {}

        self._ui = None

        self.server.controller.on_server_ready.add(self.on_server_ready)

        self.update_inference_models(self.state.inference_models)

    def on_server_ready(self, *args, **kwargs):
        self.state.change("current_dataset")(self.reset_predictor)
        self.state.change("confidence_score_threshold")(self.start_update_images)

    def update_inference_models(self, models):
        if isinstance(models, str):
            models = [models]

        # At least one model should be selected
        if len(models) == 0:
            return

        models_set = set(models)
        models_to_remove = []
        # Remove predictors that are not selected anymore
        for model_name, obj in self.context.models.items():
            if model_name not in models_set:
                predictor = obj["predictor"]
                original_annotations = obj["original_annotations"]
                transformed_annotations = obj["transformed_annotations"]
                predictor.shutdown()
                original_annotations.cache_clear()
                transformed_annotations.cache_clear()
                models_to_remove.append(model_name)

        for model_name in models_to_remove:
            del self.context.models[model_name]

        # Create any predictors that may have been added
        for model_name in models:
            if model_name not in self.context.models:
                predictor = MultiprocessPredictor(model_name=model_name)
                original_annotations = make_stateful_predictor(self.server, model_name)
                transformed_annotations = make_stateful_predictor(self.server, model_name)

                self.context.models[model_name] = {
                    "predictor": predictor,
                    "original_annotations": original_annotations.annotations_factory,
                    "transformed_annotations": transformed_annotations.annotations_factory,
                }

        models_obj = {0: {"name": "ground-truth"}}
        for i, model in enumerate(models):
            models_obj[i + 1] = {"name": model}

        with self.state:
            self.state.inference_models = models
            self.state.inference_models_obj = models_obj

        self.start_update_images()

    def update_inference_multi_model(self, multi):
        if not multi:
            self.update_inference_models(self.state.inference_models[0])

        with self.state:
            self.state.inference_multi_model = multi

    def start_update_images(self, *args, **kwargs):
        if self.ctrl.start_update_images.exists():
            self.ctrl.start_update_images()

    def reset_predictor(self, **kwargs):
        for obj in self.context.models.values():
            predictor = obj["predictor"]
            original_annotations = obj["original_annotations"]
            transformed_annotations = obj["transformed_annotations"]
            predictor.reset()
            original_annotations.cache_clear()
            transformed_annotations.cache_clear()

    def settings_widget(self):
        quasar.QSelect(
            label="Inference Model",
            model_value=("inference_multi_model ? inference_models : inference_models",),
            update_model_value=(self.update_inference_models, "[$event]"),
            options=("inference_models_options", []),
            multiple=("inference_multi_model",),
            filled=True,
            emit_value=True,
            map_options=True,
        )

        quasar.QToggle(
            model_value=("inference_multi_model",),
            update_model_value=(self.update_inference_multi_model, "[$event]"),
            label="Multiple models",
            left_label=True,
        )

        quasar.QSlider(
            v_model=("confidence_score_threshold", 0.01),
            min=(0,),
            max=(1.0,),
            step=(0.01,),
            classes="q-pt-sm",
        )
        html.P(
            "Confidence score threshold: {{confidence_score_threshold}}",
            classes="text-center",
        )

    # This is only used within when this module (file) is executed as an Standalone app.
    @property
    def ui(self):
        pass


def main(server=None, *args, **kwargs):
    server = get_server(client_type="vue3")

    transforms_app = InferenceApp(server)
    transforms_app.ui

    server.start(**kwargs)


if __name__ == "__main__":
    main()
