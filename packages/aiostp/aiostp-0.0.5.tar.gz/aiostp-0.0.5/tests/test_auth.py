import pytest
from cryptography.hazmat.backends.openssl.rsa import _RSAPrivateKey

from aiostp.auth import gen_pkey


@pytest.mark.asyncio
async def test_empty_priv_key():
    res = await gen_pkey('', '')

    assert res is None


@pytest.mark.asyncio
async def test_gen_pkey():
    res = await gen_pkey('tests/data/pkey.pem', '12345678')

    assert type(res) == _RSAPrivateKey
