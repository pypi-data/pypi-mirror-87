import sys
import glob
import pathlib
import subprocess as subproc
from schema import Schema, SchemaError
from chpwd_cmd.color import green, red


class WorkDir:

    schema = Schema({'dirpath': str, 'cmd': str})

    def __init__(self, name, workdir, cwd):
        self.name = name
        try:
            self.schema.validate(workdir)
        except SchemaError as e:
            raise WorkDirInvalid(e) from None

        self.cmd = workdir['cmd']
        p = pathlib.Path(workdir['dirpath'])

        self.dirpath_candidates = glob.glob(str(p.expanduser()))
        self.enable = True if cwd in self.dirpath_candidates else False
        self.cwd = cwd

    def __execute__(self):
        try:
            subproc.run(self.cmd, cwd=self.cwd, shell=True, check=True)
        except subproc.CalledProcessError as e:
            sys.stderr.write(
                f'{red(self.cmd)} in workdir[{red(self.name)}]\
                    was not successful\n')
            raise (e)

        sys.stdout.write(
            f'{green(self.cmd)} in workdir[{green(self.name)}] executed by chpwd_cmd\n')

    def __dryrun__(self):
        if self.enable:
            sys.stdout.write(
                f'{green(self.cmd)} in workdir[{green(self.name)}] execute\n')
        else:
            sys.stdout.write(
                f'{red(self.cmd)} in workdir[{red(self.name)}] not execute\n')

    def __listdir__(self):
        sys.stdout.write(
            f'workdir[{green(self.name)}] {len(self.dirpath_candidates)} directory paths\n')
        sorted_dirpath = sorted(self.dirpath_candidates)
        for dir in sorted_dirpath:
            sys.stdout.write(f'{dir}\n')

    def execute(self, mode):
        if self.enable and mode == 'exec':
            self.__execute__()
        elif mode == 'dryrun':
            self.__dryrun__()
        elif mode == 'listdir':
            self.__listdir__()


class WorkDirInvalid(Exception):
    pass
