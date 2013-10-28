from mock import Mock
from promptly.runners.console import ConsoleRunner


def run(form, returns):

    def side_effect(*args):
        result = returns.pop(0)
        return result

    mock = Mock(side_effect=side_effect)
    runner = MockRunner(form, mock)
    runner.run()
    return mock


class MockRunner(ConsoleRunner):
    def __init__(self, form, mock, prefix=None, stylesheet=None):
        super(MockRunner, self).__init__(form)
        self.mock = mock

    def render(self, value, default=None):
        return self.mock()

