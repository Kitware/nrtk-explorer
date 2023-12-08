from trame.widgets import client, html

from nrtk_explorer.widgets.nrtk_explorer import ImageDetection


def image_list_component(image_ids_key):
    with html.Div(classes="row"):
        with html.Div(
            v_for=(f"image_id in {image_ids_key}",), key="image_id", classes="col-3 q-pa-sm"
        ):
            ImageDetection(
                src=("get(image_id)",),
                meta=("get(`${image_id}_meta`)",),
                annotations=("get(`${image_id}_result`)",),
                categories=("get('annotation_categories')",),
            )
            # with client.Getter(name=("image_id",), value_name="src"):
            #     with client.Getter(name=("image_id + '_meta'",), value_name="meta"):
            #         with client.Getter(name=("image_id + '_result'",), value_name="annotations"):
            #             ImageDetection(src=("src",), meta=("meta",), annotations=("annotations",))
