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

from .common import findproject
from lagoon import autopep8, sed
import re, subprocess, sys

cols = 120 # TODO LATER: Make configurable.

def main_brown():
    'Satisfy PEP 8 with minimal impact.'
    roots = sys.argv[1:]
    if not roots:
        roots = [findproject()]
    command = autopep8._rv.partial('--max-line-length', cols, *roots)
    result = command._d(stdout = subprocess.DEVNULL, stderr = subprocess.PIPE)
    def paths():
        for line in result.splitlines():
            m = re.fullmatch(r'\[file:(.+)]', line)
            if m is not None:
                yield m.group(1)
    sed._ni.print(r'/\S/p', *paths())
    command._i.print()
