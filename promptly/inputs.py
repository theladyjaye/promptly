# -*- coding: utf-8 -*-
import sys


class BaseInput(object):

    def __init__(self, label, validators=None, default=None):
        self.label = label
        self.default = default
        self.validators = validators
        self.value = None

    def build_prompt(self):
        prompt = self.label

        if self.default:
            prompt = '%s [%s]' % (prompt, self.default)

        return prompt

    def apply_default(self, data):
        if len(data) == 0 and self.default:
            return self.default

        return data

    def process_data(self, data):
        self.value = data

    def validate(self, input):
        return True

    def __call__(self):
        prompt = self.build_prompt()

        while 1:
            data = self.apply_default(raw_input('%s ' % prompt))

            try:
                self.process_data(data)
            except:
                continue

            if self.validate(self.value):
                break
            else:
                sys.stdout.write('Sorry invalid input\n')
                continue


class StringInput(BaseInput):
    pass


class IntegerInput(BaseInput):

    def __init__(self, label, validators=None, **kwargs):
        super(IntegerInput, self).__init__(label, validators, **kwargs)

    def process_data(self, data):
        try:
            self.value = int(data)
        except ValueError:
            self.value = None
            raise


class BooleanInput(BaseInput):
    def __init__(self, label, default=True, **kwargs):
        super(BooleanInput, self).__init__(label, default=default, **kwargs)

    def build_prompt(self):
        prompt = self.label

        if self.default:
            prompt = '%s [Y/n]' % (prompt)
        else:
            prompt = '%s [y/N]' % (prompt)

        return prompt

    def apply_default(self, data):
        if len(data) == 0:
            return self.default

        return data

    def process_data(self, data):
        boolean_states = {
        True: True, '1': True, 'yes': True, 'true': True, 'on': True, 'y': True, 't': True,
        False: False, '0': False, 'no': False, 'false': False, 'off': False, 'n': False, 'f': False
        }

        candidate = data.lower() if type(data) == str else data

        try:
            self.value = boolean_states[candidate]
        except KeyError:
            raise


class ChoiceInput(BaseInput):

    def __init__(self, label, choices, **kwargs):
        super(ChoiceInput, self).__init__(label, **kwargs)
        self.choices = choices

    def build_prompt(self):
        prompt = '%s\n' % self.label

        choices = []
        for key, value in self.choices:
            choices.append('%s) %s' % (key, value))

        prompt = '%s%s\nSelect Option' % (prompt, '\n'.join(choices))

        if self.default:
            prompt = '%s [%s]' % (prompt, self.default)

        return prompt

    def process_data(self, data):
        try:
            self.value = int(data)
        except ValueError:
            self.value = None
            raise



