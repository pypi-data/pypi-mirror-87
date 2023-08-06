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

from . import st
from .common import args, findproject, infodirname, pb, savedcommits
from lagoon import clear, find, git
from pathlib import Path

def main_showstash():
    'Show stash as patch.'
    git.stash.show._p.exec()

def main_pb():
    'Find parent branch.'
    print(pb())

def main_d():
    'Show local changes.'
    clear.print()
    git.diff.print()

def main_rdx():
    'Run git rm on conflicted path, with completion.'
    git.rm.exec(*args())

def main_rx():
    'Restore given file to parent branch version.'
    git.checkout.print(pb(), *args())

def main_gag():
    'Run ag on all build.gradle files.'
    find._name.exec('build.gradle', '-exec', 'ag', *args(), '{}', '+')

def main_git_completion_path():
    print(Path(__file__).parent / 'git_completion')

def main_git_functions_path():
    print(Path(__file__).parent / 'git_functions')

def main_rd():
    'Run git add on conflicted path, with completion.'
    # FIXME: Reject directory args.
    # FIXME: Refuse to add file with outstanding conflicts, easy to do from command history.
    git.add.exec(*args())

def main_dup():
    'Apply the last slammed commit.'
    git.cherry_pick.__no_commit.print(savedcommits()[-1])
    git.reset.print()
    st.main_st()

def main_scrub():
    'Remove all untracked items, including the git-ignored.'
    git.clean._xdi.print('-e', infodirname, cwd = findproject())
