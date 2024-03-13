from trame.widgets import html

from nrtk_explorer.widgets.nrtk_explorer import ImageDetection


def image_list_component(image_ids_key, hover_fn=None, is_transformation=False):
    with html.Div(classes="row"):
        with html.Div(
            v_for=(f"image_id in {image_ids_key}",), key="image_id", classes="col-3 q-pa-sm"
        ):
            ImageDetection(
                identifier=("image_id.match(/\d+/)[0]",),  # noqa: W605
                src=("get(image_id).value",),
                meta=("get(`${image_id}_meta`).value",),
                annotations=("get(`${image_id}_result`).value",),
                categories=("annotation_categories",),
                selected=("(image_id.match(/\d+/)[0] == hovered_id)",),  # noqa: W605
                isTransformation=is_transformation,
                hover=(hover_fn, "[$event]"),
            )
