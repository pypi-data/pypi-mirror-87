
from netifaces import (
    AF_INET, AF_INET6, AF_LINK, gateways, ifaddresses, interfaces)

import requests
import ipaddress


def get_public_ipv4():
    """Get the public IPv4 address for the connection."""
    ipv4 = requests.get('https://api.ipify.org', timeout=5).text
    return ipv4

def get_public_ipv6():
    """Get the public IPv6 address for the connection."""
    ipv6 = requests.get('https://api6.ipify.org', timeout=5).text
    return ipv6


def get_internal_ip():
    """Get the local IP addresses."""
    nics = {}
    for interface_name in interfaces():
        addresses = ifaddresses(interface_name)
        try:
            nics[interface_name] = {
                'ipv4': addresses[AF_INET],
                'link_layer': addresses[AF_LINK],
                'ipv6': addresses[AF_INET6],
            }
        except KeyError:
            pass

    return nics


def geo_location(ip_address):
    """Get the Geolocation of an IP address."""
    try:
        type(ipaddress.ip_address(ip_address))
    except ValueError:
        return {}

    data = requests.get(
        'https://ipapi.co/{}/json/'.format(ip_address), timeout=5).json()
    return data


def get_gateways():
    """Get all gateways for the interfaces."""
    return gateways()


if __name__ == '__main__':
    print(get_external_ip())
