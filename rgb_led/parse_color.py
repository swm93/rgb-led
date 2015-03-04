from argparse import Action, ArgumentTypeError
import re
import json


# mapping of colors to their appropriate RGB value
colors = json.loads(open("./settings/color_mapping.json").read())

class ParseColor(Action):
    def __call__(self, parser, namespace, color, option_string):
        c_val = None
        c_types = None

        if (isinstance(color, list) and len(color) == 1):
            color = color[0]

        if (isinstance(color, list) and len(color) == 3):
            color = [float(i) for i in color]

        # request is a color, use lookup table to convert it to list
        if (isinstance(color, str) and color in colors):
            color = colors[color]

        c_val = color
        c_types = self.infer_types(color)

        # color is invalid
        if (len(c_types) == 0):
            msg = "%r is not a color" % c_val
            raise(ArgumentTypeError(msg))

        setattr(namespace, self.dest, c_val)
        setattr(namespace, 'possible_types', c_types)

    def infer_types(self, color):
        c_types = []

        if (self.is_hex(color)):
            c_types.append('hex')
        if (self.is_rgb(color)):
            c_types.append('rgb')
        if (self.is_hs(color)):
            c_types.append('hsv')
            c_types.append('hsl')

        return c_types

    def is_color(self, color):
        return self.is_rgb(color) or self.is_hs(color) or self.is_hex(color)

    def is_rgb(self, color):
        return (
            isinstance(color, list) and
            len(color) == 3 and
            sum(0.0 <= i <= 255.0 for i in color) == 3
        )

    def is_hs(self, color):
        return (
            isinstance(color, list) and
            len(color) == 3 and
            0.0 <= color[0] <= 360.0 and
            sum(0.0 <= i <= 100.0 for i in color[1:]) == 2
        )

    def is_hex(self, color):
        return (
            isinstance(color, str) and
            re.match('^#?(?:[0-9a-fA-F]{3}){1,2}$', color)
        )