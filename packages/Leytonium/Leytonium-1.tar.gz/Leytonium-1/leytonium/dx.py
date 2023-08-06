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

from .common import AllBranches, args as getargs, pb, savedcommits, showmenu, stderr
from lagoon import git

def main_dx():
    'Diff from parent branch or from passed-in commit number.'
    args = getargs()
    if args:
        n, = args
        n = int(n)
        parent = showmenu(AllBranches().branchcommits(), False)[n]
    else:
        parent = pb()
        stderr("Parent branch: %s" % parent)
    git.diff._M25.exec(parent)

def main_dxx():
    'Short diff from parent branch or of passed-in commit number.'
    args = getargs()
    if args:
        n, = args
        n = int(n)
        if n > 0:
            commit = showmenu(AllBranches().branchcommits(), False)[n]
        else:
            saved = savedcommits()
            commit = saved[len(saved) - 1 + n]
        commits = "%s^" % commit, commit
    else:
        parent = pb()
        stderr("Parent branch: %s" % parent)
        commits = parent,
    git.diff._M25.__name_status.exec(*commits)
