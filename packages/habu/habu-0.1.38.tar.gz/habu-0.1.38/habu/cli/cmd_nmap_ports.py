#!/usr/bin/env python3

import re
import sys

import click


def detect_format(data):
    if data.startswith('<?xml version="1.0" encoding="UTF-8"?>'):
        return 'xml'

    lines = data.split('\n')

    if lines[1].startswith('Host'):
        return 'gnmap'

    if lines[1].startswith('Nmap scan report'):
        return 'nmap'

    return 'unknown'


def parse_format_xml(data, protocol):

    # <port protocol="tcp" portid="21"><state state="closed"

    line_regex_str = r'<port protocol="{}" portid="(?P<port>\d+)"'.format(protocol)
    line_regex = re.compile(line_regex_str)

    ports = set()

    for line in data.split('\n'):
        m = line_regex.match(line)
        if m:
            ports.add(int(m.group(1)))

    return sorted(ports)



def parse_format_nmap(data, protocol):

    line_regex_str = r'(?P<port>\d+)/{}'.format(protocol)
    line_regex = re.compile(line_regex_str)

    ports = set()

    for line in data.split('\n'):
        m = line_regex.match(line)
        if m:
            ports.add(int(m.group(1)))

    return sorted(ports)



def parse_format_gnmap(data, protocol):

    line_regex_str = r'(?P<port>\d+)/\w+/{}'.format(protocol)
    line_regex = re.compile(line_regex_str)

    ports = set()

    for line in data.split('\n'):
        if 'Ports:' not in line:
            continue

        content = line.split('Ports: ')[1]
        for c in content.split(','):
            c = c.strip()
            m = line_regex.match(c)
            if m:
                ports.add(int(m.group(1)))

    return sorted(ports)



@click.command()
@click.argument('scanfile', type=click.File())
@click.option('-p', 'protocol', default='tcp', type=click.Choice(['tcp', 'udp', 'sctp']), help='The protocol (default=tcp)')
def cmd_nmap_ports(scanfile, protocol):
    """Read an nmap report and print the tested ports.

    Print the ports that has been tested reading the generated nmap output.

    You can use it to rapidly reutilize the port list for the input of other tools.

    Supports and detects the 3 output formats (nmap, gnmap and xml)

    Example:

    \b
    # habu.nmap.ports portantier.nmap
    21,22,23,80,443
    """

    data = scanfile.read()
    fmt = detect_format(data)

    if fmt not in ['xml', 'nmap', 'gnmap']:
        print('Unknown file format.', file=sys.stdout)
        return 1

    if fmt == 'nmap':
        result = parse_format_nmap(data, protocol)
    elif fmt == 'gnmap':
        result = parse_format_gnmap(data, protocol)
    elif fmt == 'xml':
        result = parse_format_xml(data, protocol)

    print(','.join([ str(r) for r in result]), end='')

    return True


if __name__ == '__main__':
    cmd_nmap_ports()
