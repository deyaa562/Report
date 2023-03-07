import pytest
import report


@pytest.fixture(autouse=True, scope='package')
def launc():
    report.parse()
    yield
    report.Launch.finish_launch()