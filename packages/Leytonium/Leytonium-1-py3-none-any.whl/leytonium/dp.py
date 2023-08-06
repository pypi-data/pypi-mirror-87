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

from .common import getpublic, args, stderr
from lagoon import git

def main_dp():
    'Diff from public branch.'
    parent = getpublic()
    stderr("Public branch: %s" % parent)
    git.diff._M25.exec(*args(), parent)

def main_pd():
    'Diff from public branch, the other way.'
    parent = getpublic()
    stderr("Public branch: %s" % parent)
    git.diff._M25.exec(*args(), 'HEAD', parent)
