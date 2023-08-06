import toml
import os
import sys


class ConfigFile:

    CONFIG_FILE_PATH = f'{os.environ["HOME"]}/.chpwd_cmd'

    def __init__(self):
        try:
            self.config = toml.load(open(self.CONFIG_FILE_PATH))
        except toml.decoder.TomlDecodeError as e:
            sys.stderr.write(f'configuration file ({self.CONFIG_FILE_PATH}) seems to be wrong\n {e}')
            raise ConfigFileError(e) from None
        except FileNotFoundError as e:
            sys.stderr.write(f'configuration file ({self.CONFIG_FILE_PATH}) does not exist\n {e}')
            raise ConfigFileError(
                f'configuration file ({self.CONFIG_FILE_PATH}) does not exist {e}') from None


class ConfigFileError(Exception):
    pass
