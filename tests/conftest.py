# conftest.py

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--benchmark-dataset-file", default=None, help="COCO JSON path for benchmarks"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "benchmark: mark test as benchmarks")


def pytest_collection_modifyitems(config, items):
    json_file = config.getoption("--benchmark-dataset-file")
    if json_file is not None:
        # list test durations
        config.option.verbose = 1
        config.option.durations = 0

    else:
        do_skip = pytest.mark.skip(reason="need --benchmark-dataset-file opt set to run")
        for item in items:
            if "benchmark" in item.keywords:
                item.add_marker(do_skip)
