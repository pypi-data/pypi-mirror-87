from nose.tools import raises
import chpwd_cmd.config_file as cf


class TestConfigFile:

    @raises(cf.ConfigFileError)
    def test_config_file_not_found(self):
        cf.ConfigFile.CONFIG_FILE_PATH = 'test/.notfound_test_chpwd_cmd'
        cf.ConfigFile()

    @raises(cf.ConfigFileError)
    def test_config_file_invalid(self):
        cf.ConfigFile.CONFIG_FILE_PATH = 'test/.test_invalid_config_file'
        cf.ConfigFile()
