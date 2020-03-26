import sys
from typing import Dict, TypedDict

import dns.resolver
import dns.reversename

from ipwhois.net import Net
from ipwhois.asn import IPASN

import pandas as pd

from collision import Collision


class ASNLookup(TypedDict):
    """
    ASN Lookup function return type description
    Example: {'asn_registry': 'arin', 'asn': '15169', 'asn_cidr': '8.8.8.0/24', 'asn_country_code': 'US', 'asn_date': '1992-12-01', 'asn_description': 'GOOGLE, US'}
        {
            'asn_registry': 'arin',
            'asn': '15169',
            'asn_cidr': '8.8.8.0/24',
            'asn_country_code': 'US',
            'asn_date': '1992-12-01',
            'asn_description': 'GOOGLE, US'
        }
    """
    asn_registry: str
    asn: str
    asn_cidr: str
    asn_country_code: str
    asn_date: str
    asn_description: str


def get_ip_from_domain(domain: str) -> str:
    """
    Gets DNS query 'IN A' field.
    Equivalent to a "dig -q domain" linux command
    :param domain: e.g. 'google.com'
    :return: ip address
    """
    resolver = dns.resolver.Resolver()
    answer: dns.resolver.Answer = resolver.query(domain, 'A')
    return answer.rrset[0].address


def get_domain_from_ip(ip: str) -> str:
    ip = dns.reversename.from_address(ip)
    return dns.resolver.query(ip, "PTR")[0]


def ip_asn_lookup(ip: str) -> Dict:
    net = Net(ip)
    obj = IPASN(net)
    results = obj.lookup()
    return results


if __name__ == '__main__':
    filepath = sys.argv[0]
    filepath = '..\checker\output.json'
    collisions: pd.DataFrame = pd.read_json(filepath)
    print(collisions)
    for i, j in collisions.iterrows():
        collision: Collision = j.to_dict()

        # ipAdressess and dnsNames could be either a string or a list of strings
        ip = collision.get('ipAdressess')
        if isinstance(ip, list):
            ip = ip[0]

        domain = collision.get('dnsNames')
        if isinstance(domain, list):
            domain = domain[0]

        # Get ip or domain if missing
        if ip is None and domain is not None:
            ip = get_ip_from_domain(domain)
        elif domain is None and ip is not None:
            domain = get_domain_from_ip(ip)

        collisions.at[i, 'ipAdressess'] = ip
        collisions.at[i, 'dnsNames'] = domain

        asn = {}
        if ip is not None:
            asn: ASNLookup = ip_asn_lookup(ip)

        collisions.at[i, 'asn'] = asn.get('asn')
        collisions.at[i, 'asnRegistry'] = asn.get('asn_registry')
        collisions.at[i, 'asnCidr'] = asn.get('asn_cidr')
        collisions.at[i, 'asnCountryCode'] = asn.get('asn_country_code')
        collisions.at[i, 'asnDate'] = asn.get('asn_date')
        collisions.at[i, 'asnDescription'] = asn.get('asn_description')

    for i, j in collisions.iterrows():
        print(j)

    collisions.to_json('collisions_completed.json')
