from trame.widgets import html, quasar, client

from nrtk_explorer.widgets.nrtk_explorer import ImageDetection


class ImageList(html.Div):
    def __init__(self, hover_fn=None):
        super().__init__(classes="col")
        with self:
            with quasar.QTabs(classes="row", v_model=("image_list_tab", "grid"), align="left"):
                quasar.QTab(name="grid", label="Grid")
                quasar.QTab(name="table", label="Table")

            with quasar.QTabPanels(
                v_if="get(image_kinds[0].image_ids_list).value.length > 0",
                v_model=("image_list_tab", "grid"),
                animated=True,
            ):
                with quasar.QTabPanel(name="grid"):
                    ImageGrid(hover_fn=hover_fn)
                with quasar.QTabPanel(name="table"):
                    ImageTable(hover_fn=hover_fn)
            html.Div(
                "No images selected",
                v_if="get(image_kinds[0].image_ids_list).value.length === 0 && !loading_images",
                classes="text-h5 row flex-center q-my-md",
            )
            quasar.QInnerLoading(
                showing=("loading_images", False),
                label="Loading, transforming, and annotating images...",
            )


class ImageGrid(html.Div):
    def __init__(self, hover_fn=None):
        super().__init__(classes="row")
        with self:
            with html.Div(
                # For each original image, show all kinds of images.
                # Assume equal number of images in each image kind array.
                v_for=("id, idx in get(image_kinds[0].image_ids_list).value",),
                key="id",
                classes="col-xs-12 col-sm-6 col-md-4 col-xl-3 q-pa-xs",
            ):
                with quasar.QCard(flat=True, bordered=True):
                    with html.Div(classes="row"):
                        with html.Div(v_for=("kind in image_kinds",), classes="col-6 q-pa-sm"):
                            with client.Getter(
                                key_name="image_id",
                                name=("get(kind.image_ids_list).value[idx]",),
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


class ImageTable(html.Div):
    def __init__(self, hover_fn=None):
        super().__init__()
        with self:
            with quasar.QTable(
                flat=True,
                columns=(
                    """[
                        { name: 'id', label: 'ID', field: 'id', sortable: true },
                        { name: 'original', label: 'Original Image', field: 'original' },
                        { name: 'transformed', label: 'Transformed Image', field: 'transformed' },
                        { name: 'width', label: 'Width', field: 'width', sortable: true },
                        { name: 'height', label: 'Height', field: 'height', sortable: true },
                    ]""",
                ),
                rows=(
                    r"""get(image_kinds[0].image_ids_list).value.map((id) => 
                            {
                                const datasetId = id.split('_').at(-1) 
                                const meta = get(`${datasetId}_meta`).value
                                return {  
                                    id: datasetId, 
                                    original: id, 
                                    transformed: `transformed_${id}`,
                                    originalAnnotations: get(`${id}_result`).value,
                                    transformedAnnotations: get(`transformed_${id}_result`).value,
                                    ...meta,
                                }
                            })
                        """,
                ),
                row_key="id",
                rows_per_page_options=("[0]",),  # [0] means show all rows
            ):
                with html.Template(
                    v_slot_body_cell_original=True,
                    __properties=[
                        ("v_slot_body_cell_original", "v-slot:body-cell-original='props'")
                    ],
                ):
                    with quasar.QTd():
                        ImageDetection(
                            style="max-width: 10rem; float: inline-end;",
                            identifier=("props.row.original",),
                            src=("get(props.row.original).value",),
                            annotations=("props.row.originalAnnotations",),
                            categories=("annotation_categories",),
                            selected=("(props.row.original == hovered_id)",),
                            hover=(hover_fn, "[$event]"),
                        )
                with html.Template(
                    v_slot_body_cell_transformed=True,
                    __properties=[
                        ("v_slot_body_cell_transformed", "v-slot:body-cell-transformed='props'")
                    ],
                ):
                    with quasar.QTd():
                        ImageDetection(
                            style="max-width: 10rem; float: inline-end;",
                            identifier=("props.row.transformed",),
                            src=("get(props.row.transformed).value",),
                            annotations=("props.row.transformedAnnotations",),
                            categories=("annotation_categories",),
                            selected=("(props.row.transformed == hovered_id)",),
                            hover=(hover_fn, "[$event]"),
                        )
