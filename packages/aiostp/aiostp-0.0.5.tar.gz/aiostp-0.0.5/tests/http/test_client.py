from unittest import mock

import pytest
from aiohttp.client_exceptions import ClientResponseError
from stpmex.exc import InvalidPassphrase, StpmexException

from aiostp.http.client import Session

CUENTA_ENDPOINT = '/cuentaModule/fisica'


class MockResponse:
    def __init__(self, json, status):
        self._json = json
        self.status = status

    async def json(self):
        return self._json

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


@pytest.mark.asyncio
async def test_forbidden_without_vpn():
    session = Session()
    await session.configure(demo=False)
    with pytest.raises(ClientResponseError) as exc_info:
        await session.get('/application.wadl')
    assert exc_info.value.status == 403


@pytest.mark.asyncio
async def test_error():
    error = dict(descripcion='unknown code', id=999999)
    session = Session()
    await session.configure(demo=True)

    with mock.patch(
        'aiostp.http.client.aiohttp.ClientSession.request',
        return_value=MockResponse(error, 200),
    ):
        with pytest.raises(StpmexException) as exc_info:
            await session.post(CUENTA_ENDPOINT, data={})
        exc = exc_info.value

    assert type(exc) == StpmexException


@pytest.mark.asyncio
async def test_incorrect_passphrase():
    session = Session()
    with pytest.raises(InvalidPassphrase):
        await session.configure(
            priv_key='tests/data/pkey.pem', priv_key_passphrase='wrong'
        )


@pytest.mark.asyncio
async def test_configure():
    session = Session()
    await session.configure(
        empresa='EMPRESA PRUEBA', clabe='1234567890', pool_size=6
    )
    # running configure again just to re-generate aiohttp session
    await session.configure()

    assert session.empresa == 'EMPRESA PRUEBA'
    assert session.clabe == '1234567890'
    assert session._connection_pool_size == 6
