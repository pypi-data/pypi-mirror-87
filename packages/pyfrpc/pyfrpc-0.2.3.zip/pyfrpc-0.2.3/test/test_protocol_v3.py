# -*- coding: utf-8 -*-

import pyfrpc
import pytest

from pyfrpc import datetime, timezone, timedelta

from conftest import *


BASIC_CODING_VECTOR = {
    "int":
    [
        (h2b("0fffffffffffffffff"), -0x8000000000000000),
        (h2b("0803"), -2),
        (h2b("0801"), -1),
        (h2b("0800"), 0),
        (h2b("0802"), 1),
        (h2b("0804"), 2),
        (h2b("092043"), 8592),
        (h2b("0ffeffffffffffffff"), 0x7fffffffffffffff),

        # invalid length
        (h2b("08"), RaisesOutOfBound),
        (h2b("0f00000000000000"), RaisesOutOfBound),

        # can't be encoded
        (RaisesIntTooBig, -0x8000000000000001),
        (RaisesIntTooBig, +0x10000000000000000),
    ],
    "double":
    [
        (h2b("18182d4454fb210940"), 3.141592653589793),
    ],
    "string":
    [
        (h2b("2006 'Česko'"), u"Česko"),
    ],
    "binary":
    [
        (h2b("3002cafe"), bytearray(b"\xca\xfe")),
    ],
    "bool":
    [
        (h2b("10"), False),
        (h2b("11"), True),
    ],
    "null":
    [
        (h2b("60"), None)
    ],
    "struct":
    [
        (h2b("5001 06 'Česko' 200b 'Hello World'"),
            {u"Česko": "Hello World"}),
    ],
    "array":
    [
        (h2b("5800"), []),
        (h2b("5803 200d 'Žluťoučký' 0802 3005 'hello'"),
            [u"Žluťoučký", 1, bytearray(b"hello")])
    ],
    "datetime":
    [
        (h2b("28 00 635e285a00000000 bba26a3834"),
            datetime(2017, 12, 6, 21, 17, 23,
                tzinfo=timezone(timedelta(hours=0)))),
        (h2b("28 fc 635e285a00000000 bb226b3834"),
            datetime(2017, 12, 6, 22, 17, 23,
                tzinfo=timezone(timedelta(hours=1)))),
        (h2b("28 fc 5350285a00000000 bba26a3834"),
            datetime(2017, 12, 6, 21, 17, 23,
                tzinfo=timezone(timedelta(hours=1)))),
        (h2b("28 c8 8399275a00000000 bba26a3834"),
            datetime(2017, 12, 6, 21, 17, 23,
                tzinfo=timezone(timedelta(hours=14)))),
        (h2b("28 32 2b0e295a00000000 bba26a3834"),
            datetime(2017, 12, 6, 21, 17, 23,
                tzinfo=timezone(timedelta(hours=-12, minutes=-30)))),
    ]
}


@parametrize_with_cases(BASIC_CODING_VECTOR)
def test_decode(raw, item):
    helper_test_decode(h2b("ca11 0300 70"), raw, item)


@parametrize_with_cases(BASIC_CODING_VECTOR)
def test_encode(raw, item):
    helper_test_encode(h2b("ca11 0300 70"), raw, item, 0x0300)


@parametrize_with_cases({
    "int":
    [
        (h2b("0fffffffffffffffff"), 0x8000000000000000),
        (h2b("0801"), 0xffffffffffffffff),
    ]
})
def test_overflow(raw, item):
    helper_test_encode(h2b("ca11 0300 70"), raw, item, 0x0300)
