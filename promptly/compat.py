import sys
import six
from six.moves import input


if six.PY3:
    unichr = chr
    unicode = str
    string_types = str
else:
    unichr = unichr
    unicode = unicode
    string_types = basestring


def iteritems(value):
    return six.iteritems(value)


def itervalues(value):
    return six.itervalues(value)


def input_compat(prompt):
    if six.PY2:
        return input(prompt.encode(sys.stdout.encoding))
    else:
        return input(prompt)
