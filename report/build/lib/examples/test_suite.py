import report

@report.feature('Feature')
class Feature:
    pass

@report.story('Story')
class TestStory(Feature):

    @report.title('Suite')
    def test_suite(self):
        self.add_step()

    @report.step('Step')
    def add_step(self):
        pass
