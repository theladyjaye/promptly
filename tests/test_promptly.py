import unittest
from promptly import Form
from promptly import StringInput
from promptly import IntegerInput
from promptly import ChoiceInput
from promptly import BooleanInput


class TestPromptly(unittest.TestCase):

    def test_session(self):
        form = Form()

        form.add('name',
            StringInput('What is your name?',
            default='Aubrey'))

        form.add('age',
            IntegerInput('What is your age?',
            default=1))

        form.add('color',
            ChoiceInput('What is your favorite color',
                zip(range(1,4), ('red', 'green', 'blue')),
            default=1))

        form.add('yaks', BooleanInput('Do you like yaks?', default=True))

        form.prompt()
        values = form.values()

        for v in values:
            print(v)
