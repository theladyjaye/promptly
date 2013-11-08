from __future__ import unicode_literals
import sys
from promptly.styles import Style
from promptly.compat import unichr
from promptly.compat import unicode
from .core import Prompt


class ConsolePrompt(Prompt):
    def __init__(self, runner, input, prefix, stylesheet):
        self.runner = runner
        self.input = input
        self.prefix = prefix
        self.stylesheet = stylesheet

    @property
    def default(self):
        if self.input.default:
            return str(self.input.default)
        return None

    @property
    def seperator(self):
        return unichr(0x00b7)

    @property
    def footer_style(self):
        return Style.styles_for_key('notification.footer', self.stylesheet)

    def append_notifications(self, prompt, notifications):
        styles_footer = self.footer_style

        notices = []
        dot = self.seperator

        for each in notifications:
            x = self.runner.notification('', each, prefix=False)
            notices.append(x.prompt.rjust(len(self.prefix), ' '))

        if notices:
            prompt = '%s\n%s' % (prompt, '\n'.join(notices))
            prompt = '%s\n%s' % (prompt, styles_footer(dot.ljust(3, dot)))

        return prompt


class NotificationPrompt(ConsolePrompt):

    @property
    def prompt(self):
        input = self.input
        stylesheet = self.stylesheet
        prefix = self.prefix

        styles_prefix = Style.styles_for_key('prefix', stylesheet)
        styles_label = Style.styles_for_key('notification.label', stylesheet)

        return '%s%s' % (styles_prefix(prefix),
                         styles_label(input.label))


class StringPrompt(ConsolePrompt):
    @property
    def prompt(self):
        input = self.input
        stylesheet = self.stylesheet
        prefix = self.prefix

        styles_prefix = Style.styles_for_key('prefix', stylesheet)
        styles_label = Style.styles_for_key('string.label', stylesheet)

        styles_default_wrapper = Style.styles_for_key(
            'string.default_wrapper', stylesheet)

        styles_default_value = Style.styles_for_key(
            'string.default_value', stylesheet)

        if not input.default:
            prompt = '%s%s' % (styles_prefix(prefix),
                               styles_label(input.label))
        else:
            try:
                # pyreadline does not support set_startup_hook
                # so we do the next best thing when it comes to defaults
                import pyreadline
                prompt = '%s%s %s%s%s' % (
                    styles_prefix(prefix),
                    styles_label(input.label),
                    styles_default_wrapper('['),
                    styles_default_value(input.default),
                    styles_default_wrapper(']'))
            except ImportError:
                prompt = '%s%s' % (styles_prefix(prefix),
                                   styles_label(input.label))

        return self.append_notifications(prompt, input.notifications)


class IntegerPrompt(ConsolePrompt):
    def process_value(self, value):
        try:
            return int(value)
        except ValueError:
            raise

    @property
    def prompt(self):
        input = self.input
        stylesheet = self.stylesheet
        prefix = self.prefix

        styles_prefix = Style.styles_for_key('prefix', stylesheet)
        styles_label = Style.styles_for_key('integer.label', stylesheet)

        styles_default_wrapper = Style.styles_for_key(
            'integer.default_wrapper', stylesheet)

        styles_default_value = Style.styles_for_key(
            'integer.default_value', stylesheet)

        if not input.default:
            prompt = '%s%s' % (styles_prefix(prefix),
                               styles_label(input.label))

        else:
            try:
                # pyreadline does not support set_startup_hook
                # so we do the next best thing when it comes to defaults
                import pyreadline
                prompt = '%s%s %s%s%s' % (
                    styles_prefix(prefix),
                    styles_label(input.label),
                    styles_default_wrapper('['),
                    styles_default_value(input.default),
                    styles_default_wrapper(']'))
            except ImportError:
                prompt = '%s%s' % (styles_prefix(prefix),
                                   styles_label(input.label))

        return self.append_notifications(prompt, input.notifications)


class BooleanPrompt(ConsolePrompt):

    def process_value(self, value):
        boolean_states = {
        True: True, '1': True, 'yes': True, 'true': True, 'on': True, 'y': True, 't': True,
        False: False, '0': False, 'no': False, 'false': False, 'off': False, 'n': False, 'f': False
        }

        candidate = value.lower() if type(value) == str else value

        try:
            return boolean_states[candidate]
        except KeyError:
            raise

    @property
    def default(self):
        return None

    @property
    def prompt(self):
        input = self.input
        stylesheet = self.stylesheet
        prefix = self.prefix

        styles_prefix = Style.styles_for_key('prefix', stylesheet)
        styles_label = Style.styles_for_key('boolean.label', stylesheet)

        styles_default_wrapper = Style.styles_for_key(
            'boolean.default_wrapper', stylesheet)

        styles_default_value = Style.styles_for_key(
            'boolean.default_value', stylesheet)

        styles_other_value = Style.styles_for_key(
            'boolean.other_value', stylesheet)

        styles_seperator = Style.styles_for_key(
            'boolean.seperator', stylesheet)

        prompt = styles_label(input.label)

        if input.default:
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


