# -*- coding: utf-8 -*-

import six

from .models import FrpcCall, FrpcResponse, FrpcFault

try:
    from ._coding_base_c import FrpcEncoder as _FrpcEncoder
    from ._coding_base_c import FrpcDecoder as _FrpcDecoder
    WITH_EXT = True
except ImportError:
    from ._coding_base_py import FrpcEncoder as _FrpcEncoder
    from ._coding_base_py import FrpcDecoder as _FrpcDecoder
    WITH_EXT = False


def _encode_data(buf, data, version):
    _FrpcEncoder(buf, version).encode_data(data)


def _decode_data(buf, idx, version):
    decoder = _FrpcDecoder(buf, idx, version)
    return decoder.decode_data(), decoder.offset()


def decode(buf):
    if len(buf) < 5:
        raise Exception("buffer too short ({})".format(buf))

    # We need to access elements of `buf` as integers.
    # For compatibility with python2's str we may need to convert it to bytearray.
    if not (type(buf[0]) is int):
        buf = bytearray(buf)

    # Decode magix (0xca11)
    if buf[0:2] != b"\xca\x11":
        raise Exception("bad magic (0x{:02X}{:02X})".format(*buf[0:2]))

    # Decode protocol version
    version = (buf[2] << 8) + buf[3]

    if not (0x0100 <= version <= 0x03ff):
        raise Exception("unknown protocol version (0x{:04X})".format(version))

    idx = 4

    # Decode non-data payload
    B, idx = buf[idx], idx + 1
    T = B >> 3

    # Method call
    if T == 0x0d:
        size = buf[idx]
        name = buf[idx + 1:idx + 1 + size].decode("utf8")
        idx += 1 + size

        if size == 0:
            raise Exception("invalid method name")

        args = []

        while idx < len(buf):
            data, idx = _decode_data(buf, idx, version)
            args.append(data)

        return FrpcCall(name=name, args=args)

    # Method response
    elif T == 0x0e:
        data, idx = _decode_data(buf, idx, version)

        return FrpcResponse(data=data)

    # Fault response
    elif T == 0x0f:
        err, idx = _decode_data(buf, idx, version)
        msg, idx = _decode_data(buf, idx, version)

        if not (isinstance(err, six.integer_types) and isinstance(msg, six.string_types)):
            raise Exception("malformed FprcFault frame")

        return FrpcFault(err=err, msg=msg)

    else:
        raise Exception("unknown type to decode {:02X}".format(T))


def encode(payload, version):
    if not (0x0100 <= version <= 0x03ff):
        raise Exception("unknown protocol version(0x{:04X})".format(version))

    buf = bytearray((0xca, 0x11, version >> 8, version & 0xff))

    # Method call
    if isinstance(payload, FrpcCall):
        name = payload.name.encode("utf8")

        if not (0 < len(name) <= 0xff):
            raise Exception("invalid method name ({})".format(name))

        buf.append(0x0d << 3)
        buf.append(len(name))
        buf += name

        for arg in payload.args:
            _encode_data(buf, arg, version)

    # Method response
    elif isinstance(payload, FrpcResponse):
        buf.append(0x0e << 3)
        _encode_data(buf, payload.data, version)

    # Fault response
    elif isinstance(payload, FrpcFault):
        buf.append(0x0f << 3)

        _encode_data(buf, payload.err, version)
        _encode_data(buf, payload.msg, version)

    else:
        raise Exception("unknown type to encode ({})".format(type(payload)))

    return buf
