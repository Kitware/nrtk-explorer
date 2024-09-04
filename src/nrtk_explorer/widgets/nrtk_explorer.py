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
            "identifier",
            "src",
            "annotations",
            "categories",
            "selected",
            "containerSelector",
        ]
        self._event_names += [
            "hover",
        ]


class ScatterPlot(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "scatter-plot",
            **kwargs,
        )
        self._attr_names += [
            "cameraPosition",
            "highlightedPoint",
            "points",
            "transformedPoints",
            "selectedPoints",
        ]
        self._event_names += [
            "cameraMove",
            "hover",
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


class FilterOptionsWidget(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "filter-options-widget",
            **kwargs,
        )
        self._attr_names += [
            "modelValue",
            "options",
        ]
        self._event_names += [
            "update:modelValue",
        ]


class FilterOperatorWidget(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "filter-operator-widget",
            **kwargs,
        )
        self._attr_names += [
            "operator",
            "invert",
        ]
        self._event_names += [
            "update:operator",
            "update:invert",
        ]
