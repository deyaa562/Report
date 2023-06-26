import pytest
from ._data import parse
from ._internal import Launch
import traceback


been_there_key = pytest.StashKey[bool]()
done_that_key = pytest.StashKey[str]()

parse()

latest_item = ''


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
        for item in Launch.items().keys():
            Launch.finish_item(item)
        Launch.finish_launch()
    
    # Delete when done debugging
    for item in Launch.items().keys():
        Launch.finish_item(item)
    Launch.finish_launch()


@pytest.hookimpl(tryfirst=True)
def pytest_fixture_setup(fixturedef, request):
    fixture_name = getattr(fixturedef.func, '__new_name__', request.fixturename)
    if fixture_name and '_xunit_setup_class' not in fixture_name:
        parent = Launch.get_latest_item()
        item_id = Launch.create_report_item(
                name=fixture_name,
                parent_item=parent,
                type='step',
                has_stats=True,
                description='')
    
        Launch.add_item(request.fixturename, item_id)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
    test_name = getattr(item.function, '__new_name__', item.name)
    if item.name not in Launch.items() and item.parent is not None:
        item_id = Launch.create_report_item(
            name=test_name,
            parent_item=item.parent.name,
            type='scenario',
            has_stats=True,
            description='')

        Launch.add_item(item.name, item_id)
        
        item_setup_name = f'Setup'
        item_id = Launch.create_report_item(
            name=item_setup_name,
            parent_item=item.name,
            type='before_test',
            has_stats=True,
            description='')

        Launch.add_item(f'{item.name}_{item_setup_name}', item_id)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item, nextitem):
    item_teardown_name = 'Teardown'
    item_id = Launch.create_report_item(
        name=item_teardown_name,
        parent_item=item.name,
        type='after_test',
        has_stats=True,
        description='')

    Launch.add_item(f'{item.name}_{item_teardown_name}', item_id)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    excinfo = call.excinfo

    if call.when == 'setup':
        run_item_teardown(f'{item.name}_Setup', excinfo)

    if call.when == 'call':
        run_item_teardown(f'{item.name}_Execution', excinfo)

    if call.when == 'teardown':
        run_item_teardown(f'{item.name}_Teardown', excinfo)


def run_item_teardown(item_name: str, excinfo):
    if excinfo is None:
        Launch.finish_passed_item(item_name)
        if 'Setup' in item_name:
            required_item = item_name.split('_Setup')
            add_item_execution(required_item[0])

    elif excinfo is not None:
        traceback_str = ''.join(traceback.format_tb(excinfo.tb))
        Launch.finish_failed_item(item_name, message=excinfo.typename, reason=traceback_str)

def add_item_execution(item_name):
    item_execution_name = 'Execution'
    item_id = Launch.create_report_item(
        name=item_execution_name,
        parent_item=item_name,
        type='step',
        has_stats=True,
        description='')

    Launch.add_item(f'{item_name}_{item_execution_name}', item_id)