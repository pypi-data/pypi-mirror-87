# -*- coding: utf-8 -*-

import six


if six.PY3:
    from datetime import datetime, timezone, timedelta

    def unixtimestamp(dt):
        return dt.timestamp()

else:
    from datetime import datetime, timedelta
    from datetime import tzinfo

    class timezone(tzinfo):
        """Fixed offset in minutes east from UTC."""

        def __init__(self, delta):
            assert(isinstance(delta, timedelta))
            self.__offset = delta

        def utcoffset(self, dt):
            return self.__offset

        def tzname(self, dt):
            return None

        def dst(self, dt):
            return timedelta(0)

    timezone.utc = timezone(timedelta(0))

    _EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)

    def unixtimestamp(dt):
        return (dt - _EPOCH).total_seconds()
