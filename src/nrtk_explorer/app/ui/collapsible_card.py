from trame.widgets import quasar
from trame.widgets import html
from trame.app import get_server

state = get_server().state
card_count = 0


def get_card_open_key():
    global card_count
    card_count += 1
    key = f"is_card_open_{card_count}"
    state[key] = True
    state.client_only(key)
    return key


def card(open_key=None):
    key = open_key if open_key is not None else get_card_open_key()
    with quasar.QCard():
        with quasar.QCardSection():
            with html.Div(classes="row items-center no-wrap"):
                title_slot = html.Div(classes="col")
                with html.Div(classes="col-auto"):
                    quasar.QBtn(
                        round=True,
                        flat=True,
                        dense=True,
                        click=f"{key} = !{key}",
                        icon=(f"{key} ? 'keyboard_arrow_up' : 'keyboard_arrow_down'",),
                    )
        with quasar.QSlideTransition():
            with html.Div(v_show=f"{key}"):
                content_slot = quasar.QCardSection()
                actions_slot = quasar.QCardActions(align="right")

    return title_slot, content_slot, actions_slot
