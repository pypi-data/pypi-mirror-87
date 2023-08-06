import base64
import pyfrpc
import pytest
import re
import six


PYFRPC_MODEL_CLASSES = (pyfrpc.FrpcResponse, pyfrpc.FrpcFault, pyfrpc.FrpcCall)



def pytest_addoption(parser):
    parser.addoption("--with-fastrpc", action="store_true",
        help="run tests requiring installation of fastrpc")

def pytest_configure(config):
    global SKIP_FASTRPC
    SKIP_FASTRPC = not config.getoption("--with-fastrpc")



def b2h(binary):
    return base64.b16encode(binary)


def h2b(hexstring):
    if six.PY3 or (six.PY2 and isinstance(hexstring, unicode)):
        hexstring = hexstring.encode("utf8")

    while True:
        m = re.match(b"^(.*?)[\"'](.*?)[\"'](.*)$", hexstring)

        if not m:
            break

        hexstring = m.group(1) + b2h(m.group(2)) + m.group(3)

    hexstring = hexstring.upper().replace(b" ", b"")

    return base64.b16decode(hexstring)


def parametrize_with_cases(cases):
    inputs = []
    ids = []

    for name, pairs in cases.items():
        for idx, (raw, item) in enumerate(pairs):
            inputs.append((raw, item))
            ids.append("{}#{}".format(name, idx + 1))

    return pytest.mark.parametrize("raw, item", inputs, ids=ids)


def parametrize_with_list(variables, cases):
    ids = ["#{}".format(i + 1) for i in range(len(cases))]
    return pytest.mark.parametrize(variables, cases, ids=ids)


def parametrize_with_versions(versions):
    ids = ["v{}.{}".format(v >> 8, v & 0xff) for v in versions]
    return pytest.mark.parametrize("version", versions, ids=ids)


class Raises:
    """
    Class which denotes that encoding/decoding is not possible. It can be used
    in test cases in place of `raw` or `item` fields. If so, than test helpers
    check that encode/decode function raises exception.
    """

    def __init__(self, match=""):
        self.match = match


RaisesOutOfBound = Raises(r"(out-of-bound)|(index out of range)")
RaisesIntTooBig = Raises(r"(integer too big)|(int too large)")


def helper_test_decode(raw_prefix, raw, item):
    if isinstance(raw, Raises):
        pytest.skip()

    raw = raw_prefix + raw

    if isinstance(item, Raises):
        with pytest.raises(Exception, match=item.match):
            decoded = pyfrpc.decode(raw)

    else:
        decoded = pyfrpc.decode(raw)

        if isinstance(decoded, pyfrpc.FrpcResponse):
            assert(item == decoded.data)
        else:
            assert(item == decoded)


def helper_test_encode(raw_prefix, raw, item, version):
    if isinstance(item, Raises):
        pytest.skip()

    if not isinstance(item, PYFRPC_MODEL_CLASSES):
        item = pyfrpc.FrpcResponse(item)

    if isinstance(raw, Raises):
        with pytest.raises(Exception, match=raw.match):
            encoded = pyfrpc.encode(item, version=version)

    else:
        encoded_right = raw_prefix + raw
        encoded = pyfrpc.encode(item, version=version)
        assert(b2h(encoded) == b2h(encoded_right))
