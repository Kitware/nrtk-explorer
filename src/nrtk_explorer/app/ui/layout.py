from trame.ui.quasar import QLayout
from trame.widgets import quasar
from trame.widgets import html, alerts, alerts_quasar
from nrtk_explorer.app import ui

HORIZONTAL_SPLIT_DEFAULT_VALUE = 17
VERTICAL_SPLIT_DEFAULT_VALUE = 40


class NrtkDrawer(html.Div):
    def __init__(
        self,
        datasets_app=None,
        embeddings_app=None,
        filtering_app=None,
        transforms_app=None,
        inference_app=None,
        export_app=None,
    ):
        super().__init__(classes="q-pa-md q-gutter-md")

        with self:
            # Datasets
            if datasets_app:
                with ui.CollapsibleCard() as card:
                    with card.slot_title:
                        html.Span("Dataset", classes="text-h6")
                    with card.slot_content:
                        datasets_app.settings_widget()

            # Embeddings
            if embeddings_app:
                with ui.CollapsibleCard() as card:
                    with card.slot_title:
                        quasar.QToggle(v_model=("embeddings_enabled_switch", True))
                        html.Span("Embeddings", classes="text-h6")
                    with card.slot_content:
                        embeddings_app.settings_widget()
                    with card.slot_actions:
                        embeddings_app.compute_ui()

            # Inference
            if inference_app:
                with ui.CollapsibleCard() as card:
                    with card.slot_title:
                        quasar.QToggle(v_model=("inference_enabled_switch", False))
                        html.Span("Model Inference", classes="text-h6")
                    with card.slot_content:
                        inference_app.settings_widget()

            # Transforms
            if transforms_app:
                with ui.CollapsibleCard() as card:
                    with card.slot_title:
                        quasar.QToggle(v_model=("transform_enabled_switch", False))
                        html.Span("Transform", classes="text-h6")
                    with card.slot_content:
                        transforms_app.settings_widget()
                    with card.slot_actions:
                        transforms_app.apply_ui()

            # Export
            if export_app:
                with ui.CollapsibleCardUnslotted() as card:
                    with card.slot_title:
                        html.Span("Export Dataset", classes="text-h6")
                    with card.slot_collapse:
                        export_app.export_ui()

            # Filters
            if filtering_app:
                with ui.CollapsibleCard() as card:
                    with card.slot_title:
                        html.Span("Category Filter", classes="text-h6")
                    with card.slot_content:
                        filtering_app.filter_operator_ui()
                        filtering_app.filter_options_ui()
                    with card.slot_actions:
                        filtering_app.filter_apply_ui()


def nrtk_content(embeddings_app=None, images_app=None):
    if embeddings_app and images_app:
        with Splitter(
            model_value=("embeddings_enabled_switch ? vertical_split : 0",),
            update_model_value="vertical_split = $event",
            limits=("[0,100]",),
            disable=("!embeddings_enabled_switch",),
            horizontal=True,
            classes="inherit-height zero-height",
        ) as split_scatter_table:
            with split_scatter_table.slot_before:
                with html.Template(v_if=("embeddings_enabled_switch",)):
                    embeddings_app.visualization_widget()

            with split_scatter_table.slot_after:
                images_app.dataset_widget()
    elif embeddings_app:
        with html.Template(v_if=("embeddings_enabled_switch",)):
            embeddings_app.visualization_widget()
    elif images_app:
        images_app.dataset_widget()


class Splitter(quasar.QSplitter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self:
            self.slot_before = html.Template(raw_attrs=["v-slot:before"])
            self.slot_after = html.Template(raw_attrs=["v-slot:after"])


class NrtkToolbar(quasar.QHeader):
    def __init__(self, reload=None):
        super().__init__()
        with self:
            with quasar.QToolbar(classes="shadow-4"):
                quasar.QToolbarTitle("NRTK Explorer")
                if reload:
                    quasar.QBtn(
                        "Reload",
                        click=(reload,),
                        flat=True,
                    )
                quasar.QSpinnerBox(
                    v_show="trame__busy",
                    size="2rem",
                )
                alerts_quasar.AlertsCount(click="rightDrawer = !rightDrawer")


class NrtkExplorerLayout(QLayout):
    def __init__(
        self,
        server,
        reload=None,
        datasets_app=None,
        images_app=None,
        embeddings_app=None,
        filtering_app=None,
        inference_app=None,
        transforms_app=None,
        export_app=None,
        **kwargs,
    ):
        super().__init__(server, view="lhh LpR lff", classes="shadow-2 rounded-borders bg-grey-2")

        self.state.setdefault("vertical_split", VERTICAL_SPLIT_DEFAULT_VALUE)
        self.state.setdefault("horizontal_split", HORIZONTAL_SPLIT_DEFAULT_VALUE)
        # Make local variables on state
        self.state.client_only("horizontal_split", "vertical_split")
        self.state.trame__title = "NRTK Explorer"

        with self:
            with alerts.AlertsProvider() as alerts_provider:
                # Add create_alert, create_error_alert, etc. to the controller
                alerts_provider.bind_controller()

                NrtkToolbar(reload=reload)

                with quasar.QDrawer(
                    v_model=("rightDrawer", False),
                    side="right",
                    bordered=True,
                    overlay=True,
                    width=400,
                ):
                    alerts_quasar.AlertsList()

                with quasar.QPageContainer():
                    with quasar.QPage():
                        drawer_apps = (
                            datasets_app,
                            embeddings_app,
                            filtering_app,
                            inference_app,
                            transforms_app,
                            export_app,
                        )
                        if any(drawer_apps):
                            with Splitter(
                                model_value=("horizontal_split", HORIZONTAL_SPLIT_DEFAULT_VALUE),
                                classes="inherit-height",
                                before_class="inherit-height zero-height scroll",
                                after_class="inherit-height zero-height",
                            ) as split_drawer_main:
                                with split_drawer_main.slot_before:
                                    NrtkDrawer(
                                        datasets_app=datasets_app,
                                        embeddings_app=embeddings_app,
                                        filtering_app=filtering_app,
                                        inference_app=inference_app,
                                        transforms_app=transforms_app,
                                        export_app=export_app,
                                    )
                                with split_drawer_main.slot_after:
                                    nrtk_content(embeddings_app, images_app)
                        else:
                            nrtk_content(embeddings_app, images_app)

                alerts_quasar.AlertsPopup()
