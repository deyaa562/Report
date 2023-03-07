import pytest
from ._internal import Launch
from ._data import parse


parse()
def pytest_addoption(parser):
    parser.addoption("--report", action="store_true")

def pytest_sessionstart(session):

    script_path = session.config.getoption("--report")
    if script_path:
        parse()
        Launch.start_launch()

def pytest_sessionfinish(session, exitstatus):

    script_path = session.config.getoption("--report")
    if script_path:
        Launch.finish_launch()
