from trame_server.core import Server, State, Controller


class Applet:
    def __init__(self, server: Server):
        self._server = server

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
