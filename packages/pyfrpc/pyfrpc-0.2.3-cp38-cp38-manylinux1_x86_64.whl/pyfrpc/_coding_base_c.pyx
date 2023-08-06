# -*- coding: utf-8 -*-

import cython

from .compat import datetime, timezone, timedelta, unixtimestamp

from libc.stdint cimport *
from libc.string cimport memcpy

from cpython.bytes cimport PyBytes_Size, PyBytes_AsString
from cpython.version cimport PY_MAJOR_VERSION


cdef extern from "Python.h":
    char* PyUnicode_AsUTF8AndSize(object unicode, Py_ssize_t *size)
    # Return a pointer to the UTF-8 encoding of the Unicode object, and store
    # the size of the encoded representation (in bytes) in size. The size
    # argument can be NULL; in this case no size will be stored. The returned
    # buffer always has an extra null byte appended (not included in size),
    # regardless of whether there are any other null code points.
    #
    # In the case of an error, NULL is returned with an exception set and no
    # size is stored.
    #
    # This caches the UTF-8 representation of the string in the Unicode object,
    # and subsequent calls will return a pointer to the same buffer. The caller
    # is not responsible for deallocating the buffer.
    #
    # New in version 3.3.

    Py_ssize_t PyByteArray_Size(object bytearray)
    # Return the size of bytearray after checking for a NULL pointer.

    char* PyByteArray_AsString(object bytearray)
    # Return the contents of bytearray as a char array after checking for a NULL
    # pointer. The returned array always has an extra null byte appended.

    int PyByteArray_Resize(object bytearray, Py_ssize_t len)
    # Resize the internal buffer of bytearray to len.



@cython.final
cdef class FrpcDecoder:
    cdef BinaryReader io
    cdef int32_t version

    def __cinit__(self, buf, offset, version):
        self.io = BinaryReader(buf, offset)
        self.version = version

    cpdef offset(self):
        return self.io.offset()

    cpdef decode_data(self):
        cdef uint8_t S = self.io.read_int(1)

        cdef uint8_t T = S >> 3          # Type
        cdef uint8_t L = S & 7           # Additional type info

        if T == 0x01:
            return self._decode_int(L)

        elif T == 0x02:
            # Boolean
            return <bint>(L & 0x01)

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
            return self._decode_varint(L) * <object>(-1)

        elif T == 0x0A:
            return self._decode_struct(L)

        elif T == 0x0B:
            return self._decode_list(L)

        elif T == 0x0C:
            return None

        else:
            raise Exception("unknown type to decode ({:02X})".format(T))

    cdef uint64_t _decode_varint(self, uint8_t L) except? 0:
        if self.version >= 0x0200:
            # protocol >= v2.x
            if not (0 <= L <= 7):
                raise Exception("varint is out-of-bound ({})".format(L))

            return self.io.read_int(L + 1)

        else:
            # protocol == v1.x
            if not (1 <= L <= 4):
                raise Exception("varint is out-of-bound ({})".format(L))

            return self.io.read_int(L)

    cdef _decode_int(self, uint8_t L):
        cdef uint64_t n = self._decode_varint(L)

        if self.version >= 0x0300:
            # protocol >= v3.x (64-bit zigzag encoded)
            n = ((n >> 1) ^ (-(n & 1)))
            return <int64_t>(n)

        else:
            # protocol == v1.x (32-bit)
            return <int32_t>(n)

    cdef _decode_double(self):
        cdef double value
        self.io.read_raw(&value, 8)
        return value

    cdef _decode_str(self, uint8_t L):
        return self.io.read_utf8(self._decode_varint(L))

    cdef _decode_datetime(self):
        # zone (signed 8-bit integer)
        cdef int32_t zone = <int8_t>self.io.read_int(1)
        zone = -zone * 15 * 60

        # timestamp
        if self.version >= 0x0300:
            self.io.read_int(8)
        else:
            self.io.read_int(4)

        # packed timetuple
        cdef uint64_t p = self.io.read_int(5)

        tz = timezone(timedelta(seconds=zone))
        dt = datetime(
            ((p >> 29) & 0x7ff) + 1600,  # year    11 bits (29 .. 39)
            ((p >> 25) & 0xf),           # month    4 bits (25 .. 28)
            ((p >> 20) & 0x1f),          # day      5 bits (20 .. 24)
            ((p >> 15) & 0x1f),          # hour     5 bits (15 .. 19)
            ((p >>  9) & 0x3f),          # min      6 bits ( 9 .. 14)
            ((p >>  3) & 0x3f),          # sec      6 bits ( 3 ..  8)
            tzinfo=tz
        )

        return dt

    cdef _decode_bin(self, uint8_t L):
        return self.io.read_bytes(self._decode_varint(L))

    cdef _decode_struct(self, uint8_t L):
        cdef uint64_t members_cnt = self._decode_varint(L)
        cdef uint32_t key_size

        result = {}

        for _ in range(members_cnt):
            key = self.io.read_utf8(self.io.read_int(1))
            value = self.decode_data()

            if key in result:
                raise Exception("duplicated keys ('{}')".format(key))

            result[key] = value

        return result

    cdef _decode_list(self, uint8_t L):
        cdef int64_t members_cnt = self._decode_varint(L)
        cdef int64_t i

        self.io.assert_bytes_available(members_cnt)

        result = [None] * members_cnt

        for i in range(members_cnt):
            result[i] = self.decode_data()

        return result


