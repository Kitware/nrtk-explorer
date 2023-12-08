from PIL.Image import Image
from PIL import Image as ImageModule
from cdao.library import images_manager

import warnings
import random

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import timm
import numpy as np


class EmbeddingsExtractor:
    def __init__(self, model_name="resnet50d", manager=None):
        self.images = dict()
        self.features = dict()
        self.model = model_name
        if manager is not None:
            self.manager = manager
        else:
            self.manager = images_manager.ImagesManager()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model_name):
        # Create model but do not train it
        model = timm.create_model(model_name, pretrained=True, num_classes=0)
        for param in model.parameters():
            param.requires_grad = False

        self._model = model.eval()
        data_config = timm.data.resolve_model_data_config(model)
        self.transforms = timm.data.create_transform(**data_config, is_training=False)

    def extract(self, paths, n=None, rand=False, cache=True, content=None):
        if n == 0 or len(paths) == 0:
            return None

        selected_paths = []
        if n:
            if rand:
                selected_paths = random.sample(paths, n)
            else:
                selected_paths = paths[:n]
        else:
            selected_paths = paths

        for path in selected_paths:
            if cache == False or path not in self.features:
                img = None
                if content:
                    img = content[path]
                else:
                    img = self.manager.LoadImage(path)
                features = self.model(self.transforms(img).unsqueeze(0))
                self.features[path] = features[0]

        return np.stack(list(self.features.values()))
