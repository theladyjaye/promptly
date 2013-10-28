import unittest
from mock import Mock
from promptly import Form
from promptly import inputs

# TODO before 0.4 release
# add tests for multiselect


class TestPromptly(unittest.TestCase):

    def test_form_len(self):
        form = Form()

        form.add.string(
            'name',
            'What is your name?',
            default='Aubrey'
        )

        form.add.int(
            'name',
            'What is your age?'
        )

        self.assertTrue(len(form) == 2)

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

    def test_prompt_select(self):
        returns = ['1']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()

        form.add.select(
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

    def test_prompt_select_default(self):
        returns = ['']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()

        form.add.select(
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
        ).add.select(
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
        ).add.select(
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

    def test_branch(self):
        returns = ['99', 'lucy']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        def branch(form, age, name):
            f = Form()
            f.add.int('age', 'What is your age?', default=age)
            f.add.string('name', 'What is your name?', default=name)
            self.assertTrue(name == 'clark')
            self.assertTrue(age == 1)
            return f

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()
        form.add.branch(branch, 1, name='clark')
        form.run()

        self.assertTrue(input.call_count == 2)
        data = dict(form)

        self.assertTrue(len(form) == 3)
        self.assertTrue(data['name'] == 'lucy')
        self.assertTrue(data['age'] == 99)

    def test_multiselect_select(self):
        # choices get ABC sorted though numeric options_format
        # which is the default
        choices = sorted(('chocolate', 'vanilla', 'apple'))

        # multiselect adds a final option to
        # the list of choices to signify "done"
        # the default "done" id under the standard numeric
        # options format is len(choices) + 1, in this case
        # we have 3 choices above, so the "done" option
        # is 3 + 1 -> 4
        returns = ['1', '3', '4']

        def side_effect(*args):
            result = returns.pop(0)
            return result

        input = Mock(side_effect=side_effect)
        inputs.input = input

        form = Form()
        form.add.multiselect(
            'flavors',
            'Select your favorite flavors',
            choices)
        form.run()

        self.assertTrue(input.call_count == 3)
        data = dict(form)

        self.assertTrue(len(form.flavors.value) == 2)
        self.assertTrue((1, 'apple') in data['flavors'])
        self.assertTrue((3, 'vanilla') in data['flavors'])

    def test_runner(self):
        from promptly import runners
        form = Form()
        form.add.int('age', 'What is your Age?', default=21, notifications=(
            'This will be used to help guide your experince',
            'Additionally you will be a winner!'))

        form.add.string('name', 'What is your Name?', default='Clark')
        form.add.bool('likes_dogs', 'Do you like Dogs?', default=True)
        form.add.select('dog', 'Which dog do you like?',
            choices=('Lucy', 'Ollie', 'Dexter', 'Tucker'),
            default=3,
            notifications=('Hint, all of them are great!',))

        form.add.select('dog2', 'Which dog do you like?',
            choices=('Lucy', 'Ollie', 'Dexter', 'Tucker'),
            default=3)

        runners.console(form, '')
        data = dict(form)
        from pprint import pprint
        pprint(data)

        # form.add.multiselect(
        #     'flavors',
        #     'Select your favorite flavors',
        #     choices)
        # form.run()
