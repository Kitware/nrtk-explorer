from trame.app import get_server
from trame.ui.quasar import QLayout
from trame.widgets import quasar, vtk as vtk_widgets


class Cone:
    def __init__(self, server_or_name=None):
        self.server = get_server(server_or_name, client_type="vue3")
        self.state.resolution = 12
        self.ui = self._generate_ui()

    @property
    def ctrl(self):
        return self.server.controller

    @property
    def state(self):
        return self.server.state

    @property
    def resolution(self):
        return self.state.resolution

    @resolution.setter
    def resolution(self, v):
        with self.state:
            self.state.resolution = int(v)

    def reset_resolution(self):
        self.resolution = 6

    def _generate_ui(self):
        with QLayout(self.server) as layout:
            self._ui = layout

            with quasar.QToolbar():
                quasar.QSlider(
                    v_model=("resolution", 6),
                    min=(3,),
                    max=(60,),
                    step=(1,),
                    snap=(True,),
                )

            with quasar.QPageContainer():
                with quasar.QPage():
                    with vtk_widgets.VtkView(style="position: static") as view:
                        self.ctrl.view_reset_camera = view.reset_camera
                        with vtk_widgets.VtkGeometryRepresentation():
                            vtk_widgets.VtkAlgorithm(
                                vtk_class="vtkConeSource", state=("{ resolution }",)
                            )

        return layout


def main(**kwargs):
    cone = Cone()
    cone.server.start(**kwargs)


if __name__ == "__main__":
    main()
