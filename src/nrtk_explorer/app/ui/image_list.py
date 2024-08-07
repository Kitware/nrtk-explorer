from trame.widgets import html, quasar

from nrtk_explorer.widgets.nrtk_explorer import ImageDetection

COLUMNS = [
    {"name": "id", "label": "Dataset ID", "field": "id", "sortable": True},
    {"name": "truth", "label": "Original: Ground Truth Annotations", "field": "truth"},
    {"name": "original", "label": "Original: Detection Annotations", "field": "original"},
    {
        "name": "transformed",
        "label": "Transformed: Detection Annotations",
        "field": "transformed",
    },
    {
        "name": "original_ground_to_original_detection_score",
        "label": "Ground Truth - Original Detection | Annotations Similarity",
        "field": "original_ground_to_original_detection_score",
        "sortable": True,
    },
    {
        "name": "ground_truth_to_transformed_detection_score",
        "label": "Ground Truth - Transformed Detection | Annotations Similarity",
        "field": "ground_truth_to_transformed_detection_score",
        "sortable": True,
    },
    {
        "name": "original_detection_to_transformed_detection_score",
        "label": "Original Detection - Transformed Detection | Annotations Similarity",
        "field": "original_detection_to_transformed_detection_score",
        "sortable": True,
    },
]


def init_state(state):
    state.client_only("columns")
    state.columns = COLUMNS
    state.visible_columns = [col["name"] for col in COLUMNS]


class ImageList(html.Div):
    def __init__(self, hover_fn=None):
        super().__init__(classes="col full-height")
        with self:
            ImageTable(
                v_if="source_image_ids.length > 0", hover_fn=hover_fn, classes="full-height"
            )
            html.Div(
                "No images selected",
                v_if="source_image_ids.length === 0 && !loading_images",
                classes="text-h5 row flex-center q-my-md",
            )
            quasar.QInnerLoading(
                showing=("loading_images", False),
                label="Loading, transforming, and annotating images...",
            )


