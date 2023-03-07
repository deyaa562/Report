import pytest
from ._internal import Launch, Data, parse


def pytest_addoption(parser):
    parser.addoption("--report", action="store", default=None,
                     help="path to the script to be executed before running tests")

def pytest_sessionstart(session):
    script_path = session.config.getoption("--report")
    if script_path:
        parse()
        Launch.start_launch()

def pytest_sessionfinish(session, exitstatus):
    script_path = session.config.getoption("--report")
    if script_path:
        Launch.finish_launch()

def parsepytest_load_initial_conftests_data(args):
        parse()
