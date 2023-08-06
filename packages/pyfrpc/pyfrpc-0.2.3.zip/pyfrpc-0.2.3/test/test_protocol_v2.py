# -*- coding: utf-8 -*-

import pyfrpc
import pytest

from pyfrpc import datetime, timezone, timedelta
from pyfrpc import FrpcCall, FrpcFault

from conftest import *


BASIC_CODING_VECTOR = {
    "int_pos":
    [
        (h2b("3800"), 0x0),
        (h2b("38ff"), 0xff),
        (h2b("3900ff"), 0xff00),
        (h2b("3a0000ff"), 0xff0000),
        (h2b("3b000000ff"), 0xff000000),
        (h2b("3c00000000ff"), 0xff00000000),
        (h2b("3d0000000000ff"), 0xff0000000000),
        (h2b("3e000000000000ff"), 0xff000000000000),
        (h2b("3f00000000000000ff"), 0xff00000000000000),
        (h2b("3fffffffffffffffff"), 0xffffffffffffffff),
        (h2b("3f1234567812345678"), 0x7856341278563412),
    ],
    "int_neg":
    [
        (h2b("4001"), -0x1),
        (h2b("40ff"), -0xff),
        (h2b("4100ff"), -0xff00),
        (h2b("420000ff"), -0xff0000),
        (h2b("43000000ff"), -0xff000000),
        (h2b("4400000000ff"), -0xff00000000),
        (h2b("450000000000ff"), -0xff0000000000),
        (h2b("46000000000000ff"), -0xff000000000000),
        (h2b("47ffffffffffffff7f"), -0x7fffffffffffffff),
        (h2b("470000000000000080"), -0x8000000000000000),
        (h2b("478765432187654321"), -0x2143658721436587),
    ],
    "double":
    [
        (h2b("18182d4454fb210940"), 3.141592653589793),
        (h2b("18000000000000f03f"), 1.0),
        (h2b("1800000000000024c0"), -10.0),
    ],
    "string":
    [
        (h2b("2000"), ""),
        (h2b("200b 'Hello World'"), "Hello World"),
        (h2b("2006 'Česko'"), u"Česko"),
    ],
    "binary":
    [
        (h2b("3000"), bytearray(b"")),
        (h2b("3002cafe"), bytearray(b"\xca\xfe")),
    ],
    "bool":
    [
        (h2b("10"), False),
        (h2b("11"), True),
    ],
    "struct":
    [
        (h2b("5000"), {}),
        (h2b("5001 06 'Česko' 200b 'Hello World'"),
            {u"Česko": "Hello World"}),

        # key with max length
        (h2b("5001 ff") + b"a"*255 + h2b("2003 'foo'"), {"a"*255: "foo"}),

        # key too long
        (Raises("invalid key"), {"a"*256: "foo"}),

        # duplicated keys
        (h2b("5002 03 'foo' 2001 'a' 03 'foo' 2001 'b'"),
            Raises("duplicated keys")),
    ],
    "array":
    [
        (h2b("5800"), []),
        (h2b("5803 200d 'Žluťoučký' 3801 3005 'hello'"),
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


@parametrize_with_cases(BASIC_CODING_VECTOR)
def test_decode_v20(raw, item):
    helper_test_decode(h2b("ca11 0200 70"), raw, item)


@parametrize_with_cases(BASIC_CODING_VECTOR)
def test_encode_v20(raw, item):
    helper_test_encode(h2b("ca11 0200 70"), raw, item, 0x0200)



@parametrize_with_cases(BASIC_CODING_VECTOR)
def test_decode_v21(raw, item):
    helper_test_decode(h2b("ca11 0201 70"), raw, item)

@parametrize_with_cases(BASIC_CODING_VECTOR)
def test_encode_v21(raw, item):
    helper_test_encode(h2b("ca11 0201 70"), raw, item, 0x0201)



def test_encode_null_v20():
    helper_test_encode(h2b("ca11 0200 70"), Raises("can't be encoded"), None, 0x0200)

def test_encode_null_v21():
    helper_test_encode(h2b("ca11 0201 70"), h2b("60"), None, 0x0201)

def test_decode_null_v21():
    helper_test_decode(h2b("ca11 0201 70"), h2b("60"), None)



TEST_CASES_FRAMES = {
    "call":
    [
        # ok (no argument)
        (h2b("ca11 0201 68 03 'foo'"),
            FrpcCall("foo", [])),

        # ok (1 argument)
        (h2b("ca11 0201 68 07 'Žlutý' 2003 'foo'"),
            FrpcCall(u"Žlutý", ["foo"])),

        # ok (2 arguments)
        (h2b("ca11 0201 68 07 'Žlutý' 2003 'foo' 2003 'bar'"),
            FrpcCall(u"Žlutý", ["foo", "bar"])),

        # missing method name
        (h2b("ca11 0201 68"), RaisesOutOfBound),

        # empty method name
        (Raises("invalid method name"), FrpcCall("", ["foo", "bar"])),
        (h2b("ca11 0201 68 00"), Raises("invalid method name")),
    ],
    "response":
    [
        # missing payload
        (h2b("ca11 0201 70"), RaisesOutOfBound)
    ],
    "fault":
    [
        (h2b("ca11 0201 78 3800 2000"), FrpcFault(0, "")),

        (h2b("ca11 0201 78 39f401 200e 'internal error'"),
            FrpcFault(500, "internal error")),

        # missing payload
        (h2b("ca11 0201 78"), RaisesOutOfBound)
    ],
}


@parametrize_with_cases(TEST_CASES_FRAMES)
def test_decode_frame(raw, item):
    helper_test_decode(b"", raw, item)


@parametrize_with_cases(TEST_CASES_FRAMES)
def test_encode_frame(raw, item):
    helper_test_encode(b"", raw, item, 0x0201)



MALICIOUT_INPUT = [
    h2b("ca11 0201 70 5d 000000000001"),  # array
    h2b("ca11 0201 70 55 000000000001"),  # struct
    h2b("ca11 0201 70 25 000000000001 'Hello World'"),  # string
    h2b("ca11 0201 70 35 000000000001 'Hello World'"),  # binary
]


@parametrize_with_list("item", MALICIOUT_INPUT)
def test_malicious(item):
    helper_test_decode(b"", item, RaisesOutOfBound)

