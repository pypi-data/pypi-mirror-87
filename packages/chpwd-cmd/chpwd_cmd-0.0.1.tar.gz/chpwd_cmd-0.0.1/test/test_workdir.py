from nose.tools import raises

import chpwd_cmd.workdir as wd


class TestWorkdir:

    # error
    @raises(wd.WorkDirInvalid)
    def test_type_invalid(self):
        wd.WorkDir('test', {'dirpath': 0, 'cmd': []}, 'pwd')

    @raises(wd.WorkDirInvalid)
    def test_dirpath_key_missing(self):
        wd.WorkDir('test', {'cmd': 'pwd'}, 'pwd')

    @raises(wd.WorkDirInvalid)
    def test_cmd_key_missing(self):
        wd.WorkDir('test', {'dirpath': '/home'}, 'pwd')

    @raises(wd.WorkDirInvalid)
    def test_all_key_missing(self):
        wd.WorkDir('', {}, '')
