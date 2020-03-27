import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import community
import json

from typing import Dict, TypedDict, List
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
    filepath = sys.argv[1] if len(sys.argv) > 1 else './collisions_completed.json'

    collisions = None
    with open(filepath, 'r', encoding='utf-8') as file:
        collisions: List = json.load(file)

    results: List[Dict] = []

    for collisions_dict in collisions:  # each row is a collision dataframe
        collisions_df = pd.DataFrame.from_dict(collisions_dict).transpose()
        print(collisions_df)

        
    
    

