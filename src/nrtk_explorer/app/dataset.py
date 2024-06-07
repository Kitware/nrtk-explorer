import json
from typing import Optional
from pathlib import Path
from aiohttp import web
from trame.app import get_server
from trame.widgets import html, quasar

from nrtk_explorer.library.dataset import Dataset

DATASET_ENDPOINT = "dataset"

dataset_path = None
state = None


def get_disk_path(path: str) -> web.FileResponse:
    dataset_dir = Path(dataset_path).parent
    file_path = dataset_dir / path
    return file_path


def dataset_endpoint(request: web.Request):
    path = request.match_info["path"]
    file_path = get_disk_path(path)
    return web.FileResponse(file_path)


dataset_routes = [
    web.get(f"/{DATASET_ENDPOINT}/{{path}}", dataset_endpoint),
]


server = get_server()


def app_available(wslink_server):
    """Add our custom REST endpoints to the trame server."""
    wslink_server.app.add_routes(dataset_routes)


# --hot-reload does not work if this is configured as decorator on the function
server.controller.add("on_server_bind")(app_available)


def init(trame_state):
    global state
    state = trame_state
    load_dataset(None)
    state.selected_dataset_ids = []
    state.change("selected_dataset_rows")(on_selected_dataset_rows)


def load_dataset(path: str):
    global loaded_dataset, dataset_path
    dataset_path = path
    loaded_dataset = None
    if dataset_path is not None:
        with open(dataset_path) as f:
            loaded_dataset = json.load(f)
    update_images(loaded_dataset)


def update_images(loaded_dataset: Optional[Dataset]):
    state.selected_dataset_rows = []
    if loaded_dataset is None:
        state.all_images = []
        return
    state.all_images = [
        {"id": img["id"], "path": img["file_name"]} for img in loaded_dataset["images"]
    ]


def on_selected_dataset_rows(selected_dataset_rows, **kwargs):
    state.selected_dataset_ids = [row["id"] for row in selected_dataset_rows]


class ImageBrowser(html.Div):
    def __init__(self, hover_fn=None, **kwargs):
        super().__init__(style="height: 100%;", **kwargs)
        with self:
            with quasar.QTable(
                flat=True,
                virtual_scroll=(True,),
                style="height: 100%;",
                title="Dataset Images",
                grid=("image_browser_grid", False),
                filter=("image_browser_search", ""),
                raw_attrs=['selection="multiple"', 'v-model:selected="selected_dataset_rows"'],
                columns=(
                    """[
                        { name: 'id', label: 'ID', field: 'id', sortable: true },
                        { name: 'original', label: 'Original Image', field: 'original' },
                    ]""",
                ),
                rows=(
                    r"""get('all_images').value.map((image) =>
                            {
                                return {
                                    id: image.id,
                                    original: image.path,
                                }
                            })
                    """,
                ),
                row_key="id",
                rows_per_page_options=("[0]",),  # [0] means show all rows
            ):
                # img DOM element for original image column
                with html.Template(
                    v_slot_body_cell_original=True,
                    __properties=[
                        ("v_slot_body_cell_original", "v-slot:body-cell-original='props'")
                    ],
                ):
                    with quasar.QTd():
                        html.Img(
                            src=(f"`{DATASET_ENDPOINT}/${{props.row.original}}`",),
                            style="height: 10rem;",
                        )
                # Grid Mode template for each row/grid-item
                with html.Template(
                    v_slot_item=True,
                    __properties=[("v_slot_item", "v-slot:item='props'")],
                ):
                    with html.Div(classes="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3"):
                        with quasar.QCard(flat=True, bordered=True):
                            with html.Div(classes="row"):
                                html.Img(
                                    src=(f"`{DATASET_ENDPOINT}/${{props.row.original}}`",),
                                    style="height: 10rem;",
                                )
                            with quasar.QList(
                                dense=True,
                            ):
                                with quasar.QItem(
                                    v_for=(
                                        "col in props.cols.filter(col => !(['original'].includes(col.name)))",
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
                # Top control bar for search, grid switch, full screen
                with html.Template(
                    v_slot_top=True,
                    __properties=[("v_slot_top", "v-slot:top='props'")],
                ):
                    html.Span("Dataset Images", classes="col q-table__title")
                    quasar.QBtn(
                        icon="fullscreen",
                        dense=True,
                        flat=True,
                        click="props.toggleFullscreen",
                        classes="q-mx-md",
                    )
                    quasar.QToggle(
                        v_model=("image_browser_grid", False),
                        label="Grid",
                        left_label=True,
                        classes="col-1 q-mx-md",
                    )
                    quasar.QInput(
                        v_model=("image_browser_search", ""),
                        label="Search",
                        dense=True,
                        classes="col-3",
                    )
