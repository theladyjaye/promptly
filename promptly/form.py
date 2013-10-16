# -*- coding: utf-8 -*-
import sys
import signal
import pkg_resources
from .styles import CSSParser
from .inputs import StringInput
from .inputs import IntegerInput
from .inputs import SelectInput
from .inputs import BooleanInput
from .inputs import MultiSelectInput
from .inputs import Branch
from .utils import numeric_options


class AddAction(object):

    def __init__(self, form):
        self.form = form

    def __call__(self, key, obj):
        self.form._fields.append((key, obj))

    def string(self, key, label, **kwargs):
        obj = StringInput(label, **kwargs)
        self.form._add(key, obj)
        return self.form

    def int(self, key, label, **kwargs):
        obj = IntegerInput(label, **kwargs)
        self.form._add(key, obj)
        return self.form

    def select(self, key, label, choices, option_format=numeric_options, **kwargs):
        obj = SelectInput(label, choices, option_format, **kwargs)
        self.form._add(key, obj)
        return self.form

    def multiselect(self, key, label, choices, done_label='Done', option_format=numeric_options, **kwargs):
        obj = MultiSelectInput(label, choices, done_label, option_format, **kwargs)
        self.form._add(key, obj)
        return self.form

    def bool(self, key, label, **kwargs):
        obj = BooleanInput(label, **kwargs)
        self.form._add(key, obj)
        return self.form

    def branch(self, handler, *args, **kwargs):
        obj = Branch(handler, *args, **kwargs)
        self.form._add(id(obj), obj)
        return self.form


class Form(object):

    @property
    def add(self):
        action = AddAction(self)
        return action

    def __init__(self):
        self._fields = []
        signal.signal(signal.SIGINT, self._on_sigint)

    def _add(self, key, obj):
        self._fields.append((key, obj))

    def run(self, prefix=None, stylesheet=None):
        styles = None

        if stylesheet:
            styles = CSSParser.parse_string(stylesheet)
        else:
            stream = pkg_resources.resource_stream(
                'promptly.resources',
                'default.css'
            )

            styles = CSSParser.parse_string(stream.read())

        for label, input in iter(self._fields):
            input(form=self, prefix=prefix, stylesheet=styles)

    def __len__(self):
        return len(self._fields)

    def __iter__(self):
        for k, v in iter(self._fields):
            if not isinstance(v, Branch):
                yield k, v.value

    def __getattr__(self, key):
        try:
            # we were using an ordereddict so access was pretty close to
            # O(1), switched to lists in order to facilitate branching
            # this lookup will be O(N)
            return next(x[1] for x in self._fields if x[0] == key)
        except StopIteration:
            raise AttributeError

    # signal handlers
    def _on_sigint(self, signal, frame):
        print ('You Quit! You\'re a quitter! Boo!')
        sys.exit(0)
