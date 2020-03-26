import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import community

from collections import Counter

# keyType                  rsaEncryption
# dnsNames                      epita.fr
# ipAdressess             151.101.66.159
# publicKeyRaw      30 82 01 22 30 0d 06
# commonName          GeoTrust Global CA
# countryName                         US
# asn                              54113
# asnRegistry                       arin
# asnCidr                151.101.64.0/22
# asnCountryCode                      US
# asnDate                     2016-02-01
# asnDescription              FASTLY, US

if __name__ == '__main__':
    # filepath = sys.argv[0]
    filepath = './collisions_completed.json'
    collisions: pd.DataFrame = pd.read_json(filepath)
    print(collisions)

    ip_asn_counter = [(ip, Counter(list(collisions[collisions['ipAdressess'] == ip]['asn']))) for ip in collisions]

    g = nx.Graph()
    for ip, c in ip_asn_counter:
        for k, v in c.items():
            g.add_edge(ip, k, weight=v)

    pos = nx.spring_layout(g)
    plt.figure(3, figsize=(10, 10))
    nx.draw(g, pos, with_labels=True)


    
    

