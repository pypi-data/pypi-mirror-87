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

import sys

from cliff.command import Command

from pyjamaas import parse, maas
from pyjamaas.log import log


class Clone(Command):
    """
    clone configuration
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--source', type=parse.yaml_argument, required=True,
            help='source machine')
        parser.add_argument(
            '--destination', type=parse.yaml_argument, required=True,
            help='destination machines')
        parser.add_argument(
            '--force', action='store_true', help='do not ask for confirmation')
        parser.add_argument(
            '--network', action='store_true', help='clone interface config')
        parser.add_argument(
            '--storage', action='store_true', help='clone storage config')
        return parser

    def take_action(self, parsed_args):
        source = maas.match_machines(parsed_args.source)
        if len(source) > 1:
            log.fatal('Multiple source machines were matched')
            sys.exit(1)

        system_id, hostname = source[0]['system_id'], source[0]['hostname']
        log.info(f'Using {system_id} ({hostname}) as source')

        destination = maas.match_machines(parsed_args.destination)

        # filter out source machine from destinations
        destination = [d for d in destination if d['system_id'] != system_id]

        log.info(f'Will apply configuration to {len(destination)} machines:')
        for machine in destination:
            m_id, m_name = machine['system_id'], machine['hostname']
            log.info(f'- {m_id} ({m_name})')

        if not parsed_args.force:
            reply = input('Are you sure [y/N]? ')
            if reply.lower() != 'y':
                log.error('Aborted due to user input')

        s = maas.session()
        log.info('Cloning')
        r = s.Machines.clone(
            system_id=system_id,
            destination=destination,
            interfaces=parsed_args.network,
            storage=parsed_args.storage
        )
        log.info(f'Result: {r}')
