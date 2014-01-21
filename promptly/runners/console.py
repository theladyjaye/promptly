import sys
import signal

# on windows pyreadline will be installed
# pyreadline installs a file under the name
# readline.py in site-packages
import readline

from promptly.styles import Style
from promptly.styles import AnsiStyle
from promptly.utils import prepare_stylesheet
from promptly.renderers import console
from promptly.compat import input as get_input
from promptly import Notification


def run(form, prefix=None, stylesheet=None):
    runner = ConsoleRunner(form, prefix=prefix, stylesheet=stylesheet)
    runner.run()


def notification(text, prefix=None, stylesheet=None):
    styles = prepare_stylesheet(stylesheet)
    prefix = '' if prefix is None else prefix
    message = Notification(text)

    obj = console.NotificationPrompt(
        runner=None,
        input=message,
        prefix=prefix,
        stylesheet=styles)

    sys.stdout.write('\n%s' % obj.prompt)
    sys.stdout.flush()


class ConsoleRunner(object):

    def __init__(self, form, prefix=None, stylesheet=None):
        self.form = form
        self.prefix = '' if prefix is None else prefix
        self.stylesheet = prepare_stylesheet(stylesheet)
        signal.signal(signal.SIGINT, self._on_sigint)

    # signal handlers
    def _on_sigint(self, signal, frame):
        sys.stdout.write(Style.reset_all)
        print ('\nYou Quit! You\'re a quitter! Boo!\n')
        sys.exit(0)

    def branch(self, label, input):
        input(self.form)

    def notification(self, label, input, prefix=True):
        obj = self.factory(console.NotificationPrompt, input)

        if not prefix:
            obj.prefix = ''

        return obj

    def string(self, label, input):
        return self.factory(console.StringPrompt, input)

    def boolean(self, label, input):
        return self.factory(console.BooleanPrompt, input)

    def select(self, label, input):
        return self.factory(console.SelectPrompt, input)

    def multiselect(self, label, input):
        return self.factory(console.MultiSelectPrompt, input)

    def integer(self, label, input):
        return self.factory(console.IntegerPrompt, input)

    def factory(self, cls, input):
        return cls(self, input, self.prefix, self.stylesheet)

    def loop(self):
        while 1:
            result = None
            prompt = (yield)

            while 1:
                if isinstance(prompt, console.NotificationPrompt):
                    footer_style = prompt.footer_style
                    seperator = prompt.seperator
                    wrap = footer_style(seperator.ljust(3, seperator))

                    notification = '\n%s\n%s\n%s\n' % \
                                   (wrap, prompt.prompt, wrap)

                    sys.stdout.write(notification)
                    break

                result = self.render(
                    prompt.prompt,
                    default=prompt.default)

                result = prompt.apply_default(result)

                try:
                    result = prompt.process_value(result)
                except:
                    continue
                break
            yield result

    def run(self):
        loop = self.loop()
        next(loop)

        for label, input in iter(self.form._fields):
            key = input.__class__.__name__.lower()
            prompt = getattr(self, key)(label, input)
            if prompt:
                data = loop.send(prompt)
                input.value = data
                next(loop)

    def prompt_format(self, prompt):
        stylesheet = self.stylesheet
        styles_action = Style.styles_for_key('action', stylesheet)
        styles_input = Style.styles_for_key('input', stylesheet)

        # there appears to be an issue when feeding the whole
        # prompt to input/raw_input (py3 and py2 respectively)
        # So we send the text part of the prompt to stdout
        # and only actualy have the single line with the
        # prompt/default go to input/raw_input
        sys.stdout.write('\n%s\n' % prompt)

        return '%(action)s%(input)s' % {
            'action': styles_action('> '),
            'input': styles_input.color +
            styles_input.background_color +
            styles_input.font_weight
        }

    def render(self, value, default=None):
        # http://stackoverflow.com/questions/2533120/show-default-value-for-editing-on-python-input-possible/2533142#2533142
        # http://stackoverflow.com/questions/3327524/crossplatform-method-for-inserting-text-into-raw-input-to-avoid-readine-in-pyt
        # windows: https://pypi.python.org/pypi/readline
        #          https://pypi.python.org/pypi/pyreadline/2.0
        #
        # Under windows we don't get the set_startup_hook functionality
        # So the defaults will not be displayed.
        # The prompts will be rendered differently for windows based clients

        result = None
        if default:
            readline.set_startup_hook(lambda: readline.insert_text(default))
            try:
                result = get_input(self.prompt_format(value))
            finally:
                readline.set_startup_hook()
        else:
            result = get_input(self.prompt_format(value))

        sys.stdout.write(AnsiStyle.RESET_ALL)
        return result
