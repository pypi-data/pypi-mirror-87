from typing import List
from xml.etree import ElementTree

from pydantic.dataclasses import dataclass
from stpmex.auth import compute_signature
from stpmex.resources import Saldo as SaldoSTPMex

from ..exc import NoPkeySet
from ..http import session
from .base import Resource


@dataclass
class Saldo(Resource, SaldoSTPMex):
    @classmethod
    async def consulta_saldo_env_rec(cls) -> List['Saldo']:  # type: ignore
        data = dict(empresa=session.empresa, firma=cls._firma_consulta({}))
        resp = await session.post(cls._endpoint, data)
        saldos = []
        for saldo in resp['saldos']:  # type: ignore
            del saldo['empresa']
            saldos.append(cls(**saldo))  # type: ignore
        return saldos

    @classmethod
    async def consulta(cls) -> float:  # type: ignore
        """
        cuenta es la CLABE de la empresa

        Based on:
        https://stpmex.zendesk.com/hc/es/articles/360002812571-consultaSaldoCuenta
        """
        if not session.pkey:
            raise NoPkeySet()
        firma = compute_signature(session.pkey, session.clabe)
        data = f'''
<soapenv:Envelope
        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:h2h="http://h2h.integration.spei.enlacefi.lgec.com/">
    <soapenv:Body>
        <h2h:consultaSaldoCuenta>
            <cuenta>{session.clabe}</cuenta>
            <firma>{firma}</firma>
        </h2h:consultaSaldoCuenta>
    </soapenv:Body>
</soapenv:Envelope>
'''
        resp = await session.soap_request('POST', '', data)
        root = ElementTree.fromstring(resp)
        saldo = root.findtext('.//saldo') or 0
        return float(saldo)
