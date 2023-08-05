import os
from typing import Any, Dict, List, Optional, Union

import aiohttp
from aiohttp.client_reqrep import ClientResponse
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from stpmex.client import _raise_description_error_exc, _raise_description_exc

from ..auth import gen_pkey
from ..version import __version__ as client_version

DEMO_HOST = 'https://demo.stpmex.com:7024'
PROD_HOST = 'https://prod.stpmex.com'


class Session:
    base_url: str
    soap_url: str
    empresa: str
    pkey: Optional[RSAPrivateKey]

    _session: Optional[aiohttp.ClientSession] = None

    _connection_pool_size: int
    _ssl_verify: bool

    def __init__(self):
        self.empresa = os.getenv('EMPRESA', '')
        self.clabe = os.getenv('CLABE', '')

        self._ssl_verify = True
        self._connection_pool_size = 4
        self.pkey = None

        self.base_url = f'{PROD_HOST}/speiws/rest'
        self.soap_url = f'{PROD_HOST}/spei/webservices/SpeiConsultaServices'

    async def configure(
        self,
        demo: bool = False,
        priv_key: Union[str, bytes] = '',
        priv_key_passphrase: str = '',
        empresa: str = '',
        clabe: str = '',
        pool_size: Optional[int] = None,
    ):
        priv_key = priv_key or os.getenv('STP_PRIVATE_LOCATION', '')
        priv_key_passphrase = priv_key_passphrase or os.getenv(
            'STP_KEY_PASSPHRASE', ''
        )
        self.pkey = await gen_pkey(priv_key, priv_key_passphrase)

        if demo:
            host_url = DEMO_HOST
            self._ssl_verify = False
        else:
            host_url = PROD_HOST
            self._ssl_verify = True
        self.base_url = f'{host_url}/speiws/rest'
        self.soap_url = f'{host_url}/spei/webservices/SpeiConsultaServices'

        if empresa:
            self.empresa = empresa

        if clabe:
            self.clabe = clabe

        if pool_size:
            self._connection_pool_size = pool_size

        if self._session is not None:
            await self._session.close()
            self._session = None
        await self.session()

    async def session(self):
        if self._session is None:
            conn = aiohttp.TCPConnector(
                limit=self._connection_pool_size, ssl=self._ssl_verify
            )
            self._session = aiohttp.ClientSession(
                connector=conn,
                headers={'User-Agent': f'stpmex-python/{client_version}'},
            )
        return self._session

    async def get(
        self,
        endpoint: str,
    ) -> Union[Dict[str, Any], List[Any]]:
        return await self.request('GET', endpoint, {})

    async def post(
        self, endpoint: str, data: Dict[str, Any]
    ) -> Union[Dict[str, Any], List[Any]]:
        return await self.request('POST', endpoint, data)

    async def request(
        self,
        method: str,
        endpoint: str,
        data: Dict[str, Any],
        **kwargs: Any,
    ) -> Union[Dict[str, Any], List[Any]]:
        session = await self.session()
        url = self.base_url + endpoint
        async with session.request(
            method,
            url,
            json=data,
            **kwargs,
        ) as response:
            await self._check_response(response)
            resultado = await response.json()
        if 'resultado' in resultado:  # Some responses are enveloped
            resultado = resultado['resultado']
        return resultado

    async def soap_request(
        self,
        method: str,
        endpoint: str,
        data: str,
        **kwargs: Any,
    ):
        session = await self.session()
        url = self.soap_url + endpoint
        async with session.request(method, url, json=data) as response:
            if response.status != 200:
                response.raise_for_status()
            resultado = await response.text()
        return resultado

    @staticmethod
    async def _check_response(response: ClientResponse) -> None:
        if response.status != 200:
            response.raise_for_status()
        resp = await response.json()
        if isinstance(resp, dict):
            try:
                _raise_description_error_exc(resp)
            except KeyError:
                ...
            try:
                assert resp['descripcion']
                _raise_description_exc(resp)
            except (AssertionError, KeyError):
                ...
        response.raise_for_status()
