class Translator:
    def __init__(self):
        self._transl = {}

    def add_translation(self, key, translated_key):
        self._transl[key] = translated_key

    def get_translation(self, key):
        if key in self._transl:
            return self._transl[key]
        else:
            return key

    def __call__(self, key):
        return self.get_translation(key)


class Wrapper:
    def __init__(self, obj, translator=None):
        if translator is None:
            translator = Translator()

        self.__dict__["translator"] = translator
        self.__dict__["_obj"] = obj

    def __getattr__(self, key):
        key = self.translator.get_translation(key)

        return getattr(self._obj, key)

    def __setattr__(self, key, value):
        key = self.translator.get_translation(key)

        return setattr(self._obj, key, value)

    def __getitem__(self, key):
        key = self.translator.get_translation(key)

        return self._obj[key]

    def __setitem__(self, key, value):
        key = self.translator.get_translation(key)

        self._obj[key] = value


class StateWrapper(Wrapper):
    def change(self, key):
        key = self.translator.get_translation(key)

        return self._obj.change(key)


class Applet:
    def __init__(
        self, server, state_translator=None, ctrl_translator=None, local_state_translator=None
    ):
        self._server = server

        if state_translator is None:
            self._state_translator = Translator()
            self._state = server.state
        else:
            self._state_translator = state_translator
            self._state = StateWrapper(server.state, state_translator)

        if ctrl_translator is None:
            self._ctrl_translator = Translator()
            self._ctrl = server.controller
        else:
            self._ctrl_translator = ctrl_translator
            self._ctrl = Wrapper(server.controller, ctrl_translator)

        if local_state_translator is None:
            self._local_state_translator = Translator()
            if not hasattr(self.server, "_local_state"):
                self.server._local_state = {}

            self._local_state = server._local_state

        else:
            self._local_state_translator = local_state_translator
            self._local_state = Wrapper(server.local_state, ctrl_translator)

    @property
    def server(self):
        return self._server

    @property
    def state(self):
        return self._state

    @property
    def ctrl(self):
        return self._ctrl

    @property
    def state_translator(self):
        return self._state_translator

    @property
    def ctrl_translator(self):
        return self._ctrl_translator

    @property
    def local_state(self):
        return self._local_state

    @property
    def local_state_translator(self):
        return self._local_state_translator
