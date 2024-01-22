from trame.widgets import html

from nrtk_explorer.widgets.nrtk_explorer import ImageDetection


def image_list_component(image_ids_key, hover_fn=None):
    with html.Div(classes="row"):
        with html.Div(
            v_for=(f"image_id in {image_ids_key}",), key="image_id", classes="col-3 q-pa-sm"
        ):
            ImageDetection(
                identifier=("image_id",),
                src=("get(image_id)",),
                meta=("get(`${image_id}_meta`)",),
                annotations=("get(`${image_id}_result`)",),
                categories=("get('annotation_categories')",),
                selected=("get(`${image_id}_selected`)",),
                hover=(hover_fn, "[$event]"),
            )
