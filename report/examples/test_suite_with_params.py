import pytest
import report

@report.feature('Feature')
class Feature:
    pass

@pytest.fixture(autouse=True)
def a():
    print('a')
    return 'a'
@pytest.fixture(autouse=True)
def b():
    return 'b'
@pytest.fixture(autouse=True)
def c():
    return 'c'

@report.story('Story')
class TestStory(Feature):

    @report.title('Suite with params {1} {2} {3}')
    def test_suite(self, a, b, c):
        self.add_step()

    @report.step('Step')
    def add_step(self):
        pass

    @report.step('Nested Step')
    def nested_step(self):
        self.add_step()

