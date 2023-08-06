# Copyright (C) 2020  GRNET S.A.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import yaml


def yaml_argument(arg):
    """
    argparse YAML argument type
    """
    try:
        if arg is not None and arg.startswith('@'):
            with open(arg[1:], 'r') as fin:
                return yaml.safe_load(fin)
        return yaml.safe_load(arg)
    except yaml.YAMLError as e:
        raise argparse.ArgumentTypeError('invalid YAML') from e
    except OSError as e:
        raise argparse.ArgumentTypeError('could not load file') from e


def maas_arguments(parser):
    """
    MaaS configuration
    """


def machines_arguments(parser):
    """
    Arguments for matching against MaaS machines
    """
    parser.add_argument(
        '--match', type=yaml_argument, required=True,
        help='Choose MaaS machines')
