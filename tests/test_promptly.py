import unittest
from mock import Mock
from promptly import Form
from promptly import inputs


class TestPromptly(unittest.TestCase):

    def test_prompt_string(self):
        returns = ['lucy']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()

        form.add.string(
            'name',
            'What is your name?',
            default='Aubrey'
        )

        form.run()

        self.assertTrue(input.call_count == 1)
        data = dict(form)

        self.assertTrue(data['name'] == 'lucy')

    def test_prompt_string_default(self):
        returns = ['']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()

        form.add.string(
            'name',
            'What is your name?',
            default='lucy'
        )

        form.run()

        self.assertTrue(input.call_count == 1)
        data = dict(form)

        self.assertTrue(data['name'] == 'lucy')

    def test_prompt_int(self):
        returns = ['22']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()

        form.add.int(
            'age',
            'What is your age?',
            default='5'
        )

        form.run()

        self.assertTrue(input.call_count == 1)
        data = dict(form)

        self.assertTrue(data['age'] == 22)

    def test_prompt_int_default(self):
        returns = ['']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()

        form.add.int(
            'age',
            'What is your age?',
            default=5
        )

        form.run()

        self.assertTrue(input.call_count == 1)
        data = dict(form)

        self.assertTrue(data['age'] == 5)

    def test_prompt_choice(self):
        returns = ['1']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()

        form.add.choice(
            'color',
            'What is your favorite color?',
            ('red', 'green', 'blue'),
            default=2
        )

        form.run()

        self.assertTrue(input.call_count == 1)
        data = dict(form)

        self.assertTrue(data['color'][0] == 1)
        self.assertTrue(data['color'][1] == 'red')

    def test_prompt_choice_default(self):
        returns = ['']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()

        form.add.choice(
            'color',
            'What is your favorite color?',
            ('red', 'green', 'blue'),
            default=2
        )

        form.run()

        self.assertTrue(input.call_count == 1)
        data = dict(form)

        self.assertTrue(data['color'][0] == 2)
        self.assertTrue(data['color'][1] == 'green')

    def test_prompt_bool_false(self):
        returns = ['0', 'no', 'false', 'off', 'n', 'f']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()

        form.add.bool(
            'yaks0',
            'Do you likes yaks?',
            default=True
        ).add.bool(
            'yaks1',
            'Do you likes yaks?',
            default=True
        ).add.bool(
            'yaks2',
            'Do you likes yaks?',
            default=True
        ).add.bool(
            'yaks3',
            'Do you likes yaks?',
            default=True
        ).add.bool(
            'yaks4',
            'Do you likes yaks?',
            default=True
        ).add.bool(
            'yaks5',
            'Do you likes yaks?',
            default=True
        )

        form.run()
        self.assertTrue(input.call_count == 6)
        data = dict(form)

        self.assertTrue(data['yaks0'] == False)
        self.assertTrue(data['yaks1'] == False)
        self.assertTrue(data['yaks2'] == False)
        self.assertTrue(data['yaks3'] == False)
        self.assertTrue(data['yaks4'] == False)
        self.assertTrue(data['yaks5'] == False)

    def test_prompt_bool_true(self):
        returns = ['1', 'yes', 'true', 'on', 'y', 't']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()

        form.add.bool(
            'yaks0',
            'Do you likes yaks?',
            default=False
        ).add.bool(
            'yaks1',
            'Do you likes yaks?',
            default=False
        ).add.bool(
            'yaks2',
            'Do you likes yaks?',
            default=False
        ).add.bool(
            'yaks3',
            'Do you likes yaks?',
            default=False
        ).add.bool(
            'yaks4',
            'Do you likes yaks?',
            default=False
        ).add.bool(
            'yaks5',
            'Do you likes yaks?',
            default=False
        )

        form.run()
        self.assertTrue(input.call_count == 6)
        data = dict(form)

        self.assertTrue(data['yaks0'] == True)
        self.assertTrue(data['yaks1'] == True)
        self.assertTrue(data['yaks2'] == True)
        self.assertTrue(data['yaks3'] == True)
        self.assertTrue(data['yaks4'] == True)
        self.assertTrue(data['yaks5'] == True)

    def test_prompt_bool_true_default(self):
        returns = ['']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()

        form.add.bool(
            'yaks',
            'Do you likes yaks?',
            default=True
        )

        form.run()
        self.assertTrue(input.call_count == 1)
        data = dict(form)

        self.assertTrue(data['yaks'] == True)

    def test_prompt_bool_false_default(self):
        returns = ['']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()

        form.add.bool(
            'yaks',
            'Do you likes yaks?',
            default=False
        )

        form.run()
        self.assertTrue(input.call_count == 1)
        data = dict(form)

        self.assertTrue(data['yaks'] == False)

    def test_prompt_loop_simple(self):
        returns = ['ollie', '22', 'n', '']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()

        form.add.string(
            'name',
            'What is your name?',
            default='Aubrey'
        ).add.int(
            'age',
            'What is your age?',
            default=1
        ).add.bool(
            'yaks',
            'Do you like yaks?',
            default=True
        ).add.choice(
            'color',
            'What is your favorite color?',
            ('red', 'green', 'blue'),
            default=2
        )

        form.run()

        self.assertTrue(input.call_count == 4)
        data = dict(form)

        self.assertTrue(data['name'] == 'ollie')
        self.assertTrue(data['age'] == 22)
        self.assertTrue(data['yaks'] == False)
        self.assertTrue(data['color'][0] == 2)
        self.assertTrue(data['color'][1] == 'green')

    def test_prompt_loop_repeat(self):
        returns = ['lucy', 'foo', 'bar', '99', 'y', '3']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()

        form.add.string(
            'name',
            'What is your name?',
            default='Aubrey'
        ).add.int(
            'age',
            'What is your age?',
            default=1
        ).add.bool(
            'yaks',
            'Do you like yaks?',
            default=True
        ).add.choice(
            'color',
            'What is your favorite color?',
            ('red', 'green', 'blue'),
            default=2
        )

        form.run()

        self.assertTrue(input.call_count == 6)
        data = dict(form)

        self.assertTrue(data['name'] == 'lucy')
        self.assertTrue(data['age'] == 99)
        self.assertTrue(data['yaks'] == True)
        self.assertTrue(data['color'][0] == 3)
        self.assertTrue(data['color'][1] == 'blue')
