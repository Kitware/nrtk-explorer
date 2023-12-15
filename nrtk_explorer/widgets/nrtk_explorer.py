from trame_client.widgets.core import AbstractElement
from .. import module


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


class ImageDetection(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "image-detection",
            **kwargs,
        )
        self._attr_names += [
            "src",
            "meta",
            "annotations",
            "categories",
        ]
        self._event_names += []


class ScatterPlot(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "scatter-plot",
            **kwargs,
        )
        self._attr_names += [
            "points",
        ]
        self._event_names += [
            "click",
            "select",
        ]


class ParamsWidget(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "params-widget",
            **kwargs,
        )
        self._attr_names += [
            "values",
            "descriptions",
        ]
        self._event_names += ["valuesChanged"]
