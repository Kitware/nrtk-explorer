from trame.widgets import quasar
from trame.widgets import html


def card(collapse_key):
    with quasar.QCard():
        with quasar.QCardSection():
            with html.Div(classes="row items-center no-wrap"):
                title_slot = html.Div(classes="col")

                with html.Div(classes="col-auto"):
                    quasar.QBtn(
                        round=True,
                        flat=True,
                        dense=True,
                        click=f"{collapse_key} = !{collapse_key}",
                        icon=(f"{collapse_key} ? 'keyboard_arrow_down' : 'keyboard_arrow_up'",),
                    )
        with quasar.QSlideTransition():
            with html.Div(v_show=f"!{collapse_key}"):
                content_slot = quasar.QCardSection()
                actions_slot = quasar.QCardActions(align="right")

    return title_slot, content_slot, actions_slot
