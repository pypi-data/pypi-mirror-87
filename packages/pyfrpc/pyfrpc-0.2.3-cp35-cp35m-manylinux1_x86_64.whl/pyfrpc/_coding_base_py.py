# -*- coding: utf-8 -*-

import six
import struct

from six.moves import range

from .compat import datetime, timezone, timedelta, unixtimestamp


class FrpcDecoder:
    def __init__(self, buf, offset, version):
        self.buf = buf
        self.idx = offset

        self.version = version

    def offset(self):
        return self.idx

    def decode_data(self):
        r = self._decode_data()

        # Slicing does not check boundaries -> check pass the end access here.
        if self.idx > len(self.buf):
            raise Exception("read out-of-bound")

        return r

    def _decode_data(self):
        S = self.buf[self.idx]
        self.idx += 1

        T = S >> 3      # Type
        L = S & 7       # Additional type info

        if T == 0x01:
            return self._decode_int(L)

        elif T == 0x02:
            # Boolean
            return bool(L & 0x01)

        elif T == 0x03:
            return self._decode_double()

        elif T == 0x04:
            return self._decode_str(L)

        elif T == 0x05:
            return self._decode_datetime()

        elif T == 0x06:
            return self._decode_bin(L)

        elif T == 0x07:
            # Integer (positive)
            return self._decode_varint(L)

        elif T == 0x08:
            # Integer (negative)
            return self._decode_varint(L) * -1

        elif T == 0x0A:
            return self._decode_struct(L)

        elif T == 0x0B:
            return self._decode_list(L)

        elif T == 0x0C:
            # Null
            return None

        else:
            raise Exception("unknown type to decode ({:02X})".format(T))

    def _decode_varint(self, L):
        if self.version >= 0x0200:
            # protocol >= v2.x
            if not (0 <= L <= 7):
                raise Exception("varint is out-of-bound ({})".format(L))

            L += 1

        else:
            # protocol == v1.x
            if not (1 <= L <= 4):
                raise Exception("varint is out-of-bound ({})".format(L))

        result = 0
        i = 0

        while i < L:
            result += self.buf[self.idx + i] << (i << 3)
            i += 1

        self.idx += L

        return result

    def _decode_int(self, L):
        n = self._decode_varint(L)

        if self.version >= 0x0300:
            # protocol >= v3.x (64-bit zigzag encoded)
            n = ((n >> 1) ^ (-(n & 1)))
            return n

        else:
            # protocol == v1.x (32-bit)
            if 0x80000000 & n:
                # negative number
                return n - 0x100000000
            else:
                # positive number
                return n

    def _decode_double(self):
        self.idx += 8
        return struct.unpack_from("<d", self.buf, self.idx - 8)[0]

    def _decode_str(self, L):
        size = self._decode_varint(L)
        self.idx += size
        return self.buf[self.idx - size:self.idx].decode("utf8")

    def _decode_datetime(self):
        # zone (signed 8-bit integer)
        zone = self.buf[self.idx]
        self.idx += 1
        # decode signed part
        zone = zone if (not zone & 0x80) else zone - 0x100
        zone = -zone * 15 * 60

        # timestamp
        if self.version >= 0x0300:
            self.idx += 8
        else:
            self.idx += 4

        # packed timetuple
        p_bytes = self.buf[self.idx:self.idx + 5] + b"\x00\x00\x00"
        p = struct.unpack("<Q", p_bytes)[0]
        self.idx += 5

        tz = timezone(timedelta(seconds=zone))
        dt = datetime(
            ((p >> 29) & 0x7ff) + 1600,  # year    11 bits (29 .. 39)
            ((p >> 25) & 0xf),           # month    4 bits (25 .. 28)
            ((p >> 20) & 0x1f),          # day      5 bits (20 .. 24)
            ((p >> 15) & 0x1f),          # hour     5 bits (15 .. 19)
            ((p >> 9) & 0x3f),           # min      6 bits ( 9 .. 14)
            ((p >> 3) & 0x3f),           # sec      6 bits ( 3 ..  8)
            tzinfo=tz
        )

        return dt

    def _decode_bin(self, L):
        size = self._decode_varint(L)
        self.idx += size
        return self.buf[self.idx - size:self.idx]

    def _decode_struct(self, L):
        members_cnt = self._decode_varint(L)

        result = {}

        for _ in range(members_cnt):
            key_size = self.buf[self.idx]
            key = self.buf[self.idx + 1:self.idx + 1 + key_size].decode("utf8")
            self.idx += 1 + key_size

            value = self._decode_data()

            if key in result:
                raise Exception("duplicated keys ('{}')".format(key))

            result[key] = value

        return result

    def _decode_list(self, L):
        members_cnt = self._decode_varint(L)

        result = []

        for _ in range(members_cnt):
            value = self._decode_data()
            result.append(value)

        return result


