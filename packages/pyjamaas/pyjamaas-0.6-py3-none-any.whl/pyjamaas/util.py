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


def list_dict_to_cliff(data):
    """
    convert list of dicts to Cliff (columns, (values)) format
    """
    if not data:
        return (None, None)

    columns = list(data[0].keys())
    values = list([d[col] for col in columns] for d in data)

    return columns, values


def dict_to_cliff(data):
    """
    convert list of dicts to Cliff (columns, (values)) format
    """
    columns, values = list_dict_to_cliff([data])
    return columns, values[0]
