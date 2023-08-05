import datetime as dt

import pytest

from aiostp.utils import get_file_body, strftime, strptime


def test_strftime():
    assert strftime(dt.date(2020, 4, 20)) == '20200420'


def test_strptime():
    assert strptime('20200420') == dt.date(2020, 4, 20)


@pytest.mark.asyncio
async def test_get_file_body_file():
    res = await get_file_body('tests/data/test.txt')
    assert res == b'hello world'


@pytest.mark.asyncio
async def test_get_file_body_bytes():
    res = await get_file_body(b'hello world')
    assert res == b'hello world'
