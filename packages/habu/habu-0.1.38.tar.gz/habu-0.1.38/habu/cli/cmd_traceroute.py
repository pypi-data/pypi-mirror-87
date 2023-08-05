#!/usr/bin/env python3

import logging

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from habu.lib.iface import search_iface
from scapy.all import IP, TCP, conf, sr1


@click.command()
@click.argument('ip')
@click.option('-p', 'port', default=80, help='Port to use (default: 80)')
@click.option('-i', 'iface', default=None, help='Interface to use')
def cmd_traceroute(ip, port, iface):
    """TCP traceroute.

    Identify the path to a destination getting the ttl-zero-during-transit messages.

    Note: On the internet, you can have various valid paths to a device.

    Example:

    \b
    # habu.traceroute 45.77.113.133
    IP / ICMP 192.168.0.1 > 192.168.0.5 time-exceeded ttl-zero-during-transit / IPerror / TCPerror
    IP / ICMP 10.242.4.197 > 192.168.0.5 time-exceeded ttl-zero-during-transit / IPerror / TCPerror / Padding
    IP / ICMP 200.32.127.98 > 192.168.0.5 time-exceeded ttl-zero-during-transit / IPerror / TCPerror / Padding
    .
    IP / ICMP 4.16.180.190 > 192.168.0.5 time-exceeded ttl-zero-during-transit / IPerror / TCPerror
    .
    IP / TCP 45.77.113.133:http > 192.168.0.5:ftp_data SA / Padding

    Note: It's better if you use a port that is open on the remote system.
    """

    conf.verb = False

    if iface:
        iface = search_iface(iface)
        if iface:
            conf.iface = iface['name']
        else:
            logging.error('Interface {} not found. Use habu.interfaces to show valid network interfaces'.format(iface))
            return False

    pkts = IP(dst=ip, ttl=(1, 16)) / TCP(dport=port)

    for pkt in pkts:

        ans = sr1(pkt, timeout=1, iface=conf.iface)

        if not ans:
            print('.')
            continue

        print(ans.summary())

        if TCP in ans and ans[TCP].flags == 18:
            break

    return True


if __name__ == '__main__':
    cmd_traceroute()
