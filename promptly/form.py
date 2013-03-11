# -*- coding: utf-8 -*-
from collections import OrderedDict


class Form(object):

    def __init__(self):
        self._fields = OrderedDict()

    def add(self, key, obj):
        self._fields[key] = obj

    def prompt(self):
        for prompt in self._fields.itervalues():
            prompt()

    def values(self):
        for prompt in self._fields.itervalues():
            yield prompt.value

    def __iter__(self):
        for k, v in self._fields.iteritems():
            yield k, v.value

    def __getattr__(self, key):
        try:
            return self._fields[key]
        except KeyError:
            raise AttributeError
