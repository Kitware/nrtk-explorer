from trame_server.core import Server, State, Controller
from trame.app import get_server


class Applet:
    def __init__(self, server: Server):
        self._server = get_server(server, client_type="vue3")

    @property
    def server(self) -> Server:
        return self._server

    @property
    def state(self) -> State:
        return self.server.state

    @property
    def ctrl(self) -> Controller:
        return self.server.controller

    @property
    def context(self) -> State:
        return self.server.context
