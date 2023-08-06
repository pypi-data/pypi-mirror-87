import argparse


class Arguments:

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='This program executes the commands in the \
                        configuration file according to the\
                        current working directory')
        self.parser.add_argument(
            '-c', '--cwd', type=str,
            help='current working directory')
        self.parser.add_argument(
            '-m', '--mode', default='exec',
            choices=['exec', 'dryrun', 'listdir'],
            help='running mode (default:exec)')

    def get(self):
        if not self.parser.parse_args().mode == 'listdir' and not self.parser.parse_args().cwd:
            raise ArgumentsError(
                f'command line arguments was invalid {self.parser.parse_args()}')
        return self.parser.parse_args()

    def help(self):
        self.parser.print_help()


class ArgumentsError(ValueError):
    pass
