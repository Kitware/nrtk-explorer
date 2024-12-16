def process_config(cli, config_options, **kwargs):
    for opt in config_options.values():
        cli.add_argument(*opt["flags"], **opt["params"])
    known_args, _ = cli.parse_known_args()

    config = {}
    for name in config_options:
        if name in kwargs:
            config[name] = kwargs[name]
        else:
            config[name] = getattr(known_args, name)
    return config
