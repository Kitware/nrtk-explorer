from pathlib import Path
from trame.ui.quasar import QLayout
from trame.widgets import quasar
from trame.widgets import html
from nrtk_explorer.app import ui


def toolbar(reload=None):
    with quasar.QHeader():
        with quasar.QToolbar(classes="shadow-4"):
            quasar.QToolbarTitle("NRTK_EXPLORER")
            if reload:
                quasar.QBtn(
                    "Reload",
                    click=(reload,),
                    flat=True,
                )


def parse_dataset_dirs(datasets):
    return [{"label": Path(ds).name, "value": ds} for ds in datasets]


def parameters(dataset_paths=[], embeddings_app=None, filtering_app=None, transforms_app=None):
    with html.Div(classes="q-pa-md q-gutter-md"):
        (
            dataset_title_slot,
            dataset_content_slot,
            _,
        ) = ui.card("collapse_dataset")

        with dataset_title_slot:
            html.Span("Dataset Selection", classes="text-h6")

        with dataset_content_slot:
            quasar.QSelect(
                label="Dataset",
                v_model=("current_dataset",),
                options=(parse_dataset_dirs(dataset_paths),),
                filled=True,
                emit_value=True,
                map_options=True,
                dense=True,
            )
            quasar.QSlider(
                v_model=("num_images", 15),
                min=(0,),
                max=("num_images_max", 25),
                disable=("num_images_disabled", True),
                step=(1,),
            )
            html.P(
                "{{num_images}}/{{num_images_max}} images",
                classes="text-caption text-center",
            )

            quasar.QToggle(
                v_model=("random_sampling", False),
                dense=False,
                label="Random selection",
            )

        (
            embeddings_title_slot,
            embeddings_content_slot,
            embeddings_actions_slot,
        ) = ui.card("collapse_embeddings")

        with embeddings_title_slot:
            html.Span("Embeddings", classes="text-h6")

        with embeddings_content_slot:
            embeddings_app.settings_widget()

        with embeddings_actions_slot:
            embeddings_app.compute_ui()

        (annotations_title_slot, annotations_content_slot, _) = ui.card("collapse_annotations")

        with annotations_title_slot:
            html.Span("Annotations settings", classes="text-h6")

        with annotations_content_slot:
            quasar.QSelect(
                label="Object detection Model",
                v_model=("object_detection_model", "facebook/detr-resnet-50"),
                options=(
                    [
                        {
                            "label": "facebook/detr-resnet-50",
                            "value": "facebook/detr-resnet-50",
                        },
                    ],
                ),
                filled=True,
                emit_value=True,
                map_options=True,
            )
            quasar.QInput(
                v_model=("object_detection_batch_size", 32),
                filled=True,
                stack_label=True,
                label="Batch Size",
                type="number",
            )

        filter_title_slot, filter_content_slot, filter_actions_slot = ui.card("collapse_filter")

        with filter_title_slot:
            html.Span("Category Filter", classes="text-h6")

        with filter_content_slot:
            filtering_app.filter_operator_ui()
            filtering_app.filter_options_ui()

        with filter_actions_slot:
            filtering_app.filter_apply_ui()

        (
            transforms_title_slot,
            transforms_content_slot,
            transforms_actions_slot,
        ) = ui.card("collapse_transforms")

        with transforms_title_slot:
            html.Span("Transform Settings", classes="text-h6")

        with transforms_content_slot:
            transforms_app.settings_widget()

        with transforms_actions_slot:
            transforms_app.apply_ui()


def dataset_view(
    embeddings_app=None,
    transforms_app=None,
):
    with quasar.QSplitter(
        v_model=("vertical_split",),
        limits=("[0,100]",),
        horizontal=True,
        classes="inherit-height zero-height",
    ):
        with html.Template(v_slot_before=True):
            embeddings_app.visualization_widget()

        with html.Template(v_slot_after=True):
            transforms_app.dataset_widget()


def explorer(
    dataset_paths=[],
    embeddings_app=None,
    filtering_app=None,
    transforms_app=None,
):
    with quasar.QSplitter(
        model_value=("horizontal_split",),
        classes="inherit-height",
        before_class="inherit-height zero-height scroll",
        after_class="inherit-height zero-height",
    ):
        with html.Template(v_slot_before=True):
            parameters(
                dataset_paths=dataset_paths,
                embeddings_app=embeddings_app,
                filtering_app=filtering_app,
                transforms_app=transforms_app,
            )

        with html.Template(v_slot_after=True):
            dataset_view(embeddings_app=embeddings_app, transforms_app=transforms_app)


def build_layout(
    server=None,
    reload=None,
    **kwargs,
):
    with QLayout(
        server, view="lhh LpR lff", classes="shadow-2 rounded-borders bg-grey-2"
    ) as layout:
        toolbar(reload=reload)

        with quasar.QPageContainer():
            with quasar.QPage():
                explorer(**kwargs)

    return layout
