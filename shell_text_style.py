class ShellTextStyle:
    styles = {
        'HEADER': '\033[95m',
        'SUCCESS': '\033[92m',
        'INFO': '\033[94m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m'
    }
    endc = '\033[0m'

    @staticmethod
    def header(text):
        return ShellTextStyle.styles['HEADER'] + text + ShellTextStyle.endc

    @staticmethod
    def success(text):
        return ShellTextStyle.styles['SUCCESS'] + text + ShellTextStyle.endc

    @staticmethod
    def info(text):
        return ShellTextStyle.styles['INFO'] + text + ShellTextStyle.endc

    @staticmethod
    def warning(text):
        return ShellTextStyle.styles['WARNING'] + text + ShellTextStyle.endc

    @staticmethod
    def error(text):
        return ShellTextStyle.styles['ERROR'] + text + ShellTextStyle.endc

    @staticmethod
    def bold(text):
        return ShellTextStyle.styles['BOLD'] + text + ShellTextStyle.endc

    @staticmethod
    def underline(text):
        return ShellTextStyle.styles['UNDERLINE'] + text + ShellTextStyle.endc