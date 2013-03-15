# -*- coding: utf-8 -*-
import signal
import sys

import pkg_resources
from collections import OrderedDict
from .styles import CSSParser

from .inputs import StringInput
from .inputs import IntegerInput
from .inputs import ChoiceInput
from .inputs import BooleanInput


class AddAction(object):

    def __init__(self, form):
        self.form = form

    def __call__(self, key, obj):
        self.form._fields[key] = obj

    def string(self, key, label, **kwargs):
        obj = StringInput(label, **kwargs)
        self.form._add(key, obj)
        return self.form

    def int(self, key, label, **kwargs):
        obj = IntegerInput(label, **kwargs)
        self.form._add(key, obj)
        return self.form

    def choice(self, key, label, choices, **kwargs):
        obj = ChoiceInput(label, choices, **kwargs)
        self.form._add(key, obj)
        return self.form

    def bool(self, key, label, **kwargs):
        obj = BooleanInput(label, **kwargs)
        self.form._add(key, obj)
        return self.form


class Form(object):
    @property
    def add(self):
        action = AddAction(self)
        return action

    def __init__(self):
        self._fields = OrderedDict()
        signal.signal(signal.SIGINT, self._on_sigint)

    def _add(self, key, obj):
        self._fields[key] = obj

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

        for prompt in self._fields.itervalues():
            prompt(prefix=prefix, stylesheet=styles)

    def __iter__(self):
        for k, v in self._fields.iteritems():
            yield k, v.value

    def __getattr__(self, key):
        try:
            return self._fields[key]
        except KeyError:
            raise AttributeError

    # signal handlers
    def _on_sigint(self, signal, frame):
        print " You Quit! You're a quitter! Boo!"
        sys.exit(0)
