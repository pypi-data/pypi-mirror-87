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

from maas.client.bones import SessionAPI, CallError, helpers

from pyjamaas.config import config
from pyjamaas.log import log


__session = None


# Collection of errors that may happen when using MaaS API
APIError = (CallError, helpers.RemoteError)


def session():
    """
    Return a sessions to the MaaS server. Subsequent calls reuse the same
    connection
    """
    global __session
    if __session:
        return __session

    if not config.maas.api_url:
        raise RuntimeError('MAAS_API_URL is not set, see `pyjamaas --help`')
    if not config.maas.api_key:
        raise RuntimeError('MAAS_API_KEY is not set, see `pyjamaas --help`')

    log.info(f'Connecting to {config.maas.api_url}')
    _, __session = SessionAPI.connect(
        config.maas.api_url, apikey=config.maas.api_key)

    return __session


def format_machine(machine):
    """
    format/filter machine info from MaaS
    """
    return {
        'hostname': machine['hostname'],
        'system_id': machine['system_id'],
        'status': machine['status_name'],
        'tags': machine['tag_names'],
    }


def _get(options, key):
    s = options.get(key) or []
    if not isinstance(s, list):
        s = [s]
    return s


def match_machines(options, formatted=True):
    """
    Match machines based on tags, hostname, or system id
    """
    s = session()

    log.debug(f'Looking for machines with filter {options}')

    match_tags = _get(options, 'tags')
    match_hostnames = _get(options, 'hostname')
    match_system_ids = _get(options, 'system_id')

    if match_system_ids:
        machines = s.Machines.read(id=match_system_ids)
    elif match_hostnames:
        machines = s.Machines.read(hostname=match_hostnames)
    elif match_tags:
        unfiltered_machines = s.Tag.machines(name=match_tags[0])
        machines = [m for m in unfiltered_machines if all(
            t in m['tag_names'] for t in match_tags)]
    else:
        log.error('Not fetching machines with empty filter')
        machines = []

    if formatted:
        machines = [format_machine(m) for m in machines]

    return machines