@cython.final
cdef class FrpcEncoder:
    cdef BinaryWriter io
    cdef UtfEncoder utf8
    cdef int32_t version

    def __cinit__(self, bytearray buf, version=0x0201):
        self.io = BinaryWriter(buf)
        self.utf8 = UtfEncoder()
        self.version = version

    cpdef encode_data(self, value):
        self._encode_data(value)
        self.io.finalize()

    cdef _encode_data(self, value):
        value_type = type(value)

        if value_type is bool:
            self.io.write_int(0x10 | (0x01 if value else 0x00), 1)

        elif (value_type is int) or (value_type is long):
            self._encode_int(value)

        elif value_type is float:
            self._encode_double(value)

        elif (value_type is str) or (value_type is unicode):
            self._encode_str(value)

        elif (value_type is bytearray) or (value_type is bytes):
            self._encode_bin(value)

        elif value is None:
            self._encode_null()

        elif value_type is dict:
            self._encode_struct(value)

        elif (value_type is list) or (value_type is tuple):
            self._encode_array(value)

        elif value_type is datetime:
            self._encode_datetime(value)

        else:
            raise Exception("unknown type to encode ({})".format(value_type))

    cdef _etwi(self, int32_t type_id, uint64_t value):
        """
        Encode type with integer.
        """

        cdef uint64_t value_copy = value >> 8
        cdef int32_t length = 1

        while value_copy != 0:
            value_copy >>= 8
            length += 1

        if self.version >= 0x0200:
            # protocol >= v2.x
            self.io.write_int((type_id << 3) | (length - 1), 1)
            self.io.write_int(value, length)

        else:
            # protocol == v1.x
            if length > 4:
                raise Exception("integer too big to encode ({})".format(value))

            self.io.write_int(((type_id << 3) | length), 1)
            self.io.write_int(value, length)

    cdef _encode_int(self, value):
        cdef int64_t n

        if self.version >= 0x0300:
            # protocol v3.x (64-bit zig-zag encoded)

            if value >= 0:
                n = <uint64_t>(value)
            else:
                n = <int64_t>(value)

            n = ((n << 1) ^ (n >> 63))
            self._etwi(0x01, n)

        elif self.version >= 0x0200:
            # protocol v2.x (64-bit with sign bit)
            if value >= 0:
                self._etwi(0x07, value)
            else:
                self._etwi(0x08, value * -1)

        else:
            # protocol v1.x (32-bit)
            n = <int64_t>(value)

            if not (-0x80000000 <= n <= 0x7fffffff):
                raise Exception("integer too big to encode ({})".format(value))

            self._etwi(0x01, <uint32_t>(n))

    cdef _encode_double(self, double value):
        self.io.write_int(0x03 << 3, 1)
        self.io.write_raw(&value, 8)

    cdef _encode_null(self):
        if self.version < 0x0201:
            # Null was introduced in v2.1
            raise Exception("null can't be encoded")

        self.io.write_int(0x0C << 3, 1)

    cdef _encode_struct(self, dict value):
        self._etwi(0x0A, len(value))

        for k, v in value.iteritems():
            self._encode_struct_key(k)
            self._encode_data(v)

    cdef _encode_struct_key(self, key):
        self.utf8.encode(key)

        if self.utf8.size > 0xff:
            raise Exception("invalid key ({})".format(key))

        self.io.write_int(self.utf8.size, 1)
        self.io.write_raw(self.utf8.data, self.utf8.size)

    cdef _encode_array(self, value):
        self._etwi(0x0B, len(value))

        for item in value:
            self._encode_data(item)

    cdef _encode_str(self, value):
        self.utf8.encode(value)

        self._etwi(0x04, self.utf8.size)
        self.io.write_raw(self.utf8.data, self.utf8.size)

    cdef _encode_datetime(self, data):
        self.io.write_int(0x05 << 3, 1)

        timestamp_utc = unixtimestamp(data)
        timestamp_loc = unixtimestamp(data.replace(tzinfo=timezone.utc))

        zone = timestamp_utc - timestamp_loc
        zone = round(zone / 60.0 / 15.0)

        self.io.write_int(<uint8_t><int8_t>zone, 1)

        # 64-bit int is enough to hold datest between years 0 .. 9999
        cdef int64_t timestamp = timestamp_utc

        if self.version >= 0x0300:
            # Protocol >= v3.x
            if timestamp >= 0:
                self.io.write_int(timestamp, 8)
            else:
                self.io.write_int(0xffffffffffffffff, 8)

        else:
            # Protocol <= v2.x
            if (0 <= timestamp <= 0x7fffffff):
                self.io.write_int(timestamp, 4)
            else:
                self.io.write_int(0xffffffff, 4)

        tt = data.timetuple()

        assert(0x0 <= (tt[0] - 1600) <= 0x7ff)

        cdef uint64_t p
        p = (tt[6] + 1) % 7         # weekday  3 bits ( 0 ..  2)
        p |= tt[5] << 3             # sec      6 bits ( 3 ..  8)
        p |= tt[4] << 9             # min      6 bits ( 9 .. 14)
        p |= tt[3] << 15            # hour     5 bits (15 .. 19)
        p |= tt[2] << 20            # day      5 bits (20 .. 24)
        p |= tt[1] << 25            # month    4 bits (25 .. 28)
        p |= (tt[0] - 1600) << 29   # year    11 bits (29 .. 39)

        self.io.write_int(p, 5)

    cdef _encode_bin(self, value):
        cdef Py_ssize_t size = len(value)

        self._etwi(0x06, size)

        if isinstance(value, bytes):
            self.io.write_raw(PyBytes_AsString(value), size)

        elif isinstance(value, bytearray):
            self.io.write_raw(PyByteArray_AsString(value), size)

        else:
            Exception("this should never happen")


