# pyjamaas

Python Juju and MaaS toolkit.

## Features

`pyjamaas` simplifies interaction with MaaS and Juju when working with a large number of heterogenous machines. It heavily utilizes the MaaS tags mechanism.

Features:

- `pyjamaas tags`: Easily create, delete and update multiple tags for multiple machines
- `pyjamaas clone`: Easily clone configuration to multiple machines, using tags
- `pyjamaas machine`: Utility commands for retrieving machine information

Also see [examples](./EXAMPLES.md)

## Installation

```bash
$ pip install pyjamaas
```

## Configuration

`pyjamaas` needs MaaS credentials. You can use environment variables:

```bash
$ export MAAS_API_URL=https://maas.server.name:5240/MAAS/api/2.0
$ export MAAS_API_KEY=AAAAAAAAAAAAAA:BBBBBBBBBBBBBBB:CCCCCCCCCCCCCCC
```

Or create a `pyjamaas.conf` file (see [sample](./config/pyjamaas.conf)):

```ini
[maas]
api_url = https://maas.server.name:5240/MAAS/api/2.0
api_key = AAAAAAAAAAAAAA:BBBBBBBBBBBBBBB:CCCCCCCCCCCCCCC
```

```bash
$ pyjamaas <command> --config-file pyjamaas.conf
```

`pyjamaas` will automatically look for config files in a few standard directories, e.g. `/etc/pyjamaas.conf`, `/etc/pyjamaas/pyjamaas.conf`, `~/.pyjamaas/pyjamaas.conf`).

Print loaded configuration with `pyjamaas config`. If a required option is missing, an error message is printed:

```bash
$ pyjamaas config
value required for option api_key in group [maas]
```

## Usage

For a list of available commands:

```bash
$ pyjamaas --help
```

Most `pyjamaas` commands have the format `pyjamaas <command> <args> --match <filter>`. The `<filter>` can be used to select machines based on `system_id`, `hostname`, or `tags`. The examples below should be clear enough:

```bash
# Match a single machine using hostname
$ pyjamaas machine list --match '{hostname: host1}'
```

```bash
# Match multiple machines by hostname
$ pyjamaas machine list --match '{hostname: [host1, host2]}'
```

```bash
# Match multiple machines by system id
$ pyjamaas machine list --match '{system_id: [system1, system2]}'
```

```bash
# Match machines using tags (multiple tags imply AND)
$ pyjamaas machine list --match '{tags: [tag1, tag2]}'
```

## Auto completion

Enable auto-completion with:

```bash
$ . <(pyjamaas complete)
```
