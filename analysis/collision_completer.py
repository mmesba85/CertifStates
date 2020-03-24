from typing import Dict

import dns.resolver
import dns.reversename

from ipwhois.net import Net
from ipwhois.asn import IPASN


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