class ImageTable(html.Div):
    def __init__(self, hover_fn=None, **kwargs):
        super().__init__(**kwargs)
        with self:
            with quasar.QTable(
                classes="full-height",
                flat=True,
                hide_bottom=True,
                title="Selected Images",
                grid=("image_list_view_mode === 'grid'", False),
                filter=("image_list_search", ""),
                id="image-list",  # set id so that the ImageDetection component can select the container for tooltip positioning
                visible_columns=("visible_columns",),
                columns=("columns",),
                rows=(
                    r"""source_image_ids.map((id) =>
                            {
                                const datasetId = id.split('_').at(-1)
                                const meta = get(`meta_${datasetId}`)?.value ?? {original_ground_to_original_detection_score: 0, ground_truth_to_transformed_detection_score: 0, original_detection_to_transformed_detection_score: 0}
                                return {
                                    ...meta,
                                    original_ground_to_original_detection_score: meta.original_ground_to_original_detection_score.toFixed(2),
                                    ground_truth_to_transformed_detection_score: meta.ground_truth_to_transformed_detection_score.toFixed(2),
                                    original_detection_to_transformed_detection_score: meta.original_detection_to_transformed_detection_score.toFixed(2),
                                    id: datasetId,
                                    original: id,
                                    original_src: `original-image/${datasetId}`,
                                    transformed: `transformed_${id}`,
                                    groundTruthAnnotations: get(`result_${datasetId}`),
                                    originalAnnotations: get(`result_${id}`),
                                    transformedAnnotations: get(`result_transformed_${id}`),
                                }
                            })
                        """,
                ),
                row_key="id",
                rows_per_page_options=("[0]",),  # [0] means show all rows
            ):
                # ImageDetection component for image columns
                with html.Template(
                    v_slot_body_cell_truth=True,
                    __properties=[("v_slot_body_cell_truth", "v-slot:body-cell-truth='props'")],
                ):
                    with quasar.QTd():
                        ImageDetection(
                            style="max-width: 10rem; float: inline-end;",
                            identifier=("props.row.original",),
                            src=("props.row.original_src",),
                            annotations=("props.row.groundTruthAnnotations",),
                            categories=("annotation_categories",),
                            selected=("(props.row.original == hovered_id)",),
                            hover=(hover_fn, "[$event]"),
                            containerSelector="#image-list .q-table__middle",
                        )
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
                            src=("props.row.original_src",),
                            annotations=("props.row.originalAnnotations",),
                            categories=("annotation_categories",),
                            selected=("(props.row.original == hovered_id)",),
                            hover=(hover_fn, "[$event]"),
                            containerSelector="#image-list .q-table__middle",
                        )
                with html.Template(
                    v_slot_body_cell_transformed=True,
                    __properties=[
                        (
                            "v_slot_body_cell_transformed",
                            "v-slot:body-cell-transformed='props'",
                        )
                    ],
                ):
                    with quasar.QTd():
                        ImageDetection(
                            style="max-width: 10rem; float: inline-end;",
                            identifier=("props.row.transformed",),
                            src=("get(props.row.transformed)",),
                            annotations=("props.row.transformedAnnotations",),
                            categories=("annotation_categories",),
                            selected=("(props.row.transformed == hovered_id)",),
                            hover=(hover_fn, "[$event]"),
                            containerSelector="#image-list .q-table__middle",
                        )
                # Grid Mode template for each row/grid-item
                with html.Template(
                    v_slot_item=True,
                    __properties=[("v_slot_item", "v-slot:item='props'")],
                ):
                    with html.Div(classes="q-pa-xs col-xs-12 col-sm-6 col-md-4"):
                        with quasar.QCard(flat=True, bordered=True):
                            with html.Div(classes="row"):
                                with html.Div(
                                    classes="col-4 q-pa-sm",
                                    v_if=("props.cols.map(c => c.name).includes('truth')", True),
                                ):
                                    html.Div(
                                        "Original: Ground Truth Annotations",
                                        classes="text-center",
                                    )
                                    ImageDetection(
                                        identifier=("props.row.original",),
                                        src=("props.row.original_src",),
                                        annotations=("props.row.groundTruthAnnotations",),
                                        categories=("annotation_categories",),
                                        selected=("(props.row.original == hovered_id)",),
                                        hover=(hover_fn, "[$event]"),
                                    )
                                with html.Div(
                                    classes="col-4 q-pa-sm",
                                    v_if=(
                                        "props.cols.map(c => c.name).includes('original')",
                                        True,
                                    ),
                                ):
                                    html.Div(
                                        "Original: Detection Annotations",
                                        classes="text-center",
                                    )
                                    ImageDetection(
                                        identifier=("props.row.original",),
                                        src=("props.row.original_src",),
                                        annotations=("props.row.originalAnnotations",),
                                        categories=("annotation_categories",),
                                        selected=("(props.row.original == hovered_id)",),
                                        hover=(hover_fn, "[$event]"),
                                    )
                                with html.Div(
                                    classes="col-4 q-pa-sm",
                                    v_if=(
                                        "props.cols.map(c => c.name).includes('transformed')",
                                        True,
                                    ),
                                ):
                                    html.Div(
                                        "Transformed: Detection Annotations",
                                        classes="text-center",
                                    )
                                    ImageDetection(
                                        identifier=("props.row.transformed",),
                                        src=("get(props.row.transformed)",),
                                        annotations=("props.row.transformedAnnotations",),
                                        categories=("annotation_categories",),
                                        selected=("(props.row.transformed == hovered_id)",),
                                        hover=(hover_fn, "[$event]"),
                                    )
                            with quasar.QList(
                                dense=True,
                            ):
                                with quasar.QItem(
                                    v_for=(
                                        "col in props.cols.filter(col => !(['truth', 'original', 'transformed'].includes(col.name)))",
                                    ),
                                    key=("col.name",),
                                ):
                                    with quasar.QItemSection():
                                        with quasar.QItemLabel():
                                            html.Div("{{col.label}}")
                                    with quasar.QItemSection(side=True):
                                        with quasar.QItemLabel(
                                            caption=True,
                                        ):
                                            html.Div("{{col.value}}")
                # Top control bar for visible-columns, search, table-grid switch, full-screen
                with html.Template(
                    v_slot_top=True,
                    __properties=[("v_slot_top", "v-slot:top='props'")],
                ):
                    html.Span("Selected Images", classes="col q-table__title")
                    quasar.QSelect(
                        v_model=("visible_columns"),
                        multiple=True,
                        dense=True,
                        options_dense=True,
                        emit_value=True,
                        map_options=True,
                        options=("columns",),
                        option_value="name",
                        options_cover=True,
                        raw_attrs=[
                            ":display-value='$q.lang.table.columns'",
                        ],
                    )
                    quasar.QBtn(
                        icon="fullscreen",
                        dense=True,
                        flat=True,
                        click="props.toggleFullscreen",
                        classes="q-mx-md",
                    )
                    quasar.QBtnToggle(
                        v_model=("image_list_view_mode", "table"),
                        raw_attrs=[
                            ":options=\"[{label: 'Table', value: 'table'}, {label: 'Grid', value: 'grid'}]\"",
                        ],
                    )
                    quasar.QInput(
                        v_model=("image_list_search", ""),
                        label="Search",
                        dense=True,
                        classes="col-3 q-pl-md",
                    )
