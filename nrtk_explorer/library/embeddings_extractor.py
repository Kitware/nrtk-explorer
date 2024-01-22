from nrtk_explorer.library import images_manager

import warnings

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
                features = self.model(self.transforms(img).unsqueeze(0))
                self.features[path] = features[0]
            requested_features.append(self.features[path])

        return np.stack(requested_features)
