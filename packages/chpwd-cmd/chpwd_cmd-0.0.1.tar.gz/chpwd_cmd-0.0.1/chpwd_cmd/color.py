class Color:
    GREEN = '\033[32m'
    RED = '\033[31m'
    RESET = '\033[0m'


def green(text):
    return f'{Color.GREEN}{text}{Color.RESET}'


def red(text):
    return f'{Color.RED}{text}{Color.RESET}'
