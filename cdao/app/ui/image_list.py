from trame.widgets  import (
    client,
    vuetify3 as vuetify
)

from cdao.widgets.cdao import ImageDetection

def image_list_component(image_ids_key):
    with vuetify.VRow():
        with vuetify.VCol(v_for=(f"image_id in {image_ids_key}",), key="image_id", cols=3):
            ImageDetection(
                src=("get(image_id)",),
                meta=("get(`${image_id}_meta`)",),
                annotations=("get(`${image_id}_result`)",),
                categories=("get('annotation_categories')",)
            )
            # with client.Getter(name=("image_id",), value_name="src"):
            #     with client.Getter(name=("image_id + '_meta'",), value_name="meta"):
            #         with client.Getter(name=("image_id + '_result'",), value_name="annotations"):
            #             ImageDetection(src=("src",), meta=("meta",), annotations=("annotations",))
