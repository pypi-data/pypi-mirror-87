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

from cliff.lister import Lister
from cliff.show import ShowOne

from pyjamaas import parse, maas, util


class List(Lister):
    """
    list MaaS machines
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parse.machines_arguments(parser)
        parser.add_argument('--all', action='store_true', help='show all info')
        return parser

    def take_action(self, parsed_args):
        return util.list_dict_to_cliff(maas.match_machines(
            parsed_args.match, formatted=not parsed_args.all))


class Get(ShowOne):
    """
    get info for a MaaS machine
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parse.machines_arguments(parser)
        parser.add_argument('--all', action='store_true', help='show all info')
        return parser

    def take_action(self, parsed_args):
        return util.dict_to_cliff(maas.match_machines(
            parsed_args.match, formatted=not parsed_args.all)[0])
