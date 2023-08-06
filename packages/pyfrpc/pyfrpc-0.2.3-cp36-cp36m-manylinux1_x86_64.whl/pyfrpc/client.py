# -*- coding: utf-8 -*-

import requests

from functools import wraps
from six.moves import http_cookiejar, xmlrpc_client

from .models import FrpcCall, FrpcResponse, FrpcFault
from .coding import encode, decode


APPLICATION_FRPC = "application/x-frpc"


def cached_getter(func):
    key = "__cache_{:x}".format(id(func))

    @wraps(func)
    def new_func(self):
        if not hasattr(self, key):
            setattr(self, key, func(self))

        return getattr(self, key)

    return new_func


class BlockAllCookiePolicy(http_cookiejar.CookiePolicy):
    set_ok = return_ok = domain_return_ok =  path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = False
    hide_cookie2 = False


class FrpcClient(object):
    def __init__(self, url, session=None, version=0x0201, req_opts=None):
        self._url = url
        self._version = version

        if session:
            self.session = session
        else:
            self.session = requests.session()
            self.session.cookies.set_policy(BlockAllCookiePolicy())

        self._opts = req_opts or {}
        self._opts.setdefault('timeout', 60)

    def call(self, method, args=(), **kwargs):
        payload = encode(FrpcCall(name=method, args=args), self._version)

        headers = kwargs.pop('headers', {})
        headers.update({
            "Content-Type" : APPLICATION_FRPC,
            "Accept" : APPLICATION_FRPC,
        })

        for k,v in self._opts.items():
            kwargs.setdefault(k, v)

        res = self.session.request("POST", self._url, data=payload, headers=headers, **kwargs)
        content_type = res.headers.get("Content-Type", None)

        # FRPC decoding
        if content_type == APPLICATION_FRPC:
            payload = decode(res.content)

            if isinstance(payload, FrpcFault):
                raise payload

            return payload.data

        # XML-RPC decoding
        if content_type == "text/xml":
            try:
                payload, _ = xmlrpc_client.loads(
                    res.content, use_datetime=True, use_builtin_types=True)
                return payload[0]
            except XmlRpcFault as e:
                raise FrpcFault(e.faultCode, e.faultString)

        raise RuntimeError("bad content type: " + content_type)

    @cached_getter
    def methods(self):
        try:
            return self.call("system.listMethods")
        except:
            return []

    def help(self, method):
        return self.call("system.methodHelp", (method,))

    @property
    def rpc(self):
        return _FrpcClientAttr(self, "")


class _FrpcClientAttr(object):
    def __init__(self, client, method):
        self._client = client
        self._method = method

        self._prefix = self._method + ("." if self._method else "")

    def __getattr__(self, name):
        if name.startswith("__"):
            return super().__getattr__(name)

        method = self._prefix + name
        return _FrpcClientAttr(self._client, method)

    def __call__(self, *args, **kwargs):
        return self._client.call(self._method, args, **kwargs)

    @property
    @cached_getter
    def __doc__(self):
        try:
            return self._client.help(self._method)
        except Exception as e:
            return "Failed to get method documentation.\n\n{}".format(e)
        except:
            return "Failed to get method documentation."

    @cached_getter
    def __dir__(self):
        methods = self._client.methods()

        methods = [m for m in methods if m.startswith(self._prefix)]
        methods = [m[len(self._prefix):] for m in methods]
        methods = [m.split(".", 1)[0] for m in methods]
        methods = list(set(methods))

        return methods
