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

from argparse import ArgumentParser
from lagoon import python3
from lagoon.program import Program
from pathlib import Path
from tempfile import TemporaryDirectory
import logging, os

log = logging.getLogger(__name__)
shellpath = os.environ['SHELL']

def main_tempvenv():
    'Activate a temporary venv.'
    logging.basicConfig(level = logging.DEBUG, format = "[%(levelname)s] %(message)s")
    parser = ArgumentParser()
    parser.add_argument('-w', action = 'store_true', help = 'enable bdist_wheel command')
    parser.add_argument('reqs', nargs = '*')
    args = parser.parse_args()
    with TemporaryDirectory() as venvdir:
        venvdir = Path(venvdir)
        log.info("Create venv: %s", venvdir)
        python3._m.venv.print(venvdir) # Must use host executable to get pip apparently.
        pipinstall = Program.text(venvdir / 'bin' / 'pip').install
        if args.w:
            pipinstall.wheel.print()
        if args.reqs:
            pipinstall.print(*args.reqs)
        Program.text(shellpath)._c.print('. "$1" && exec "$2"', '-c', venvdir / 'bin' / 'activate', shellpath)
