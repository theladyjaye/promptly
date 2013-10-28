# -*- coding: utf-8 -*-
from .utils import numeric_options


class Branch(object):
    def __init__(self, handler, *args, **kwargs):
        self.handler = handler
        self.args = args
        self.kwargs = kwargs

    def __call__(self, form):
        branch = self.handler(form, *self.args, **self.kwargs)

        if not branch:
            return

        index = form._fields.index((id(self), self)) + 1

        for each in iter(branch._fields):
            form._fields.insert(index, each)
            index = index + 1


class BaseInput(object):

    def __init__(self, label, default=None, notifications=()):
        self.label = label
        self.default = default
        self.notifications = map(Notification, notifications)
        self.value = None


class Notification(BaseInput):
    pass


class String(BaseInput):
    pass


class Integer(BaseInput):
    pass


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


