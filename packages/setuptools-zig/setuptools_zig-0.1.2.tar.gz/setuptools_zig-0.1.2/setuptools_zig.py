# coding: utf-8

import sys
import os
from subprocess import run
from pathlib import Path

from distutils.dist import Distribution
from setuptools.command.build_ext import build_ext as SetupToolsBuildExt


class ZigCompilerError(Exception):
    """Some compile/link operation failed."""


class BuildExt(SetupToolsBuildExt):
    def __init__(self, dist, zig_value):
        self._zig_value = zig_value
        super().__init__(dist)

    def build_extension(self, ext):
        if not self._zig_value:
            return super().build_extension(ext)
        # check if every file in ext.sources exists
        for p in ext.sources:
            assert Path(p).exists()

        output = Path(self.get_ext_filename(ext.name))
        target = Path(self.get_ext_fullpath(ext.name))

        zig = os.environ.get('PY_ZIG', 'zig')  # override zig in path with specific version
        bld_cmd = [zig, 'build-lib', '-dynamic', '-DPYHEXVER={}'.format(sys.hexversion), '--name', output.stem]
        for inc_dir in self.compiler.include_dirs:
            bld_cmd.extend(('-I', inc_dir))
        bld_cmd.extend(('-I', '/usr/include'))
        bld_cmd.extend(ext.sources)
        print('\ncmd', ' '.join([x if ' ' not in x else '"' + x + '"' for x in bld_cmd]))
        sys.stdout.flush()
        run(bld_cmd)
        if not output.exists():
            output = output.parent / ('lib' + output.name)
        if output.exists():
            if target.exists():
                target.unlink()
            else:
                target.parent.mkdir(exist_ok=True, parents=True)
            output.rename(target)
        else:
            raise ZigCompilerError(f'expected output {output} does not exist')


class ZigBuildExtension:
    def __init__(self, value):
        self._value = value

    def __call__(self, dist):
        return BuildExt(dist, zig_value=self._value)


def setup_build_zig(dist, keyword, value):
    assert isinstance(dist, Distribution)
    assert keyword == 'build_zig'
    be = dist.cmdclass.get('build_ext')
    dist.cmdclass['build_ext'] = ZigBuildExtension(value)