class SelectPrompt(ConsolePrompt):
    @property
    def default(self):
        return None

    def process_value(self, value):
        result = [x for x in self.input.choices if str(x[0]) == str(value)]

        if not result:
            raise ValueError

        return result[0]

    @property
    def prompt(self):
        input = self.input
        stylesheet = self.stylesheet
        prefix = self.prefix

        styles_prefix = Style.styles_for_key('prefix', stylesheet)
        styles_label = Style.styles_for_key('choices.label', stylesheet)
        styles_default_wrapper = Style.styles_for_key(
            'choices.default_wrapper', stylesheet)

        styles_default_value = Style.styles_for_key(
            'choices.default_value', stylesheet)

        styles_option_key = Style.styles_for_key(
            'choices.option_key', stylesheet)

        styles_option_value = Style.styles_for_key(
            'choices.option_value', stylesheet)

        styles_seperator = Style.styles_for_key(
            'choices.seperator', stylesheet)

        styles_action = Style.styles_for_key('choices.action', stylesheet)

        prompt = '%s' % styles_label(input.label)

        choices = []

        border_len = 0
        for key, value in input.choices:
            border_len = max(len(value), border_len)
            choices.append('%s%s %s' % (
                styles_option_key(unicode(key)),
                styles_seperator(')'),
                styles_option_value(value)))

        prompt = '%s%s' % (
            styles_prefix(prefix),
            prompt)

        if input.default:
            prompt = '%s %s%s%s' % (prompt,
                styles_default_wrapper('['),
                styles_default_value(unicode(input.default)),
                styles_default_wrapper(']'))

        prompt = self.append_notifications(prompt, input.notifications)

        dot = unichr(0x00b7)
        styles_notification_footer = Style.styles_for_key(
            'notification.footer', stylesheet)

        prompt = '%s\n%s%s' % (
            prompt,
            '\n'.join(choices),
            styles_notification_footer('\n'.ljust(4, dot)))

        return prompt


class MultiSelectPrompt(ConsolePrompt):
    def __init__(self, runner, input, prefix, stylesheet):
        super(MultiSelectPrompt, self).__init__(runner, input, prefix, stylesheet)
        self.values = set()

    def process_value(self, value):
        choices = self.input.choices
        choices_count = len(choices)

        try:
            obj = next(x for x in choices if str(x[0]) == str(value))
        except StopIteration:
            pass

        # Did we get the "Done" option?
        if choices.index(obj) == (choices_count - 1):
            return tuple(self.values)

        if obj in self.values:
            self.values.remove(obj)
        else:
            self.values.add(obj)

        # force the run loop to contine
        raise Exception

    @property
    def default(self):
        return None

    @property
    def prompt(self):
        input = self.input
        stylesheet = self.stylesheet
        prefix = self.prefix

        styles_prefix = Style.styles_for_key('prefix', stylesheet)
        styles_label = Style.styles_for_key('choices.label', stylesheet)

        styles_default_wrapper = Style.styles_for_key(
            'choices.default_wrapper', stylesheet)

        styles_default_value = Style.styles_for_key(
            'choices.default_value', stylesheet)

        styles_option_key = Style.styles_for_key(
            'choices.option_key', stylesheet)

        styles_option_value = Style.styles_for_key(
            'choices.option_value', stylesheet)

        styles_seperator = Style.styles_for_key(
            'choices.seperator', stylesheet)

        styles_action = Style.styles_for_key(
            'choices.action', stylesheet)

        styles_selection = Style.styles_for_key(
            'choices.selection', stylesheet)

        prompt = '%s' % styles_label(input.label)

        choices = []
        choices_count = len(input.choices)

        prompt = '%s%s' % (
            styles_prefix(prefix),
            prompt)

        for i, each in enumerate(input.choices):
            key, value = each
            prefix = '[ ] '

            if i == (choices_count - 1):
                prefix = ''
            elif each in self.values:
                prefix = '[%s] ' % styles_selection('x')

            choices.append('%s%s %s' % (
                styles_option_key(unicode(key)),
                styles_seperator(')'),
                styles_option_value('%s%s' % (prefix, value))))

        prompt = self.append_notifications(prompt, input.notifications)

        dot = unichr(0x00b7)
        styles_notification_footer = Style.styles_for_key(
            'notification.footer', stylesheet)

        prompt = '%s\n%s%s' % (
            prompt,
            '\n'.join(choices),
            styles_notification_footer('\n'.ljust(4, dot)))

        return prompt
