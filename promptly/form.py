# -*- coding: utf-8 -*-
import pkg_resources
from collections import OrderedDict
from .styles import CSSParser


class Form(object):

    def __init__(self):
        self._fields = OrderedDict()

    def add(self, key, obj):
        self._fields[key] = obj

    def run(self, prefix=None, stylesheet=None):
        styles = None

        if stylesheet:
            styles = CSSParser.parse_string(stylesheet)
        else:
            stream = pkg_resources \
            .resource_stream('promptly.resources','default.css')

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
