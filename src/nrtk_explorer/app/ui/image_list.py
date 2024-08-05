from pathlib import Path
from trame.widgets import html, quasar, client
from trame.app import get_server
from nrtk_explorer.widgets.nrtk_explorer import ImageDetection

CSS_FILE = Path(__file__).with_name("image_list.css")

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


server = get_server()
state = server.state

state.client_only("columns")
state.columns = COLUMNS
state.visible_columns = [col["name"] for col in COLUMNS]


state.client_only("image_list_ids")


@state.change("dataset_ids", "user_selected_ids")
def update_image_list_ids(**kwargs):
    if len(state.user_selected_ids) > 0:
        state.image_list_ids = state.user_selected_ids
    else:
        state.image_list_ids = state.dataset_ids


@state.change("image_list_ids")
def reset_virtual_scroll(**kwargs):
    ImageList.reset_view_range()


class ImageList(html.Div):
    instances = []

    def get_id(self):
        return f"image-list-{self.instance_id}"

    @staticmethod
    def reset_view_range():
        for instance in ImageList.instances:
            instance.visible_ids = set()
            server.js_call(ref=instance.get_id(), method="resetVirtualScroll")

    def on_scroll(self, from_index, to_index):
        # TODO: fix sorted or filtered cases (with table.computedRows?)
        visible = set(state.image_list_ids[from_index : to_index + 1])
        if self.visible_ids != visible:
            self.visible_ids = visible
            self.scroll_callback(self.visible_ids)

    def __init__(self, on_scroll, on_hover, **kwargs):
        super().__init__(classes="full-height", **kwargs)
        self.instance_id = len(ImageList.instances)
        ImageList.instances.append(self)
        self.visible_ids = set()
        self.scroll_callback = on_scroll
        with self:
            client.Style(CSS_FILE.read_text())
            with quasar.QTable(
                ref=(self.get_id()),
                classes="full-height sticky-header",
                flat=True,
                hide_bottom=True,
                title="Selected Images",
                grid=("image_list_view_mode === 'grid'", False),
                filter=("image_list_search", ""),
                id="image-list",  # set id so that the ImageDetection component can select the container for tooltip positioning
                visible_columns=("visible_columns",),
                columns=("columns",),
                rows=(
                    r"""image_list_ids.map((id) =>
                            {
                                const meta = get(`meta_${id}`)?.value ?? {original_ground_to_original_detection_score: 0, ground_truth_to_transformed_detection_score: 0, original_detection_to_transformed_detection_score: 0}
                                return {
                                    ...meta,
                                    original_ground_to_original_detection_score: meta.original_ground_to_original_detection_score.toFixed(2),
                                    ground_truth_to_transformed_detection_score: meta.ground_truth_to_transformed_detection_score.toFixed(2),
                                    original_detection_to_transformed_detection_score: meta.original_detection_to_transformed_detection_score.toFixed(2),
                                    id,
                                    original: `img_${id}`,
                                    original_src: `original-image/${id}`,
                                    transformed: `transformed_img_${id}`,
                                    groundTruthAnnotations: get(`result_${id}`),
                                    originalAnnotations: get(`result_img_${id}`),
                                    transformedAnnotations: get(`result_transformed_img_${id}`),
                                }
                            })
                        """,
                ),
                row_key="id",
                rows_per_page_options=("[0]",),  # [0] means show all rows
                raw_attrs=[
                    "virtual-scroll",
                    "virtual-scroll-slice-size='2'",
                    "virtual-scroll-item-size='200'",
                    f'''@virtual-scroll="(e) => trigger('{ self.server.controller.trigger_name(self.on_scroll) }', [e.from, e.to])"''',
                    "virtual-scroll-sticky-size-start='48'",
                ],
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
                            hover=(on_hover, "[$event]"),
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
                            hover=(on_hover, "[$event]"),
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
                            hover=(on_hover, "[$event]"),
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
                                        hover=(on_hover, "[$event]"),
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
                                        hover=(on_hover, "[$event]"),
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
                                        hover=(on_hover, "[$event]"),
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
