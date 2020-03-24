from analysis.collision import Collision
from analysis.collision_completer import *

collision = Collision(keyType='test', dnsNames='google.com', ipAdressess='8.8.8.8', publicKeyRaw='1',
                      commonName='1',
                      countryName='FR')


def test_dns_lookup():
    print('\n')
    print('Testing', collision)
    ip = get_ip_from_domain(collision.dnsNames)
    domain = get_domain_from_ip(ip)
    print('Asked ip for domain', collision.dnsNames, 'got ip', ip, 'and reverse domain', domain)

    asn_lookup: Dict = ip_asn_lookup(ip)
    print(asn_lookup)
    print('ASN Lookup', asn_lookup.get('asn'), asn_lookup.get('asn_description'), asn_lookup.get('asn_cidr'), asn_lookup.get('asn_country_code'))

def test_reverse_dns():
    print(get_domain_from_ip(collision.ipAdressess))
