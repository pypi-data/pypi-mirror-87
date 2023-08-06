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

from datetime import datetime
import pytz, re, sys

tz = pytz.timezone('Europe/London') # TODO LATER: Should be configurable, or deduce local somehow.
pattern = re.compile('(9[0-9]{8}|[1-3][0-9]{9})([0-9]{3})?')

def _repl(m):
    tstr, mstr = m.groups()
    t = int(tstr) + (int(mstr) / 1000 if mstr else 0)
    dt = datetime.utcfromtimestamp(t).replace(tzinfo = pytz.utc).astimezone(tz)
    return f"{dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}{dt.strftime('%z')}"

def main_isotime():
    'Filter UNIX timestamps to human-readable form.'
    for line in sys.stdin:
        sys.stdout.write(pattern.sub(_repl, line))
