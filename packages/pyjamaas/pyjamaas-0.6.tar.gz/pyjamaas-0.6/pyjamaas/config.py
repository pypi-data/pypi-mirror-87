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

from oslo_config import cfg
from oslo_config.sources import _environment


class EnvSource(_environment.EnvironmentConfigurationSource):
    """
    EnvironmentConfigurationSource with custom prefix
    """
    prefix = ""

    @classmethod
    def _make_name(cls, group_name, option_name):
        group_name = group_name or 'PYJAMAAS'
        return '{}{}_{}'.format(
            cls.prefix, group_name.upper(), option_name.upper())


config = cfg.ConfigOpts()
config._env_driver = EnvSource()

grp = cfg.OptGroup('maas')
opts = [
    cfg.StrOpt(
        'api_url',
        required=True,
        help='MaaS API URL',
        sample_default='https://maas:5240/MAAS/api/2.0'
    ),
    cfg.StrOpt(
        'api_key',
        required=True,
        help='MaaS API Key',
        sample_default='AAAAAAAAAA:BBBBBBBBBBBBB:CCCCCCCCCCCCC'
    ),
]

config.register_group(grp)
config.register_opts(opts, group=grp)


def list_opts():
    """
    used as entrypoing for `oslo-config-generator`
    """
    return [
        [g, [o['opt'] for o in g._opts.values()]]
        for g in config._groups.values()]
