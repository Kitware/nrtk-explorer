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
        original_detection_annotations=None,
        transformed_detection_annotations=None,
        **kwargs,
    ):
        super().__init__(server)

        config = process_config(self.server.cli, config_options, **kwargs)
        self.state.inference_models = config["models"]
        self.state.inference_model = self.state.inference_models[0]

        original_detection_annotations = original_detection_annotations or make_stateful_predictor(
            server
        )
        self.context.original_detection_annotations = (
            original_detection_annotations.annotations_factory
        )

        transformed_detection_annotations = (
            transformed_detection_annotations or make_stateful_predictor(server)
        )
        self.context.transformed_detection_annotations = (
            transformed_detection_annotations.annotations_factory
        )

        self.context.predictor = MultiprocessPredictor(model_name=self.state.inference_model)

        self._ui = None

        self.server.controller.on_server_ready.add(self.on_server_ready)

    def on_server_ready(self, *args, **kwargs):
        self.state.change("inference_model")(self.on_inference_model_change)
        self.state.change("current_dataset")(self.reset_predictor)
        self.state.change("confidence_score_threshold")(self.start_update_images)

    def on_inference_model_change(self, **kwargs):
        self.context.original_detection_annotations.cache_clear()
        self.context.transformed_detection_annotations.cache_clear()
        self.context.predictor.set_model(self.state.inference_model)
        self.start_update_images()

    def start_update_images(self):
        if self.ctrl.start_update_images.exists():
            self.ctrl.start_update_images()

    def reset_predictor(self, **kwargs):
        self.context.predictor.reset()

    def settings_widget(self):
        quasar.QSelect(
            label="Inference Model",
            v_model=("inference_model", "facebook/detr-resnet-50"),
            options=("inference_models", []),
            filled=True,
            emit_value=True,
            map_options=True,
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
