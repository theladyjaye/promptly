import pkg_resources
from .styles import CSSParser


DEFAULT_STYLESHEET_CACHE = None


def numeric_options(options):

    max = len(options) + 1
    numbers = range(1, max)
    # call to list if for python 3
    return list(zip(numbers, options))


def prepare_stylesheet(value=None):
    global DEFAULT_STYLESHEET_CACHE

    if value:
        return CSSParser.parse_string(value)

    if DEFAULT_STYLESHEET_CACHE:
        return DEFAULT_STYLESHEET_CACHE

    stream = pkg_resources.resource_stream(
        'promptly.resources',
        'default.css'
    )

    DEFAULT_STYLESHEET_CACHE = CSSParser.parse_string(stream.read())

    return DEFAULT_STYLESHEET_CACHE
