# -*- coding: utf-8 -*-

"""
Those tests are testing interoperability between pyfrpc and fastrpc (original
implementation).
"""

import conftest
import pytest


if conftest.SKIP_FASTRPC: #True or not pytest.config.getoption("--with-fastrpc"):
    pytestmark = pytest.mark.skip("must be enabled using --with-fastrpc flag")
else:
    import fastrpc


import pyfrpc

from test_protocol import (
    TEST_CASES,
    parametrize_with_list,
    parametrize_with_versions
)


@parametrize_with_versions([0x0100, 0x0200, 0x0201, 0x0300])
@parametrize_with_list("item", TEST_CASES)
def test_fastrpc_encode(item, version):
    kwargs = {
        "useBinary": True,
        "protocolVersionMajor": version >> 8,
        "protocolVersionMinor": version & 0xff,
    }

    if type(item) is pyfrpc.FrpcCall:
        kwargs["params"] = item.args
        kwargs["methodname"] = item.name

    if type(item) is pyfrpc.FrpcFault:
        kwargs["params"] = fastrpc.Fault(item.err, item.msg)

    if type(item) is pyfrpc.FrpcResponse:
        kwargs["params"] = tuple((item.data,))

    encoded = fastrpc.dumps(**kwargs)
    decoded = pyfrpc.decode(encoded)

    assert(item == decoded)


@parametrize_with_versions([0x0100, 0x0200, 0x0201, 0x0300])
@parametrize_with_list("item", TEST_CASES)
def test_fastrpc_decode(item, version):
    """
    Tests involving negative integers are failing because fastrpc decoder
    effectively turns signed 32-bit integers into unsigned 64-bit integers.
    """

    encoded = pyfrpc.encode(item, version)

    try:
        decoded = fastrpc.loads(bytes(encoded), useBinary=True)
    except fastrpc.Fault as e:
        decoded = e

    if type(item) is pyfrpc.FrpcCall:
        assert(item.name == decoded[1])
        assert(item.args == list(decoded[0]))

    elif type(item) == pyfrpc.FrpcResponse:
        assert(item.data == decoded[0])

    else:
        assert(type(item) is pyfrpc.FrpcFault)
        assert(item.err == decoded.faultCode)
        assert(item.msg == decoded.faultString)