################################################################################
# Low level binary IO
################################################################################

@cython.final
cdef class BinaryReader:
    cdef object _buf
    cdef uint8_t *_buf_begin
    cdef uint8_t *_buf_end
    cdef uint8_t *_buf_ptr

    def __cinit__(self, buf, offset):
        self._buf = buf
        self._buf_begin = buf
        self._buf_end = self._buf_begin + len(buf)
        self._buf_ptr = self._buf_begin + <int64_t>offset

    cdef int64_t offset(self):
        return self._buf_ptr - self._buf_begin

    cdef uint64_t read_int(self, uint8_t size) except? 0:
        cdef uint8_t *data = self._inc_ptr(size)

        cdef uint64_t result = 0
        cdef uint8_t i

        for i in range(size):
            result += <uint64_t>(data[i]) << (i << 3)

        return result

    cdef read_utf8(self, uint64_t size):
        return self._inc_ptr(size)[0:size].decode("utf8")

    cdef read_bytes(self, uint64_t size):
        return self._inc_ptr(size)[0:size]

    cdef read_raw(self, void *dst, uint64_t size):
        cdef uint8_t *data = self._inc_ptr(size)
        cdef uint64_t i

        for i in range(size):
            (<uint8_t*>(dst))[i] = data[i]

    cdef assert_bytes_available(self, int64_t cnt):
        """
        Raises exception when less than `cnt` bytes are available
        """

        if (self._buf_end - self._buf_ptr) < cnt:
            raise Exception("out-of-bound read")

    cdef uint8_t* _inc_ptr(self, int64_t inc_by) except? NULL:
        """
        Get pointer to the buffer at current position with post-increment.
        Raises exception if less than `inc_by` bytes are available.
        """

        cdef uint8_t *ptr = self._buf_ptr

        if (self._buf_end - self._buf_ptr) < inc_by:
            raise Exception("out-of-bound read")

        self._buf_ptr += inc_by

        return ptr;


