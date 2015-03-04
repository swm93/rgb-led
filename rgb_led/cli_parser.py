from argparse import ArgumentParser, ArgumentTypeError

class CliParser(ArgumentParser):
    def error(self, message):
        raise(ArgumentTypeError(message))