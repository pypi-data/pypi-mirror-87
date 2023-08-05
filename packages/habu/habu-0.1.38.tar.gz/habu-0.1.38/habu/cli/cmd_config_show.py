#!/usr/bin/env python3

import json

import click

from habu.lib.loadcfg import loadcfg


@click.command()
@click.option('-k', '--show-keys', is_flag=True, default=False, help='Show also the key values')
@click.option('--option', nargs=2, help='Write to the config(KEY VALUE)')
def cmd_config_show(option, show_keys):
    """Show the current config.

    Note: By default, the options with 'KEY' in their name are shadowed.

    Example:

    \b
    $ habu.config.show
    {
        "DNS_SERVER": "8.8.8.8",
        "FERNET_KEY": "*************"
    }
    """

    habucfg = loadcfg()

    if not show_keys:
        for key in habucfg.keys():
            if 'KEY' in key:
                habucfg[key] = '*************'

    print(json.dumps(habucfg, indent=4, sort_keys=True, default=str))


if __name__ == '__main__':
    cmd_config_show()