@cython.final
cdef class BinaryWriter:
    cdef bytearray _buf         # underlying bytearray object
    cdef Py_ssize_t _buf_size   # num of bytes containing valid data
    cdef Py_ssize_t _buf_alloc  # num of pre-allocated bytes
    cdef uint8_t *_buf_begin    # pointer to the beginning of bytearray

    def __cinit__(self, buf):
        self._buf = buf
        self._buf_size = PyByteArray_Size(buf)
        self._buf_alloc = self._buf_size
        self._buf_begin = <uint8_t*>PyByteArray_AsString(buf)

    cdef finalize(self):
        if (PyByteArray_Resize(self._buf, self._buf_size) < 0):
                raise Exception("failed to resize output bytearray")

    cdef write_raw(self, void *src, Py_ssize_t size):
        if src == NULL:
            raise Exception("trying to write data from null pointer")

        memcpy(self._inc_ptr(size), src, size)

    cdef write_int(self, uint64_t n, Py_ssize_t size):
        cdef uint8_t *dst = self._inc_ptr(size)
        cdef uint8_t i

        for i in range(size):
            dst[i] = (n & 0xff)
            n >>= 8

    cdef uint8_t* _inc_ptr(self, Py_ssize_t inc_by) except? NULL:
        """
        Append `inc_by` number of bytes to the buffer and returns pointer
        to the beginning of this newly appended region to write into.
        """

        cdef Py_ssize_t new_alloc

        if (self._buf_alloc - self._buf_size) < inc_by:
            new_alloc = max(2 * self._buf_alloc, self._buf_size + inc_by)

            if (PyByteArray_Resize(self._buf, new_alloc) < 0):
                raise Exception("failed to resize output bytearray")

            self._buf_begin = <uint8_t*>PyByteArray_AsString(self._buf)
            self._buf_alloc = new_alloc

        cdef uint8_t *ptr = self._buf_begin + self._buf_size

        self._buf_size += inc_by

        return ptr


################################################################################
# Python 2 and 3 compatibility
################################################################################


@cython.final
cdef class UtfEncoder:
    cdef _value
    cdef bytes _encoded

    cdef char* data
    cdef Py_ssize_t size

    cdef encode(self, value):
        cdef Py_ssize_t i

        if PY_MAJOR_VERSION >= 3:
            self.data = <char*>PyUnicode_AsUTF8AndSize(value, &self.size)
        else:
            if type(value) is unicode:
                self._encoded = (<unicode>(value)).encode("utf8")
                self.data = <char*>(self._encoded)
                self.size = len(self._encoded)
            else:
                self._encoded = value
                self.data = <char*>(self._encoded)
                self.size = len(self._encoded)

                # check that raw str contains only ascii characters
                for i in range(len(self._encoded)):
                    if self.data[i] >= 0x80:
                        raise Exception(
                            "non ascii character (0x{:02}) at pos {}".format(
                                self.data[i], i))
