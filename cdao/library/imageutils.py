from PIL.Image import Image
from PIL import Image as ImageModule

import json
import torch
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import timm
import numpy as np


def LoadImage(path):
    img = ImageModule.open(path)
    img = img.resize((224, 224))
    img = img.convert("RGB")
    return img


class DataSetLoader:
    def __init__(self, model_name="resnet50d"):
        self.images = dict()
        self.features = dict()

        # Create model but do not train it
        model = timm.create_model(model_name, pretrained=True, num_classes=0)
        for param in model.parameters():
            param.requires_grad = False

        self.model = model.eval()
        data_config = timm.data.resolve_model_data_config(model)
        self.transforms = timm.data.create_transform(**data_config, is_training=False)

    def load(self, paths, n):
        for path in paths[:n]:
            if path not in self.images:
                self.images[path] = LoadImage(path)

            if path not in self.features:
                img = self.images[path]
                features = self.model(self.transforms(img).unsqueeze(0))
                self.features[path] = features[0]

        return np.stack(list(self.features.values()))
