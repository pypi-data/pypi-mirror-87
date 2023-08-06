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

from lagoon import git
from pathlib import Path

def main_next():
    'Go to next step in current git workflow.'
    gitdir = Path(git.rev_parse.__git_dir().rstrip())
    if (gitdir / 'rebase-apply').is_dir():
        if git.status.__porcelain().splitlines():
            git.rebase.__continue.print()
        else:
            git.rebase.__skip.print()
    elif (gitdir / 'MERGE_HEAD').is_file():
        git.commit.__no_edit.print()
    elif (gitdir / 'CHERRY_PICK_HEAD').is_file():
        git.cherry_pick.__continue.print()
    elif (gitdir / 'REVERT_HEAD').is_file():
        git.revert.__continue.print()
    else:
        raise Exception('Unknown git workflow, giving up.')
