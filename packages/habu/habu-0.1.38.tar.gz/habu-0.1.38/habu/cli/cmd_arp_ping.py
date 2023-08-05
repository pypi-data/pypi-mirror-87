#!/usr/bin/env python3

import logging

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from habu.lib.iface import search_iface
from scapy.all import ARP, Ether, conf, srp


@click.command()
@click.argument('ip')
@click.option('-i', 'iface', default=None, help='Interface to use')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_arp_ping(ip, iface, verbose):
    """
    Send ARP packets to check if a host it's alive in the local network.

    Example:

    \b
    # habu.arp.ping 192.168.0.1
    Ether / ARP is at a4:08:f5:19:17:a4 says 192.168.0.1 / Padding
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    conf.verb = False

    if iface:
        iface = search_iface(iface)
        if iface:
            conf.iface = iface['name']
        else:
            logging.error('Interface {} not found. Use habu.interfaces to show valid network interfaces'.format(iface))
            return False

    res, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2)

    for _, pkt in res:
        if verbose:
            print(pkt.show())
        else:
            print(pkt.summary())


if __name__ == '__main__':
    cmd_arp_ping()
