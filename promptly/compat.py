import sys


_ver = sys.version_info
is_py2 = (_ver[0] == 2)


def input(prompt):
    if is_py2:
        return raw_input(prompt)
    else:
        return input(prompt)
