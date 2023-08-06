import setuptools

def long_description():
    with open('README.md') as f:
        return f.read()

# Copyright 2013, 2014, 2015, 2016, 2017, 2020 Andrzej Cichocki

# This file is part of pyven.
#
# pyven is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyven is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyven.  If not, see <http://www.gnu.org/licenses/>.

class SourceInfo:

    class PYXPath:

        suffixes = '.pyx', '.c'

        def __init__(self, module, path):
            self.module = module
            self.path = path

        def buildrequires(self):
            if self.path.endswith('.pyx'):
                yield 'Cython'

        def make_ext(self):
            g = {}
            with open(self.path + 'bld') as f: # Assume project root.
                exec(f.read(), g)
            return g['make_ext'](self.module, self.path)

    def __init__(self, rootdir):
        import os, setuptools, subprocess
        self.packages = setuptools.find_packages(rootdir)
        extpaths = {}
        def addextpaths(dirpath, moduleprefix):
            names = sorted(os.listdir(os.path.join(rootdir, dirpath)))
            for suffix in self.PYXPath.suffixes:
                for name in names:
                    if name.endswith(suffix):
                        module = "%s%s" % (moduleprefix, name[:-len(suffix)])
                        if module not in extpaths:
                            extpaths[module] = self.PYXPath(module, os.path.join(dirpath, name))
        addextpaths('.', '')
        for package in self.packages:
            addextpaths(package.replace('.', os.sep), "%s." % package)
        extpaths = extpaths.values()
        if extpaths and os.path.isdir(os.path.join(rootdir, '.git')): # We could be an unpacked sdist.
            check_ignore = subprocess.Popen(['git', 'check-ignore'] + [p.path for p in extpaths], cwd = rootdir, stdout = subprocess.PIPE)
            ignoredpaths = set(check_ignore.communicate()[0].decode().splitlines())
            assert check_ignore.wait() in [0, 1]
            self.extpaths = [path for path in extpaths if path.path not in ignoredpaths]
        else:
            self.extpaths = extpaths

# Copyright 2013, 2014, 2015, 2016, 2017, 2020 Andrzej Cichocki

# This file is part of pyven.
#
# pyven is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyven is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyven.  If not, see <http://www.gnu.org/licenses/>.

def lazy(clazz, init, *initbefore):
    from threading import Lock
    initlock = Lock()
    init = [init]
    def overridefactory(name):
        orig = getattr(clazz, name)
        def override(*args, **kwargs):
            with initlock:
                if init:
                    init[0](obj)
                    del init[:]
            return orig(*args, **kwargs)
        return override
    Lazy = type('Lazy', (clazz, object), {name: overridefactory(name) for name in initbefore})
    obj = Lazy()
    return obj

# FIXME: The idea was to defer anything Cython/numpy to pyximport time, but this doesn't achieve that.
def cythonize(extensions):
    def init(ext_modules):
        ordinary = []
        cythonizable = []
        for e in extensions:
            (cythonizable if any(s.endswith('.pyx') for s in e.sources) else ordinary).append(e)
        if cythonizable:
            from Cython.Build import cythonize
            ordinary += cythonize(cythonizable)
        ext_modules[:] = ordinary
    return lazy(list, init, '__getitem__', '__iter__', '__len__')

def ext_modules():
    extensions = [path.make_ext() for path in sourceinfo.extpaths]
    return dict(ext_modules = cythonize(extensions)) if extensions else {}

