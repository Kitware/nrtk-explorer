from trame.widgets import html, quasar, client

from nrtk_explorer.widgets.nrtk_explorer import ImageDetection


class ImageList(html.Div):
    def __init__(self, hover_fn=None):
        super().__init__(classes="row content-start", style="height: 100%")
        with self:
            with html.Div(
                # For each original image, show all kinds of images.
                # Assume equal number of images in each image kind array.
                v_for=("id, idx in get(image_kinds[0].image_id_key).value",),
                key="id",
                classes="col-xs-12 col-sm-6 col-md-4 col-xl-3 q-pa-xs",
                v_if="get(image_kinds[0].image_id_key).value.length > 0",
            ):
                with quasar.QCard(flat=True, bordered=True):
                    with html.Div(classes="row"):
                        with html.Div(v_for=("kind in image_kinds",), classes="col-6 q-pa-sm"):
                            with client.Getter(
                                key_name="image_id",
                                name=("get(kind.image_id_key).value[idx]",),
                            ):
                                html.Div("{{kind.readable}}", classes="text-caption text-center")
                                ImageDetection(
                                    identifier=("image_id",),
                                    src=("get(image_id).value",),
                                    annotations=(r"get(`${image_id}_result`).value",),
                                    categories=("annotation_categories",),
                                    selected=("(image_id == hovered_id)",),
                                    hover=(hover_fn, "[$event]"),
                                )
            html.Div(
                "No images selected",
                v_else=True,
                classes="text-h5 col-12 row flex-center",
                style="height: 100%",
            )
