class Prompt(object):

    def process_value(self, value):
        return value

    def apply_default(self, value):
        if len(value) == 0 and self.input.default is not None:
            return self.input.default

        return value
