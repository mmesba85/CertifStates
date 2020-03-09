from dataclasses import dataclass
from typing import List, Union


@dataclass
class Collision:
    """
    Collision object, returned by `checker` module in a list of pandas' data frames
    """
    keyType: str
    dnsNames: Union[List[str], str]  # TODO ask Mus if this can really be a list ?
    ipAdressess: Union[List[str], str]  # TODO same as above
    publicKeyRaw: str
    commonName: str
    countryName: str