sourceinfo = SourceInfo('.')
setuptools.setup(
        name = 'Leytonium',
        version = '1',
        description = 'Tools for developing git-managed software',
        long_description = long_description(),
        long_description_content_type = 'text/markdown',
        url = 'https://github.com/combatopera/Leytonium',
        author = 'Andrzej Cichocki',
        packages = sourceinfo.packages,
        py_modules = [],
        install_requires = ['aridity>=35', 'autopep8>=1.5.4', 'awscli>=1.18.133', 'lagoon>=17', 'PyGObject>=3.27.2', 'pytz>=2020.4', 'pyven>=56', 'PyYAML>=5.2', 'termcolor>=1.1.0'],
        package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt']},
        scripts = [],
        entry_points = {'console_scripts': ['abandon=leytonium.abandon:main_abandon', 'autopull=leytonium.autopull:main_autopull', 'awslogs=leytonium.awslogs:main_awslogs', 'br=leytonium.br:main_br', 'brown=leytonium.brown:main_brown', 'ci=leytonium.ci:main_ci', 'co=leytonium.co:main_co', 'diffuse=leytonium.diffuse:main_diffuse', 'dp=leytonium.dp:main_dp', 'pd=leytonium.dp:main_pd', 'dx=leytonium.dx:main_dx', 'dxx=leytonium.dx:main_dxx', 'gt=leytonium.gt:main_gt', 'halp=leytonium.halp:main_halp', 'hgcommit=leytonium.hgcommit:main_hgcommit', 'isotime=leytonium.isotime:main_isotime', 'ks=leytonium.ks:main_ks', 'multimerge=leytonium.multimerge:main_multimerge', 'n=leytonium.n:main_n', 'next=leytonium.next:main_next', 'prepare=leytonium.prepare:main_prepare', 'publish=leytonium.publish:main_publish', 'readjust=leytonium.readjust:main_readjust', 'agi=leytonium.refactor:main_agi', 'agil=leytonium.refactor:main_agil', 'ren=leytonium.ren:main_ren', 'resimp=leytonium.resimp:main_resimp', 'rol=leytonium.rol:main_rol', 'scrape85=leytonium.scrape85:main_scrape85', 'squash=leytonium.scripts:main_squash', 'drclean=leytonium.scripts:main_drclean', 'drst=leytonium.scripts:main_drst', 'examine=leytonium.scripts:main_examine', 'drop=leytonium.scripts:main_drop', 'gimports=leytonium.scripts:main_gimports', 'reks=leytonium.scripts:main_reks', 'eb=leytonium.scripts:main_eb', 'fixemails=leytonium.scripts:main_fixemails', 'mdview=leytonium.scripts:main_mdview', 'upgrade=leytonium.scripts:main_upgrade', 'vpn=leytonium.scripts:main_vpn', 'vunzip=leytonium.scripts:main_vunzip', 'setparent=leytonium.setparent:main_setparent', 'showstash=leytonium.shortcommands:main_showstash', 'pb=leytonium.shortcommands:main_pb', 'd=leytonium.shortcommands:main_d', 'rdx=leytonium.shortcommands:main_rdx', 'rx=leytonium.shortcommands:main_rx', 'gag=leytonium.shortcommands:main_gag', 'git-completion-path=leytonium.shortcommands:main_git_completion_path', 'git-functions-path=leytonium.shortcommands:main_git_functions_path', 'rd=leytonium.shortcommands:main_rd', 'dup=leytonium.shortcommands:main_dup', 'scrub=leytonium.shortcommands:main_scrub', 'shove=leytonium.shove:main_shove', 'show=leytonium.show:main_show', 'slam=leytonium.slam:main_slam', 'unslam=leytonium.slam:main_unslam', 'splitpkgs=leytonium.splitpkgs:main_splitpkgs', 'st=leytonium.st:main_st', 'stacks=leytonium.stacks:main_stacks', 'stmulti=leytonium.stmulti:main_stmulti', 'fetchall=leytonium.stmulti:main_fetchall', 'pullall=leytonium.stmulti:main_pullall', 'pushall=leytonium.stmulti:main_pushall', 'taskding=leytonium.taskding:main_taskding', 'tempvenv=leytonium.tempvenv:main_tempvenv', 'touchb=leytonium.touchb:main_touchb', 'unpub=leytonium.unpub:main_unpub']},
        **ext_modules())
