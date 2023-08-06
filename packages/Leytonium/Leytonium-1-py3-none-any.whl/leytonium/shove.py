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

import sys, subprocess, re

pattern = re.compile('latest|.+[.]latest')

def main_shove():
    spec, = sys.argv[1:]
    slash = spec.index('/')
    colon = spec.rindex(':')
    tag = spec[colon + 1:]
    if pattern.fullmatch(tag) is None:
        raise Exception('REFUSAL!')
    subprocess.check_call(['bash', '-ic', 'aws ecr batch-delete-image --repository-name "$1" --image-ids "$2"', 'ecr', spec[slash + 1:colon], "imageTag=%s" % tag])
    subprocess.check_call(['docker', 'push', spec])
