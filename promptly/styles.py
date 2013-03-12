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
        parser.parse(value)

    def parse(self, value):
        sheet = {'selectors':{}}
        context = sheet
        property_name = None

        import pdb; pdb.set_trace()

        for token, value in self.tokenize(value):
            if token == CSSTokens.SELECTOR:
                data = value.strip()

                if data:
                    context = context.setdefault('selectors', {})
                    context = context.setdefault(data, {})

            elif token == CSSTokens.BODY_START:
                data = value.strip()
                if data:
                    context = context.setdefault('selectors', {})
                    context = context.setdefault(data, {})

            elif token == CSSTokens.PROPERTY:
                property_name = value.strip().replace('-', '_')

            elif token == CSSTokens.PROPERTY_VALUE:
                context[property_name] = value.strip()
                property_name = None

            elif token == CSSTokens.BODY_END:
                data = value.strip()
                if data:
                    context[property_name] = data

                context = sheet

        import pdb; pdb.set_trace()
        return sheet

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
                buf = buf + char



