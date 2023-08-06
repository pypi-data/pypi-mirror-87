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


from cliff.command import Command

from pyjamaas import parse, maas
from pyjamaas.log import log


class Release(Command):
    """
    Release machines
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--machines', type=parse.yaml_argument, required=True,
            help='machines to release')
        parser.add_argument(
            '--erase-disks', action='store_true', default=False,
            help='erase disks before releasing machine')
        parser.add_argument(
            '--secure-erase', action='store_true', default=False,
            help='do secure erase')
        parser.add_argument(
            '--quick-erase', action='store_true', default=False,
            help='do quick erase')
        return parser

    def take_action(self, parsed_args):
        machines = maas.match_machines(parsed_args.machines)

        s = maas.session()
        for m in machines:
            system_id, hostname = m['system_id'], m['hostname']
            log.info(f'Releasing {hostname} ({system_id})')
            s.Machine.release(
                system_id=m['system_id'],
                erase_disks=parsed_args.erase_disks,
                secure_erase=parsed_args.secure_erase,
                quick_erase=parsed_args.quick_erase,
            )
