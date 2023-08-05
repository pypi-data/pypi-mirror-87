import datetime as dt
from unittest import mock

import pytest
from pydantic.dataclasses import dataclass

import aiostp
from aiostp.exc import NoPkeySet
from aiostp.http.client import Session
from aiostp.resources.base import Resource


@dataclass
class Mocker(Resource):
    name: str
    time: dt.date
    _endpoint = '123'
    _firma_fieldnames = ['1123']
    empresa = '123'


def test_to_dict():
    orden = aiostp.Orden(
        monto=29.00,
        conceptoPago='prueba',
        cuentaBeneficiario='072691004495711499',
        nombreBeneficiario='Pancho Villa',
        institucionContraparte=90646,
        cuentaOrdenante='646180157075068123',
    )

    orden_dict = orden.to_dict()

    assert orden_dict['monto'] == 29.00


def test_to_dict_w_date():
    mocker = Mocker(name='manu', time=dt.date(2020, 11, 29))

    mocker_dict = mocker.to_dict()

    assert mocker_dict


@pytest.mark.asyncio
async def test_no_pkey():
    session = Session()
    await session.configure(demo=True)

    with mock.patch('aiostp.resources.base.session', session):
        session.pkey = None
        base = Resource()
        with pytest.raises(NoPkeySet):
            base._firma_consulta(
                dict(
                    fechaOperacion='20201129',
                    claveRastreo='hola',
                    institucionOperante='STP',
                )
            )
