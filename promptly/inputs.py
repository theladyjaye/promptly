# -*- coding: utf-8 -*-
import sys
from .compat import input, iteritems
from .styles import Style


class Fork(object):
    def __init__(self, key, handler, *args, **kwargs):
        self.key = key
        self.handler = handler
        self.args = args
        self.kwargs = kwargs

    def __call__(self, form, prefix=None, stylesheet=None):
        value = getattr(form, self.key).value
        fork = self.handler(value, *self.args, **self.kwargs)

        for k, v in iteritems(fork._fields):
            form._add(k, v)


class BaseInput(object):

    def __init__(self, label, validators=None, default=None, prefix=None):
        self.label = label
        self.default = default
        self.validators = validators
        self.value = None

    def styles_for_key(self, key, stylesheet):
        styles = {}
        context = stylesheet

        try:
            styles.update(context['selectors']['body']['value'])
        except KeyError:
            pass

        for part in key.split('.'):
            try:
                context = context['selectors'][part]
                styles.update(context['value'])

            except KeyError:
                break

        return Style(styles)

    def build_prompt(self, stylesheet=None):
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

    def __call__(self, form, prefix=None, stylesheet=None):
        prompt = '%s' % (self.build_prompt(
            prefix=prefix,
            stylesheet=stylesheet))

        while 1:
            data = self.apply_default(input('%s ' % prompt))

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

    def build_prompt(self, prefix, stylesheet):
        styles_prefix = self.styles_for_key('prefix', stylesheet)
        styles_label = self.styles_for_key('string.label', stylesheet)
        styles_default_wrapper = self.styles_for_key('string.default_wrapper', stylesheet)
        styles_default_value = self.styles_for_key('string.default_value', stylesheet)

        if self.default:
            return '%s%s %s%s%s' % (
                styles_prefix(prefix),
                styles_label(self.label),
                styles_default_wrapper('['),
                styles_default_value(self.default),
                styles_default_wrapper(']'))

        return '%s%s' % (styles_prefix(prefix),
                         styles_label(self.label))


class IntegerInput(BaseInput):

    def __init__(self, label, validators=None, **kwargs):
        super(IntegerInput, self).__init__(label, validators, **kwargs)

    def build_prompt(self, prefix, stylesheet):
        styles_prefix = self.styles_for_key('prefix', stylesheet)
        styles_label = self.styles_for_key('integer.label', stylesheet)
        styles_default_wrapper = self.styles_for_key('integer.default_wrapper', stylesheet)
        styles_default_value = self.styles_for_key('integer.default_value', stylesheet)

        if self.default:
            return '%s%s %s%s%s' % (
                styles_prefix(prefix),
                styles_label(self.label),
                styles_default_wrapper('['),
                styles_default_value(self.default),
                styles_default_wrapper(']'))

        return '%s%s' % (styles_prefix(prefix),
                         styles_label(self.label))

    def process_data(self, data):
        try:
            self.value = int(data)
        except ValueError:
            self.value = None
            raise


class BooleanInput(BaseInput):
    def __init__(self, label, default=True, **kwargs):
        super(BooleanInput, self).__init__(label, default=default, **kwargs)

    def build_prompt(self, prefix, stylesheet):
        styles_prefix = self.styles_for_key('prefix', stylesheet)
        styles_label = self.styles_for_key('boolean.label', stylesheet)
        styles_default_wrapper = self.styles_for_key('boolean.default_wrapper', stylesheet)
        styles_default_value = self.styles_for_key('boolean.default_value', stylesheet)
        styles_other_value = self.styles_for_key('boolean.other_value', stylesheet)
        styles_seperator = self.styles_for_key('boolean.seperator', stylesheet)

        prompt = styles_label(self.label)

        if self.default:
            prompt = '%s%s %s%s%s%s%s' % (
                styles_prefix(prefix),
                prompt,
                styles_default_wrapper('['),
                styles_default_value('Y'),
                styles_seperator('/'),
                styles_other_value('n'),
                styles_default_wrapper(']'))
        else:
            prompt = '%s%s %s%s%s%s%s' % (
                styles_prefix(prefix),
                prompt,
                styles_default_wrapper('['),
                styles_other_value('y'),
                styles_seperator('/'),
                styles_default_value('N'),
                styles_default_wrapper(']'))

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
        self.choices = list(choices)

    def build_prompt(self, prefix, stylesheet):
        styles_prefix = self.styles_for_key('prefix', stylesheet)
        styles_label = self.styles_for_key('choices.label', stylesheet)
        styles_default_wrapper = self.styles_for_key('choices.default_wrapper', stylesheet)
        styles_default_value = self.styles_for_key('choices.default_value', stylesheet)
        styles_option_key = self.styles_for_key('choices.option_key', stylesheet)
        styles_option_value = self.styles_for_key('choices.option_value', stylesheet)
        styles_seperator = self.styles_for_key('choices.seperator', stylesheet)
        styles_action = self.styles_for_key('choices.action', stylesheet)

        prompt = '%s\n' % styles_label(self.label)

        choices = []
        for key, value in self.choices:
            choices.append('%s%s %s' % (
                styles_option_key(key),
                styles_seperator(')'),
                styles_option_value(value)))

        prompt = '%s%s\n%s%s' % (
            prompt,
            '\n'.join(choices),
            styles_prefix(prefix),
            styles_action('Select Option'))

        if self.default:
            prompt = '%s %s%s%s' % (prompt,
                styles_default_wrapper('['),
                styles_default_value(self.default),
                styles_default_wrapper(']'))

        return prompt

    def process_data(self, data):
        result = [x for x in self.choices if str(x[0]) == str(data)]

        if not result:
            raise ValueError

        self.value = result[0]
