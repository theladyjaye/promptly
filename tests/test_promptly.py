import os
import unittest
from promptly import Form
from promptly import StringInput
from promptly import IntegerInput
from promptly import ChoiceInput
from promptly import BooleanInput
from promptly.styles import CSSParser


class TestPromptly(unittest.TestCase):

    def test_session(self):
        form = Form()

        form.add(
            'name',
            StringInput(
                'What is your name?',
                default='Aubrey'
            )
        )

        form.add(
            'age',
            IntegerInput(
                'What is your age?',
                default=1
            )
        )

        form.add(
            'color',
            ChoiceInput(
                'What is your favorite color',
                zip(range(1, 4), ('red', 'green', 'blue')),
                default=1
            )
        )

        form.add('yaks', BooleanInput('Do you like yaks?', default=True))

    def test_convert_dict(self):

        form = Form()

        form.add(
            'name',
            StringInput(
                'What is your name?',
                default='Aubrey'
            )
        )

        form.add(
            'age',
            IntegerInput(
                'What is your age?',
                default=1
            )
        )

        form.add(
            'color',
            ChoiceInput(
                'What is your favorite color',
                zip(range(1, 4), ('red', 'green', 'blue')),
                default=1
            )
        )

        form.add('yaks', BooleanInput('Do you like yaks?', default=True))
        form.run(prefix='[promptly] ')

        d = dict(form)
        print(d)

    def test_css_parser(self):
        css = None
        filename = os.path.abspath('./tests/resources/stylesheet.css')

        with open(filename) as f:
            css = f.read()

        data = CSSParser.parse_string(css)
        print data

    def test_sugar(self):
        form = Form()
        form.add.string(
            'name',
            'What is your name?',
            default='Aubrey'
        ).add.int(
            'age',
            'What is your age?',
            default=1
        ).add.choice(
            'color',
            'What is your favorite color?',
            zip(range(1, 4), ('red', 'green', 'blue')),
            default=1
        ).add.bool(
            'yaks',
            'Do you like yaks?',
            default=True
        )

        form.run(prefix='[sugar] :: ')
        d = dict(form)

        print(d)
