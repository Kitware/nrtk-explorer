from nrtk_explorer.library import images_manager

import logging
import numpy as np
import warnings

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=UserWarning)
    import timm
    import torch


class EmbeddingsExtractor:
    def __init__(self, model_name="resnet50d", manager=None, force_cpu=False):
        self.images = dict()
        self.features = dict()
        if manager is not None:
            self.manager = manager
        else:
            self.manager = images_manager.ImagesManager()

        if torch.cuda.is_available() and not force_cpu:
            self.device = torch.device("cuda")
            logging.info("Using CUDA devices for feature extraction")
        else:
            self.device = torch.device("cpu")
            logging.info("Using CPU devices for feature extraction")

        self.model = model_name

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model_name):
        # Create model but do not train it
        model = timm.create_model(model_name, pretrained=True, num_classes=0)

        # Copy the model to the requested device
        model = model.to(self.device)

        for param in model.parameters():
            param.requires_grad = False

        self._model = model.eval()
        data_config = timm.data.resolve_model_data_config(model)
        self.transforms = timm.data.create_transform(**data_config, is_training=False)

    def extract(self, paths, cache=True, content=None):
        if len(paths) == 0:
            return None

        requested_features = list()
        for path in paths:
            if cache is False or path not in self.features:
                img = None
                if content and path in content:
                    img = content[path]
                else:
                    img = self.manager.LoadImage(path)

                img_transformation = self.transforms(img).unsqueeze(0)

                # Copy image to device if using device
                if self.device.type == "cuda":
                    img_transformation = img_transformation.cuda()

                features = self.model(img_transformation)

                # Copy output to cpu if using device
                if self.device.type == "cuda":
                    features = features.cpu()

                self.features[path] = features[0]
            requested_features.append(self.features[path])

        return np.stack(requested_features)
