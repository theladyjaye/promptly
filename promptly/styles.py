import colorama
from colorama import Style as AnsiStyle

colorama.init()


class Style(object):

    reset_all = colorama.Style.RESET_ALL

    @classmethod
    def styles_for_key(cls, key, stylesheet):
        styles = {}
        context = stylesheet

        try:
            styles.update(context['selectors']['body']['value'])
        except KeyError:
            pass

        for part in key.split('.'):
            try:
                context = context['selectors'][part]
                styles.update(context['value'])

            except KeyError:
                break

        return cls(styles)

    def __init__(self, data):
        self.data = data

    @property
    def color(self):
        try:
            return getattr(colorama.Fore, self.data['color'].upper())
        except (KeyError, AttributeError):
            return ''

    @property
    def background_color(self):
        try:
            return getattr(colorama.Back, self.data['background_color'].upper())
        except (KeyError, AttributeError):
            return ''

    @property
    def font_weight(self):

        try:
            font_weight = self.data['font_weight']
        except KeyError:
            return ''

        choices = {'normal': colorama.Style.NORMAL,
                   'bold': colorama.Style.BRIGHT,
                   'lighter': colorama.Style.DIM}

        return choices.get(font_weight, colorama.Style.NORMAL)

    def __call__(self, value):
        # Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
        # Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
        # Style: DIM, NORMAL, BRIGHT, RESET_ALL
        return self.reset_all + self.color + \
               self.background_color + \
               self.font_weight + \
               value + \
               self.reset_all


class CSSTokens(object):

    SELECTOR = 'SELECTOR'
    BODY_START = 'BODY_START'
    BODY_END = 'BODY_END'
    PROPERTY = 'PROPERTY'
    PROPERTY_VALUE = 'PROPERTY_VALUE'


class CSSParser(object):

    @staticmethod
    def parse_string(value):
        parser = CSSParser()
        return parser.parse(value)

    def parse(self, value):
        sheet = {'selectors':{}}

        context = sheet
        property_name = None

        for token, value in self.tokenize(value):
            if token == CSSTokens.SELECTOR:
                data = self.format(value)

                if data:
                    context = context.setdefault('selectors', {})
                    context = context.setdefault(data, {'value': {}})

            elif token == CSSTokens.BODY_START:
                data = self.format(value)
                if data:
                    context = context.setdefault('selectors', {})
                    context = context.setdefault(data, {'value': {}})

            elif token == CSSTokens.PROPERTY:
                property_name = self.format(value)

            elif token == CSSTokens.PROPERTY_VALUE:
                context['value'][property_name] = self.format(value)
                property_name = None

            elif token == CSSTokens.BODY_END:
                data = self.format(value)
                if data:
                    context['value'][property_name] = data

                context = sheet

        return sheet

    def format(self, value):
        return value \
               .strip() \
               .replace('-', '_') \
               .lower()

    def tokenize(self, value):
        buf = ''

        for char in value:

            if char == '.':
                yield CSSTokens.SELECTOR, buf
                buf = ''

            elif char == '{':
                yield CSSTokens.BODY_START, buf
                buf = ''

            elif char == '}':
                yield CSSTokens.BODY_END, buf
                buf = ''

            elif char == ':':
                yield CSSTokens.PROPERTY, buf
                buf = ''

            elif char == ';':
                yield CSSTokens.PROPERTY_VALUE, buf
                buf = ''
            else:
                buf = buf + str(char)



