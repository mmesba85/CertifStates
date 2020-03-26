import json
import logging
import sys
import time
from typing import Dict, TypedDict, List

import dns.resolver
import dns.reversename

from ipwhois.net import Net
from ipwhois.asn import IPASN

import pandas as pd
from pandas import DataFrame

from collision import Collision

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


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
    start_time = time.time()

    filepath = sys.argv[1] if len(sys.argv) > 1 else '..\collisions_em.json'

    collisions = None
    with open(filepath, 'r', encoding='utf-8') as file:
        collisions: List = json.load(file)

    results: List[Dict] = []

    for collisions_dict in collisions:  # each row is a collision dataframe
        collisions_df: DataFrame = pd.DataFrame.from_dict(collisions_dict).transpose()
        for index, row in collisions_df.iterrows():
            collision: Collision = row.to_dict()

            # ipAdressess and dnsNames could be either a string or a list of strings
            ip = collision.get('ipAdressess')
            if isinstance(ip, list):
                ip = ip[0]

            domain = collision.get('dnsNames')
            if isinstance(domain, list):
                domain = domain[0]

            # Get ip or domain if missing
            if not ip and domain:
                logger.debug('Missing IP address for domain %s', domain)

                ip = get_ip_from_domain(domain)
            elif not domain and ip:
                logger.debug('Missing domain for IP %s', ip)

                domain = get_domain_from_ip(ip)

            collisions_df.at[index, 'ipAdressess'] = ip
            collisions_df.at[index, 'dnsNames'] = domain

            asn = {}
            if ip is not None:
                asn: ASNLookup = ip_asn_lookup(ip)

            collisions_df.at[index, 'asn'] = asn.get('asn')
            collisions_df.at[index, 'asnRegistry'] = asn.get('asn_registry')
            collisions_df.at[index, 'asnCidr'] = asn.get('asn_cidr')
            collisions_df.at[index, 'asnCountryCode'] = asn.get('asn_country_code')
            collisions_df.at[index, 'asnDate'] = asn.get('asn_date')
            collisions_df.at[index, 'asnDescription'] = asn.get('asn_description')

        results.append(collisions_df.transpose().to_dict())

    with open('collisions_maroua_completed.json', 'w', encoding='utf-8') as file:
        json.dump(results, file)

    logger.info("--- ASN, IP and DNS lookups took %s seconds to complete. ---" % (time.time() - start_time))
