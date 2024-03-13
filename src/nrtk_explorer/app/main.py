from nrtk_explorer.app.core import create_engine


def main(server=None, *args, **kwargs):
    engine = create_engine(server)
    engine.server.start(**kwargs)


if __name__ == "__main__":
    main()
