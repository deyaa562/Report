import report

report.Launch.start_launch()
@report.feature('UI')
class UI:
    pass

@report.step('c')
def c():
    pass

@report.step('Test param {1}')
def b(param ,b):
    c()

@report.story('Class')
class A(UI):

    @report.title('Test {2}')
    def test_a(self, a, c):
        b(1, 'b')


if __name__ == '__main__':
    report.parse()
    a = A()
    a.test_a(1, 2)
    report.Launch.finish_launch()
    