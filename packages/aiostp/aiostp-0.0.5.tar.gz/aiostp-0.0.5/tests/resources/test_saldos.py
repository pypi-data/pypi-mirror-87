from unittest import mock

import pytest
from aiohttp.client_exceptions import ClientResponseError
from stpmex.types import TipoOperacion

import aiostp
from aiostp import Saldo
from aiostp.exc import NoPkeySet
from aiostp.http import Session

aiostp.configure(
    demo=True, empresa='TAMIZI', clabe='646180157000000004', pool_size=4
)


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_consulta_saldo_env_rec():
    saldos = await aiostp.Saldo.consulta_saldo_env_rec()
    assert len(saldos) == 2
    for saldo in saldos:
        assert isinstance(saldo, Saldo)


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_consulta_saldo():
    saldo = await aiostp.Saldo.consulta()

    assert type(saldo) is float
    assert saldo > 0


@pytest.mark.asyncio
@pytest.mark.vcr
@mock.patch('aiostp.session.clabe', '123456789012345678')
async def test_consulta_saldo_for_nonexistent_cuenta():
    with pytest.raises(ClientResponseError) as e:
        await aiostp.Saldo.consulta()
    assert e.value.status == 500


@pytest.mark.asyncio
async def test_no_pkey():
    session = Session()
    await session.configure(demo=True)
    session.pkey = None
    saldo = Saldo(
        montoTotal=1.0, tipoOperacion=TipoOperacion.enviada, totalOperaciones=3
    )
    with mock.patch('aiostp.resources.saldos.session', session):
        with pytest.raises(NoPkeySet):
            await saldo.consulta()
