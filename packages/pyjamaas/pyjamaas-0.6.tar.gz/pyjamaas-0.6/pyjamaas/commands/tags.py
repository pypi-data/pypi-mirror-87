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

from collections import defaultdict
import sys

from cliff.command import Command

from pyjamaas import parse, maas
from pyjamaas.log import log


class Add(Command):
    """
    add tags
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parse.machines_arguments(parser)
        parser.add_argument(
            '--tags', required=True, nargs='+', metavar='TAG',
            help='list of tags')
        parser.add_argument(
            '--no-create', action='store_true',
            help='do not create tags automatically if they do not exist')
        return parser

    def take_action(self, parsed_args):
        s = maas.session()
        existing_tags = [t['name'] for t in s.Tags.read()]

        new_tags = [t for t in parsed_args.tags if t not in existing_tags]
        if new_tags and parsed_args.no_create:
            log.fatal('Will not create new tags with --no-create flag')
            sys.exit(1)

        for tag in new_tags:
            log.info(f'Creating new tag {tag}')
            r = s.Tags.create(name=tag, description=f'{tag} (pyjamaas)')
            log.debug(f'Result: {r}')

        machines = maas.match_machines(parsed_args.match)
        system_ids = [m['system_id'] for m in machines]

        for tag in parsed_args.tags:
            log.info(f'Adding tag {tag} to {len(machines)} machines')
            r = s.Tag.update_nodes(name=tag, add=system_ids)
            log.debug(f'Result: {r}')


class Clear(Command):
    """
    clear tags from machines
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parse.machines_arguments(parser)
        g = parser.add_mutually_exclusive_group(required=True)
        g.add_argument('--all-tags', action='store_true', help='clear all')
        g.add_argument('--tags', nargs='+', metavar='TAG', help='list of tags')
        return parser

    def take_action(self, parsed_args):
        machines = maas.match_machines(parsed_args.match)
        s = maas.session()

        clear_tags = defaultdict(lambda: [])
        for machine in machines:
            if parsed_args.all_tags:
                parsed_args.tags = machine['tags']

            for tag in set(parsed_args.tags) & set(machine['tags']):
                clear_tags[tag].append(machine['system_id'])

        for tag, system_ids in clear_tags.items():
            log.info(f'Clearing tag {tag} from {len(system_ids)} machines')
            r = s.Tag.update_nodes(name=tag, remove=system_ids)
            log.debug(r)


class Delete(Command):
    """
    delete a tag
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'tags', nargs='+', metavar='TAG', help='list of tags to delete')
        return parser

    def take_action(self, parsed_args):
        s = maas.session()
        for tag in parsed_args.tags:
            log.info(f'Deleting tag {tag}')
            r = s.Tag.delete(name=tag)
            log.debug(f'Response: {r}')
