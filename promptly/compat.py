import sys


_ver = sys.version_info
is_py2 = (_ver[0] == 2)


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
        return raw_input(prompt)
    else:
        return input(prompt)
