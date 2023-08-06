from nose.tools import assert_equal, with_setup, raises
import sys
import os
import subprocess
from io import StringIO
from contextlib import redirect_stdout

from chpwd_cmd import chpwd_cmd
from chpwd_cmd.color import green, red


def run_chpwd_cmd():
    io = StringIO()
    with redirect_stdout(io):
        chpwd_cmd.main()

    return io.getvalue()


class TestChpwdCmd:

    cwd = os.getcwd()

    def setup(self):
        # remove parameter with nosetests
        del sys.argv[1:]
        chpwd_cmd.ConfigFile.CONFIG_FILE_PATH = 'test/files/.test_chpwd_cmd'

    # error
    @raises(SystemExit)
    @with_setup(setup=setup)
    def test_no_configuration(self):
        chpwd_cmd.ConfigFile.CONFIG_FILE_PATH = 'test/files/.no_chpwd_cmd'
        sys.argv.extend(['-c', self.cwd, '-m', 'exec'])
        chpwd_cmd.main()

    @raises(SystemExit)
    @with_setup(setup=setup)
    def test_no_commmand_line_args(self):
        sys.argv.extend([])
        chpwd_cmd.main()

    # exec
    @with_setup(setup=setup)
    def test_chpwd_exec_success(self):
        sys.argv.extend(['-c', self.cwd, '-m', 'exec'])
        assert_equal(run_chpwd_cmd(
        ), f"{green('pwd')} in workdir[{green('test')}] executed by chpwd_cmd\n")

    @with_setup(setup=setup)
    def test_chpwd_exec_home_dir_success(self):
        sys.argv.extend(['-c', os.environ['HOME'], '-m', 'exec'])
        assert_equal(run_chpwd_cmd(
        ), f"{green('pwd')} in workdir[{green('test_home_dir')}] executed by chpwd_cmd\n")

    @with_setup(setup=setup)
    def test_chpwd_exec_none_output(self):
        sys.argv.extend(['-c', f'{self.cwd}/test/testdirnone', '-m', 'exec'])
        assert_equal(run_chpwd_cmd(), '')

    @raises(subprocess.CalledProcessError)
    @with_setup(setup=setup)
    def test_chpwd_exec_command_exception(self):
        chpwd_cmd.ConfigFile.CONFIG_FILE_PATH = 'test/files/.test_command_exception'
        sys.argv.extend(['-c', '.', '-m', 'exec'])

        assert_equal(run_chpwd_cmd(
        ), f"{red('aaaaa')} in workdir[{red('cmd_exception')}] was not successful\n")

    # dryrun
    @with_setup(setup=setup)
    def test_chpwd_dryrun_success(self):
        sys.argv.extend(['-c', os.environ['HOME'], '-m', 'dryrun'])
        lines = run_chpwd_cmd().splitlines()
        assert_equal(
            lines[0], f"{red('pwd')} in workdir[{red('test')}] not execute")
        assert_equal(
            lines[1], f"{green('pwd')} in workdir[{green('test_home_dir')}] execute")
        assert_equal(
            lines[2], f"{red('pwd')} in workdir[{red('wildcard')}] not execute")

    # listdir
    @with_setup(setup=setup)
    def test_chpwd_listdir_success(self):
        sys.argv.extend(['-m', 'listdir'])
        lines = run_chpwd_cmd().splitlines()
        assert_equal(
            lines[0], f"workdir[{green('test')}] 1 directory paths")
        assert_equal(lines[1], self.cwd)
        assert_equal(
            lines[2], f"workdir[{green('test_home_dir')}] 1 directory paths")
        assert_equal(lines[3], os.environ["HOME"])
        assert_equal(
            lines[4], f"workdir[{green('wildcard')}] 2 directory paths")
        assert_equal(
            lines[5], f"{self.cwd}/test/testdir/dir1")
        assert_equal(
            lines[6], f"{self.cwd}/test/testdir/dir2")
