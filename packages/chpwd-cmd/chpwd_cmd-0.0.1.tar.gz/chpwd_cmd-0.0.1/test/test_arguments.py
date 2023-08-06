from nose.tools import assert_equal, with_setup, raises
import sys
import chpwd_cmd.arguments as args


class TestArguments:

    def setup(self):
        # remove parameter with nosetests
        del sys.argv[1:]

    @with_setup(setup=setup)
    def test_mode_listdir_cwd_none_success(self):
        sys.argv.extend(['-m', 'listdir'])
        res = args.Arguments().get()
        assert_equal(res.mode, 'listdir')
        assert_equal(res.cwd, None)

    @with_setup(setup=setup)
    def test_mode_listdir_cwd_success(self):
        sys.argv.extend(['-m', 'listdir', '-c', '/home/dir'])
        res = args.Arguments().get()
        assert_equal(res.mode, 'listdir')
        assert_equal(res.cwd, '/home/dir')

    @with_setup(setup=setup)
    def test_mode_none_cwd_success(self):
        sys.argv.extend(['-c', '/home/dir'])
        res = args.Arguments().get()
        assert_equal(res.mode, 'exec')
        assert_equal(res.cwd, '/home/dir')

    @raises(args.ArgumentsError)
    @with_setup(setup=setup)
    def test_mode_exec_cwd_none_value_error(self):
        sys.argv.extend(['-m', 'exec'])
        args.Arguments().get()

    @raises(args.ArgumentsError)
    @with_setup(setup=setup)
    def test_mode_dryrun_cwd_none_value_error(self):
        sys.argv.extend(['-m', 'dryrun'])
        args.Arguments().get()

    @raises(args.ArgumentsError)
    @with_setup(setup=setup)
    def test_no_command_line_arguments(self):
        args.Arguments().get()
