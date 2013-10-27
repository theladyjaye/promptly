import sys
from .form import Form
from .inputs import StringInput
from .inputs import IntegerInput
from .inputs import SelectInput
from .inputs import MultiSelectInput
from .inputs import BooleanInput
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

