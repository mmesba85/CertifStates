from typing import List, Union, TypedDict


class Collision(TypedDict):
    """
    Collision object, returned by `checker` module in a list of pandas' data frames
    """
    keyType: str
    dnsNames: Union[List[str], str]
    ipAdressess: Union[List[str], str]
    publicKeyRaw: str
    commonName: str
    countryName: str
