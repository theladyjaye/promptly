# -*- coding: utf-8 -*-
import sys
from .compat import input
from .styles import Style
from .utils import numeric_options


class Branch(object):
    def __init__(self, handler, *args, **kwargs):
        self.handler = handler
        self.args = args
        self.kwargs = kwargs

    def __call__(self, form, prefix=None, stylesheet=None):
        branch = self.handler(form, *self.args, **self.kwargs)

        if not branch:
            return

        index = form._fields.index((id(self), self)) + 1

        for each in iter(branch._fields):
            form._fields.insert(index, each)
            index = index + 1


class BaseInput(object):

    def __init__(self, label, validators=None, default=None, notifications=()):
        self.label = label
        self.default = default
        self.validators = validators
        self.notifications = map(Notification, notifications)
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
            data = self.apply_default(input('\n%s ' % prompt))

            try:
                self.process_data(data)
            except:
                continue

            if self.validate(self.value):
                break
            else:
                sys.stdout.write('Sorry invalid input\n')
                continue


class Notification(BaseInput):
    pass


class String(BaseInput):
    pass


class Integer(BaseInput):

    def __init__(self, label, validators=None, **kwargs):
        super(Integer, self).__init__(label, validators, **kwargs)


class Boolean(BaseInput):
    def __init__(self, label, default=True, **kwargs):
        super(Boolean, self).__init__(label, default=default, **kwargs)


class Select(BaseInput):

    def __init__(self, label, choices, option_format=numeric_options, **kwargs):
        super(Select, self).__init__(label, **kwargs)
        self.choices = option_format(choices)


class MultiSelect(Select):

    def __init__(self, label, choices, done_label='Done', option_format=numeric_options, **kwargs):
        options = list(choices)
        options += (done_label, )
        super(MultiSelect, self).__init__(label, options, option_format, **kwargs)
        self.value = set()

    def build_prompt(self, prefix, stylesheet):
        styles_prefix = self.styles_for_key('prefix', stylesheet)
        styles_label = self.styles_for_key('choices.label', stylesheet)
        styles_default_wrapper = self.styles_for_key('choices.default_wrapper', stylesheet)
        styles_default_value = self.styles_for_key('choices.default_value', stylesheet)
        styles_option_key = self.styles_for_key('choices.option_key', stylesheet)
        styles_option_value = self.styles_for_key('choices.option_value', stylesheet)
        styles_seperator = self.styles_for_key('choices.seperator', stylesheet)
        styles_action = self.styles_for_key('choices.action', stylesheet)
        styles_selection = self.styles_for_key('choices.selection', stylesheet)

        prompt = '%s\n' % styles_label(self.label)

        choices = []
        choices_count = len(self.choices)

        for i, each in enumerate(self.choices):
            key, value = each
            prefix = '[ ] '

            if i == (choices_count - 1):
                prefix = ''
            elif each in self.value:
                prefix = '[%s] ' % styles_selection('x')

            choices.append('%s%s %s' % (
                styles_option_key(key),
                styles_seperator(')'),
                styles_option_value('%s%s' % (prefix, value))))

        prompt = '%s%s\n%s%s' % (
            prompt,
            '\n'.join(choices),
            styles_prefix(prefix),
            styles_action('Select Options'))

        if self.default:
            prompt = '%s %s%s%s' % (prompt,
                styles_default_wrapper('['),
                styles_default_value(self.default),
                styles_default_wrapper(']'))

        return prompt

    def __call__(self, form, prefix=None, stylesheet=None):

        choices_count = len(self.choices)

        while 1:
            prompt = '%s' % (self.build_prompt(
                prefix=prefix,
                stylesheet=stylesheet))

            data = self.apply_default(input('\n%s ' % prompt))

            try:
                obj = next(x for x in self.choices if str(x[0]) == str(data))
            except StopIteration:
                continue

            if self.choices.index(obj) == (choices_count - 1):
                self.value = list(self.value)
                break

            if obj in self.value:
                self.value = self.value - frozenset([obj])
                continue

            try:
                self.process_data(data)
            except:
                continue

    def process_data(self, data):
        result = [x for x in self.choices if str(x[0]) == str(data)]

        if not result:
            raise ValueError

        self.value.add(result[0])


