import asyncio
import datetime as dt
from typing import Optional

import pandas as pd
from pydantic.dataclasses import dataclass
from stpmex.exc import NoOrdenesEncontradas
from stpmex.resources import Orden as OrdenSTPMex
from stpmex.types import Estado, TipoOperacion

from ..http import session
from ..utils import strftime, strptime
from .base import Resource

STP_BANK_CODE = 90646


@dataclass
class Orden(Resource, OrdenSTPMex):
    @classmethod
    async def _consulta_fecha(  # type: ignore
        cls, tipo: TipoOperacion, fechaOperacion: Optional[dt.date] = None
    ) -> pd.DataFrame:
        """
        Exclude the fechaOperacion if looking up transactions from the same
        day or when the fechaOperacion is in the future, in the event of this
        function being called during non-banking hours (9am – 6pm) / days.
        """
        endpoint = cls._endpoint + '/consOrdenesFech'
        consulta = dict(empresa=session.empresa, estado=tipo)
        if fechaOperacion:
            consulta['fechaOperacion'] = strftime(fechaOperacion)
        consulta['firma'] = cls._firma_consulta(consulta)
        try:
            resp = await session.post(endpoint, consulta)
        except NoOrdenesEncontradas:
            ordenes = pd.DataFrame()
        else:
            ordenes = pd.DataFrame.from_records(
                [item for item in resp['lst'] if item],  # type: ignore
            )
            ordenes.fechaOperacion = ordenes.fechaOperacion.apply(strptime)
            ordenes.estado = ordenes.estado.apply(lambda x: Estado(x))
        for col in (key for key in ordenes.keys() if key.startswith('ts')):
            ordenes[col] = ordenes[col].apply(cls._sanitize_timestamp)
        return ordenes

    @classmethod
    async def consulta_recibidas(  # type: ignore
        cls, fecha_operacion: Optional[dt.date] = None
    ) -> pd.DataFrame:
        """
        Consultar
        """
        return await cls._consulta_fecha(
            TipoOperacion.recibida, fecha_operacion
        )

    @classmethod
    async def consulta_enviadas(  # type: ignore
        cls, fecha_operacion: Optional[dt.date] = None
    ) -> pd.DataFrame:
        return await cls._consulta_fecha(
            TipoOperacion.enviada, fecha_operacion
        )

    @classmethod
    async def consulta(
        cls, fecha_operacion: Optional[dt.date] = None
    ) -> pd.DataFrame:
        recibidas, enviadas = await asyncio.gather(
            cls.consulta_recibidas(fecha_operacion),
            cls.consulta_enviadas(fecha_operacion),
        )
        return pd.concat([recibidas, enviadas])

    @staticmethod
    def _sanitize_timestamp(row):
        row /= 10 ** 3  # convertir de milisegundos a segundos
        if row > 10 ** 9:
            row = dt.datetime.fromtimestamp(row).strftime('%Y-%m-%d')
        return row
