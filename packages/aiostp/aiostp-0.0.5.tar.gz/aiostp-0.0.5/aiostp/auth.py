from typing import Union

from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from stpmex.exc import InvalidPassphrase

from .utils import get_file_body


async def gen_pkey(priv_key: Union[str, bytes], priv_key_passphrase: str):
    if not priv_key:
        return None
    pkey = await get_file_body(priv_key)

    try:
        return serialization.load_pem_private_key(
            pkey, priv_key_passphrase.encode('ascii'), default_backend()
        )
    except (ValueError, TypeError, UnsupportedAlgorithm):
        raise InvalidPassphrase
