import whois

from collision import Collision


def collision_whois(collision: Collision) -> Collision:
    dns: str = collision.dnsNames
    domain = whois.query(dns)
    return domain.__dict__


collision = Collision(keyType='test', dnsNames='google.com', ipAdressess='8.8.8.8', publicKeyRaw='1', commonName='1',
                      countryName='FR')

print(collision_whois(collision))


