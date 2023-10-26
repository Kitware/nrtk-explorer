from trame.widgets import plotly, html, client


def result_list_component(state, ctrl, image_ids_key):
    with html.Div(
        v_for=(f"image_id in {image_ids_key}",), key="image_id", style="padding: 0.71875rem;"
    ):
        with client.Getter(name=("image_id + '_result'",), value_name="value"):
            plotly.Figure(
                style="width: 100%; height: 12rem;",
                data=("value",),
            )