class FrpcEncoder:
    def __init__(self, buf, version=0x0201):
        self.buf = buf
        self.version = version

    def encode_data(self, value):
        self._encode_data(value)

    def _encode_data(self, value):
        value_type = type(value)

        if isinstance(value, bool):
            self.buf.append(0x10 | (0x01 if value else 0x00))

        elif isinstance(value, six.integer_types):
            self._encode_int(value)

        elif isinstance(value, float):
            self._encode_double(value)

        elif isinstance(value, six.string_types):
            self._encode_str(value)

        elif isinstance(value, datetime):
            self._encode_datetime(value)

        elif isinstance(value, (bytearray, bytes)):
            self._encode_bin(value)

        elif value is None:
            self._encode_null()

        elif isinstance(value, dict):
            self._encode_struct(value)

        elif isinstance(value, (list, tuple)):
            self._encode_array(value)

        else:
            raise Exception("unknown type to encode ({})".format(value_type))

    def _etwi(self, type_id, value):
        """
        Encode type with integer.
        """

        value_copy = value >> 8
        length = 1

        while value_copy != 0:
            value_copy >>= 8
            length += 1

        if self.version >= 0x0200:
            # protocol >= v2.x
            if length > 8:
                raise Exception("integer too big to encode ({})".format(value))

            self.buf.append((type_id << 3) | (length - 1))

        else:
            # protocol == v1.x
            if length > 4:
                raise Exception("integer too big to encode ({})".format(value))

            self.buf.append(((type_id << 3) | length))

        while length:
            self.buf.append(value & 0xff)
            value >>= 8
            length -= 1

    def _encode_int(self, n):
        if self.version >= 0x0300:
            # protocol v3.x (64-bit zig-zag encoded)
            if not (-0x8000000000000000 <= n <= 0xffffffffffffffff):
                raise Exception("integer too big to encode ({})".format(n))

            # 64-bit unsigned to signed overflow
            if n > 0x7fffffffffffffff:
                n -= 0x10000000000000000

            # zig-zag encoding
            n = ((n << 1) ^ (n >> 63))
            self._etwi(0x01, n)

        elif self.version >= 0x0200:
            # protocol v2.x (64-bit with sign bit)
            if n >= 0:
                self._etwi(0x07, n)
            else:
                self._etwi(0x08, n * -1)

        else:
            # protocol v1.x (32-bit)
            if not (-0x80000000 <= n <= 0x7fffffff):
                raise Exception("integer too big to encode ({})".format(n))

            self._etwi(0x01, n & 0xffffffff)

    def _encode_double(self, value):
        self.buf.append(0x03 << 3)
        self.buf += struct.pack("<d", value)

    def _encode_null(self):
        if self.version < 0x0201:
            # Null was introduced in v2.1
            raise Exception("null can't be encoded")

        self.buf.append(0x0C << 3)

    def _encode_struct(self, value):
        self._etwi(0x0A, len(value))

        for k, v in value.items():
            self._encode_struct_key(k)
            self._encode_data(v)

    def _encode_struct_key(self, key):
        key_data = key.encode("utf8")
        key_size = len(key_data)

        if key_size > 0xff:
            raise Exception("invalid key ({})".format(key))

        self.buf.append(key_size)
        self.buf += key_data

    def _encode_array(self, value):
        self._etwi(0x0B, len(value))

        for item in value:
            self._encode_data(item)

    def _encode_str(self, value):
        value = value.encode("utf8")

        self._etwi(0x04, len(value))
        self.buf += value

    def _encode_datetime(self, data):
        self.buf.append(0x05 << 3)

        timestamp_utc = unixtimestamp(data)
        timestamp_loc = unixtimestamp(data.replace(tzinfo=timezone.utc))

        zone = timestamp_utc - timestamp_loc
        zone = int(round(zone / 60.0 / 15.0))

        self.buf.append(zone & 0xff)

        # 64-bit int is enough to hold datest between years 0 .. 9999
        timestamp = int(timestamp_utc)

        if self.version >= 0x0300:
            # Protocol >= v3.x
            if timestamp >= 0:
                self.buf += struct.pack("<q", timestamp)
            else:
                self.buf += struct.pack("<q", -1)

        else:
            # Protocol <= v2.x
            if (0 <= timestamp <= 0x7fffffff):
                self.buf += struct.pack("<i", timestamp)
            else:
                self.buf += struct.pack("<i", -1)

        tt = data.timetuple()

        assert(0x0 <= (tt[0] - 1600) <= 0x7ff)

        p = (tt[6] + 1) % 7         # weekday  3 bits ( 0 ..  2)
        p |= tt[5] << 3             # sec      6 bits ( 3 ..  8)
        p |= tt[4] << 9             # min      6 bits ( 9 .. 14)
        p |= tt[3] << 15            # hour     5 bits (15 .. 19)
        p |= tt[2] << 20            # day      5 bits (20 .. 24)
        p |= tt[1] << 25            # month    4 bits (25 .. 28)
        p |= (tt[0] - 1600) << 29   # year    11 bits (29 .. 39)

        self.buf += struct.pack("<Q", p)[0:5]

    def _encode_bin(self, value):
        self._etwi(0x06, len(value))
        self.buf += value
