from rgb_led import RgbLed

from cli_parser import CliParser
from parse_color import ParseColor
from shell_text_style import ShellTextStyle as TextStyle

from cmd import Cmd
from argparse import ArgumentParser, ArgumentTypeError
import json
import re



class RgbLedShell(Cmd):
    prompt = '> '

    def __init__(self):
        self.settings = self.load_settings()

        self.led = RgbLed(self.settings['pins'], self.settings['pwm_frequency'])

        self.color_parser = CliParser(
            usage='%(prog)s [options] <inputs>',
            description='TODO: add description'
        )
        self.color_parser.add_argument('--rgb', const='rgb', dest='type', action='store_const')
        self.color_parser.add_argument('--hsv', const='hsv', dest='type', action='store_const')
        self.color_parser.add_argument('--hsl', const='hsl', dest='type', action='store_const')
        self.color_parser.add_argument('--hex', const='hex', dest='type', action='store_const')
        self.color_parser.add_argument('color', nargs='*', action=ParseColor)

        self.fade_parser = ArgumentParser(
            usage='%(prog)s [options] <inputs>',
            description='TODO: add description'
        )

        super(self.__class__, self).__init__()

    def do_color(self, args):
        try:
            args = self.color_parser.parse_args(args.split())
            args.type = args.type or args.possible_types[0]
            self.validate_color_type(args.type, args.possible_types)

            print(args)

            if (args.type == 'rgb'):
                self.led.set_rgb_color(*args.color)
                print(self.led.get_rgb_color())
            elif (args.type == 'hsv'):
                self.led.set_hsv_color(*args.color)
                print(self.led.get_hsv_color())
            elif (args.type == 'hsl'):
                self.led.set_hsl_color(*args.color)
                print(self.led.get_hsl_color())
            elif (args.type == 'hex'):
                self.led.set_hex_color(args.color)
                print(self.led.get_hex_color())

        except ArgumentTypeError as e:
            self.error(e)

    def do_fade(self, args):
        return

    def do_exit(self, *args):
        return True

    do_EOF = do_exit

    def emptyline(self):
        return

    def error(self, msg):
        print(TextStyle.error("Error: %s" % msg.args[0]))

    def format_text(self, text, format):
        return self.text_colors[format] + text + self.text_colors['ENDC']

    def validate_color_type(self, c_type, c_possible_types):
        if (not c_type in c_possible_types):
            msg = "The color provided is not of type %r" % c_type
            raise(ArgumentTypeError(msg))

    # load default and user settings, user settings take priority
    def load_settings(self):
        default_settings = json.loads(open('./settings/default.json').read())
        user_settings = json.loads(open('./settings/user.json').read())

        return dict(list(default_settings.items()) + list(user_settings.items()))




if (__name__ == '__main__'):
    shell = RgbLedShell()
    shell.cmdloop()