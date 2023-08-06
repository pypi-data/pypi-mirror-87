# -*- coding: utf-8 -*-

import pyfrpc
import pytest

from pyfrpc import datetime, timezone, timedelta

from conftest import *


TEST_CASES = {
    "int":
    [
        (h2b("0c00000080"), -0x80000000),
        (h2b("0cffffffff"), -0x1),
        (h2b("0900"), 0x0),
        (h2b("0901"), 0x1),
        (h2b("0c78563412"), 0x12345678),
        (h2b("0cffffff7f"), 0x7fffffff),

        # invalid length
        (h2b("08"), RaisesOutOfBound),
        (h2b("0d"), RaisesOutOfBound),

        # can't be encoded
        (RaisesIntTooBig, -0x80000001),
        (RaisesIntTooBig, +0x80000000),
    ],
    "double":
    [
        (h2b("18182d4454fb210940"), 3.141592653589793),
    ],
    "string":
    [
        (h2b("2100"), ""),
        (h2b("2106 'Česko'"), u"Česko"),
    ],
    "binary":
    [
        (h2b("3100"), bytearray(b"")),
        (h2b("3102cafe"), bytearray(b"\xca\xfe")),
    ],
    "null":
    [
        # can't be encoded
        (Raises("can't be encoded"), None)
    ],
    "bool":
    [
        (h2b("10"), False),
        (h2b("11"), True),
    ],
    "struct":
    [
        (h2b("5100"), {}),
        (h2b("5101 06 'Česko' 210b 'Hello World'"),
            {u"Česko": "Hello World"}),
    ],
    "array":
    [
        (h2b("5900"), []),
        (h2b("5903 210d 'Žluťoučký' 0901 3105 'hello'"),
            [u"Žluťoučký", 1, bytearray(b"hello")])
    ],
    "datetime":
    [
        (h2b("28 00 635e285a bba26a3834"),
            datetime(2017, 12, 6, 21, 17, 23,
                tzinfo=timezone(timedelta(hours=0)))),
        (h2b("28 fc 635e285a bb226b3834"),
            datetime(2017, 12, 6, 22, 17, 23,
                tzinfo=timezone(timedelta(hours=1)))),
        (h2b("28 fc 5350285a bba26a3834"),
            datetime(2017, 12, 6, 21, 17, 23,
                tzinfo=timezone(timedelta(hours=1)))),
        (h2b("28 c8 8399275a bba26a3834"),
            datetime(2017, 12, 6, 21, 17, 23,
                tzinfo=timezone(timedelta(hours=14)))),
        (h2b("28 32 2b0e295a bba26a3834"),
            datetime(2017, 12, 6, 21, 17, 23,
                tzinfo=timezone(timedelta(hours=-12, minutes=-30)))),
    ]
}


@parametrize_with_cases(TEST_CASES)
def test_decode(raw, item):
    helper_test_decode(h2b("ca11 0100 70"), raw, item)


@parametrize_with_cases(TEST_CASES)
def test_encode(raw, item):
    helper_test_encode(h2b("ca11 0100 70"), raw, item, 0x0100)
