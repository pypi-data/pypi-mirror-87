# -*- coding: utf-8 -*-

import pyfrpc
import pytest

from pyfrpc import datetime, timezone, timedelta
from pyfrpc import FrpcCall, FrpcFault, FrpcResponse

from conftest import *


TEST_CASES = [
    # long list of integers
    FrpcResponse([x * 7919 for x in range(-2000, 2000)]),

    # deep dict
    FrpcResponse({"a":{"a":{"a":{"a":{"a":{"a":{"a":{"a":{"a":{"a":"b"}}}}}}}}}}),

    # complex message
    FrpcResponse({
        "status": 200,
        "statusMessage": "ok",
        "items": [
            {
                "enabled": False,
                "position": {
                    "lng": 14.5,
                    "lat": 50.486,
                }
            },
            {
                "visible": True,
                "count": 1532486,
                "x":-854623,
            },
            {
                "img": bytearray(b"PNG\x00\xff"),
            },
        ],
        u"Příliš": [
            u"Žluťoučký", u"kůň"
        ],
    }),

    FrpcFault(500, "internal error"),

    FrpcCall(u"Žluťoučký", []),

    FrpcCall("foo", ["bar", {"lng": 16.7, "lat": 45.85}, False, 10000])
]


@parametrize_with_versions([0x0100, 0x0200, 0x0201, 0x0300])
@parametrize_with_list("item", TEST_CASES)
def test_reencode(item, version):
    encoded = pyfrpc.encode(item, version)
    decoded = pyfrpc.decode(encoded)

    assert(item == decoded)


def test_ext():
    # Test that presence of C module complies with PYFRPC_NOEXT env var.

    import os
    PYFRPC_NOEXT = bool(int(os.environ.get('PYFRPC_NOEXT', '0')))

    assert (not pyfrpc.WITH_EXT) == PYFRPC_NOEXT
