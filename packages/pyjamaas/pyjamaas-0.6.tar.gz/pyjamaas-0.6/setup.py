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


import re
from setuptools import setup, find_packages


def get_file(name):
    try:
        with open(name, 'r') as fin:
            return fin.read()
    except OSError:
        return ""


def get_version():
    changelog = get_file('CHANGELOG.md')
    version = next(re.finditer(r'## \[v([\d.]*)\]', changelog), None)
    return version and version.group(1) or 'none'


def setup_package():
    setup(
        name='pyjamaas',
        version=get_version(),
        description='Python MaaS and Juju toolkit',
        long_description=get_file('README.md'),
        long_description_content_type='text/markdown',
        url='https://github.com/grnet/pyjamaas.git',
        packages=find_packages(),
        entry_points={
            'console_scripts': [
                'pyjamaas = pyjamaas.cliff:main',
            ],
            'pyjamaas.entrypoints': [
                'clone = pyjamaas.commands.clone:Clone',
                'config = pyjamaas.commands.config:Config',
                'machine list = pyjamaas.commands.machine:List',
                'machine get = pyjamaas.commands.machine:Get',
                'tags add = pyjamaas.commands.tags:Add',
                'tags clear = pyjamaas.commands.tags:Clear',
                'tags delete = pyjamaas.commands.tags:Delete',
                'unlock = pyjamaas.commands.unlock:Unlock',
                'shell = pyjamaas.commands.shell:Shell',
                'allocate = pyjamaas.commands.allocate:Allocate',
                'release = pyjamaas.commands.release:Release',
            ],
            'oslo.config.opts': [
                'pyjamaas = pyjamaas.config:list_opts',
            ]
        },
        install_requires=[
            'cliff',
            'python-libmaas',
            'pyyaml',
        ],
        classifiers=[
            'Intended Audience :: System Administrators',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: OS Independent',
        ],
    )


if __name__ == '__main__':
    setup_package()
