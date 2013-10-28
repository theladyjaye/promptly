import sys
from .form import Form
from .inputs import String
from .inputs import Integer
from .inputs import Select
from .inputs import MultiSelect
from .inputs import Boolean
from .inputs import Branch
from .inputs import Notification
from .utils import prepare_stylesheet


def notification(text, prefix=None, stylesheet=None):

    styles = prepare_stylesheet(stylesheet)
    prefix = '' if prefix is None else prefix

    message = Notification(text)
    prompt = message.build_prompt(prefix=prefix, stylesheet=styles)
    sys.stdout.write('\n%s' % prompt)
    sys.stdout.flush()

