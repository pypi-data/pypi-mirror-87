# Copyright 2020 Andrzej Cichocki

# This file is part of Leytonium.
#
# Leytonium is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Leytonium is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Leytonium.  If not, see <http://www.gnu.org/licenses/>.

from . import effectivehome
from aridity.config import ConfigCtrl
from lagoon import clear, co, find, git, hg, hgcommit, md5sum, rsync, test, tput
from pathlib import Path
from pyven.projectinfo import ProjectInfo
import glob, logging, re, shlex, sys

log = logging.getLogger(__name__)
trunknames = {'main', 'master', 'trunk'}

def loadconfig():
    config = ConfigCtrl()
    config.loadsettings()
    return config.node.stmulti

class Project:

    kindwidth = 3
    kindformat = "%%-%ss" % kindwidth

    @classmethod
    def forprojects(cls, config, action):
        for path in sorted(d.parent for d in Path('.').glob("*/%s" % glob.escape(cls.dirname))):
            print(cls.kindformat % cls.dirname[1:1 + cls.kindwidth], "%s%s%s" % (tput.setaf(7), path, tput.sgr0()))
            getattr(cls(config, path), action)()

    def __init__(self, config, path):
        for command in self.commands:
            setattr(self, Path(command.path).name, command.cd(path))
        self.homerelpath = path.resolve().relative_to(effectivehome)
        self.netpath = Path(config.repomount, effectivehome.name, self.homerelpath)
        self.config = config
        self.path = path

class Mercurial(Project):

    dirname = '.hg'
    commands = hg, hgcommit

    def fetch(self):
        pass

    def pull(self):
        self.hg.pull.print(self.netpath)
        self.hg.update.print()

    def push(self):
        self.hgcommit.print()

    def status(self):
        self.hg.st.print()

class Git(Project):

    dirname = '.git'
    commands = co, git, hgcommit, md5sum, test
    remotepattern = re.compile('(.+)\t(.+) [(].+[)]')
    hookname = 'post-commit'

    def _checkremotes(self):
        d = {}
        for l in self.git.remote._v().splitlines():
            name, loc = self.remotepattern.fullmatch(l).groups()
            if name in d:
                assert d[name] == loc
            else:
                d[name] = loc
        netremotepath = d.get(self.config.netremotename)
        if "%s:%s.git" % (self.config.repohost, self.netpath) != netremotepath:
            log.error("Bad %s: %s", self.config.netremotename, netremotepath)
        for name, loc in d.items():
            if name != self.config.netremotename and not loc.startswith('git@'):
                log.error("Non-SSH remote: %s %s", name, loc)

    def _allbranches(self, task):
        restore, = self.git.rev_parse.__abbrev_ref.HEAD().splitlines()
        for branch in (l[2:] for l in self.git.branch().splitlines()):
            self.co.print(branch)
            task(branch)
        self.co.print(restore)

    def fetch(self):
        self.git.fetch.__all.print()

    def pull(self):
        # TODO: Only fetch once.
        # FIXME: The public branch does not normally exist in netpath.
        self._allbranches(lambda branch: self.git.pull.__ff_only.print(self.netpath, branch))

    def push(self):
        self._allbranches(lambda branch: self.hgcommit.print())

    def status(self):
        if (self.path / 'project.arid').exists():
            if Path(self.config.repomount).is_dir(): # Needn't actually be mounted.
                self._checkremotes()
                hookpath = Path('.git', 'hooks', self.hookname)
                if self.md5sum(hookpath, check = False).stdout[:32] != self.config.hookmd5:
                    log.error("Bad hook: %s", self.hookname)
                if self.test._x.print(hookpath, check = False):
                    log.error("Unexecutable hook: %s", self.hookname)
            if ProjectInfo.seek(self.path).config.pypi.participant:
                lastrelease = max((t for t in self.git.tag().splitlines() if t.startswith('v')), default = None, key = lambda t: int(t[1:]))
                if lastrelease is None:
                    lastrelease, = self.git.rev_list('--max-parents=0', 'HEAD').splitlines() # Assume trivial initial commit.
                shortstat = self.git.diff.__shortstat(lastrelease, '--', '.', *(":(exclude,glob)%s" % glob for glob in ['.travis.yml', 'project.arid', '**/test_*.py', '.gitignore']))
                if shortstat:
                    sys.stdout.write(f"{tput.rev()}{tput.setaf(5)}{lastrelease}{tput.sgr0()}{shortstat}")
        lines = [BranchLine(l) for l in self.git.branch._vv('--color=always').splitlines()]
        trunklines = [l for l in lines if l.branch in trunknames]
        if 1 == len(trunklines):
            l, = trunklines
            idealpublic = l.publicparts()
        else:
            idealpublic = None
        for line in lines:
            if idealpublic != line.parts:
                print(line.highlighted())
        self.git.status._s.print()
        self.git.stash.list.print()

class BranchLine:

    sgr = re.compile(r'\x1b\[[0-9;]*m')

    @property
    def branch(self):
        return self.parts[1]

    def __init__(self, line):
        self.parts = re.split(' +', self.sgr.sub('', line), 4)
        self.line = line

    def publicparts(self):
        return ['', 'public', self.parts[2], f"[origin/{self.parts[1]}]", self.parts[4]]

    def highlighted(self):
        line = re.sub(r':[^]\n]+]', lambda m: f"{tput.setaf(3)}{tput.rev()}{m.group()}{tput.sgr0()}", self.line)
        if '*' == self.parts[0] and self.parts[1] not in trunknames:
            line = re.sub(re.escape(self.parts[1]), lambda m: f"{tput.setaf(6)}{tput.bold()}{m.group()}{tput.sgr0()}", line, 1)
        return line

class Rsync(Project):

    dirname = '.rsync'
    commands = find, hgcommit, rsync

    def fetch(self):
        pass

    def pull(self):
        lhs = '-avzu', '--exclude', "/%s" % self.dirname
        rhs = "%s::%s/%s/" % (self.config.repohost, self.config.reponame, self.homerelpath), '.'
        self.rsync.print(*lhs, *rhs)
        lhs += '--del',
        self.rsync.print(*lhs, '--dry-run', *rhs)
        print("(cd %s && rsync %s)" % (shlex.quote(str(self.path)), ' '.join(map(shlex.quote, lhs + rhs))))

    def push(self):
        self.hgcommit.print()

    def status(self):
        tput.setaf.print(4)
        tput.bold.print()
        self.find._newer.print(self.dirname)
        tput.sgr0.print()

def main(action):
    config = loadconfig()
    clear.print()
    for projecttype in Mercurial, Git, Rsync:
        projecttype.forprojects(config, action)

def main_stmulti():
    'Short status of all shallow projects in directory.'
    main('status')

def main_fetchall():
    main('fetch')

def main_pullall():
    main('pull')

def main_pushall():
    main('push')
