from nrtk_explorer.app.core import Engine


def main(server=None, **kwargs):
    engine = Engine(server)
    engine.server.start(**kwargs)


if __name__ == "__main__":
    main()
