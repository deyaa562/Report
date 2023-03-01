import pytest

def pytest_addoption(parser):
    parser.addoption("--report", action="store_true")

def pytest_sessionstart(session):
    from ._internal import Launch, Data

    script_path = session.config.getoption("--report")
    if script_path:
        Data.parse()
        Launch.start_launch()

def pytest_sessionfinish(session, exitstatus):
    from ._internal import Launch

    script_path = session.config.getoption("--report")
    if script_path:
        Launch.finish_launch()