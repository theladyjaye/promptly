import sys

_ver = sys.version_info
is_py2 = (_ver[0] == 2)
is_py3 = (_ver[0] == 3)

if is_py3:
    unichr = chr
    unicode = str
else:
    unichr = unichr
    unicode = unicode


def iteritems(value):
    if is_py2:
        return value.iteritems()

    return value.items()


def itervalues(value):
    if is_py2:
        return value.itervalues()

    return value.values()


def input(prompt):
    if is_py2:
        return raw_input(prompt.encode(sys.stdout.encoding))
    else:
        return input(prompt)
