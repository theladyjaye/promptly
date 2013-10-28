import sys
import signal
import readline
from promptly.styles import Style
from promptly.utils import prepare_stylesheet
from promptly.renderers import console
from promptly.compat import input as get_input


def run(form, prefix=None, stylesheet=None):
    runner = ConsoleRunner(form, prefix=prefix, stylesheet=stylesheet)
    runner.run()


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
        loop.next()

        for label, input in iter(self.form._fields):
            key = input.__class__.__name__.lower()
            prompt = getattr(self, key)(label, input)
            data = loop.send(prompt)
            input.value = data
            loop.next()

    def prompt_format(self, prompt):
        stylesheet = self.stylesheet
        styles_action = Style.styles_for_key('action', stylesheet)
        styles_input = Style.styles_for_key('input', stylesheet)

        return '\n%(prompt)s\n%(action)s%(input)s' % {
            'prompt': prompt,
            'action': styles_action('> '),
            'input': styles_input.color + \
                     styles_input.background_color + \
                     styles_input.font_weight
        }

    def render(self, value, default=None):
        # http://stackoverflow.com/questions/2533120/show-default-value-for-editing-on-python-input-possible/2533142#2533142
        result = None
        if default:
            readline.set_startup_hook(lambda: readline.insert_text(default))
            try:
                result = get_input(self.prompt_format(value))
            finally:
                readline.set_startup_hook()
        else:
            result = get_input(self.prompt_format(value))

        return result
