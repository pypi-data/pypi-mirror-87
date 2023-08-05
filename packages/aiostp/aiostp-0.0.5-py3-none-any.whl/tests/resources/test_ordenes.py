import datetime as dt

import pandas as pd
import pytest

import aiostp


def test_create_order():
    orden = aiostp.Orden(
        monto=29.00,
        conceptoPago='prueba',
        cuentaBeneficiario='072691004495711499',
        nombreBeneficiario='Pancho Villa',
        institucionContraparte=90646,
        cuentaOrdenante='646180157075068123',
    )

    assert orden.monto == 29.00


def test_create_order_invalid_account_type():
    with pytest.raises(ValueError) as exc_info:
        aiostp.Orden(
            monto=29.00,
            conceptoPago='prueba',
            cuentaBeneficiario='072691004495711499',
            nombreBeneficiario='Pancho Villa',
            institucionContraparte=12345,
            cuentaOrdenante='646180157075068123',
        )
    assert '12345 no se corresponde a un banco' in str(exc_info.value)


def test_create_order_invalid_amount():
    with pytest.raises(ValueError) as exc_info:
        aiostp.Orden(
            monto='rr',
            conceptoPago='prueba',
            cuentaBeneficiario='072691004495711499',
            nombreBeneficiario='Pancho Villa',
            institucionContraparte=90646,
            cuentaOrdenante='646180157075068123',
        )
    assert 'value is not a valid float (type=type_error.float)' in str(
        exc_info.value
    )


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_consulta_ordenes_enviadas():
    enviadas = await aiostp.Orden.consulta_enviadas()

    assert isinstance(enviadas, pd.DataFrame)
    assert len(enviadas) > 0


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_consulta_ordenes_recibidas():
    recibidas = await aiostp.Orden.consulta_recibidas()

    assert isinstance(recibidas, pd.DataFrame)
    assert len(recibidas) > 0


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_consulta():
    consulta = await aiostp.Orden.consulta()

    assert isinstance(consulta, pd.DataFrame)
    assert len(consulta) > 0


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_consulta_ordenes_enviadas_con_fecha():
    enviadas = await aiostp.Orden.consulta_enviadas(dt.date(2020, 4, 20))

    assert isinstance(enviadas, pd.DataFrame)
    assert len(enviadas) > 0


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_consulta_ordenes_enviadas_con_fecha_sin_resultados():
    enviadas = await aiostp.Orden.consulta_enviadas(dt.date(2021, 4, 20))

    assert isinstance(enviadas, pd.DataFrame)
    assert len(enviadas) == 0
