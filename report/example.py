import report

@report.feature('Feature')
class Feature:
    pass

@report.story('Story')
class Story(Feature):

    @report.title('Suite')
    def test_suite(self):
        pass

    @report.step('Step')
    def step(self):
        pass

    @report.step('Sub step')
    def sub_step(self):
        pass