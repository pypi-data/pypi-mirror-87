from itertools import chain
import uuid
from operator import __all__ as all_op
from operator import *

import weakref

_inplace = (iadd, iand, iconcat, ifloordiv, ilshift, imod, imul,
            imatmul, ior, ipow, irshift, isub, itruediv, ixor)
_python_types = (float, int, list, dict, str)

imported_operators = locals()

__doc__ = """YAP - Yet another Proxy. Provides a complete proxy solution without using sometimes unsafe (and thus restricted) methods like exec. 

YAP is composed of 2 components the registery that holds all proxied items and the proxy implementation. 
"""

class _ProxyRegistery(object):
    """This Registery allows for configuration on how the proxy functions with regards to the proxied value. The registery also provides inflection points to allow for events in the future. """
    
    def __init__(self):
        self._proxied = {}

    def _default_config(self):
        return dict(load_once=False,
                    unpack=True
                    )

    def unpack(self, proxy, *a, **kw):
        key = self.key(proxy)
        proxied, cfg = self._proxied[key]
        unpacked = proxied(*a, **kw)
        if cfg["load_once"]:
            cfg["unpack"] = False
            self._proxied[key] = unpacked, cfg
        return unpacked

    def key(self, proxy):
        return id(proxy)

    def proxy(self, proxy, proxied, config=None, **kw):
        key = self.key(proxy)
        proxy_config = self._default_config()
        proxy_config.update(**kw)
        proxy_config.update(config or {})
        self._proxied[key] = (proxied, proxy_config)

    def get(self, proxy):
        key = self.key(proxy)
        proxied, cfg = self._proxied[key]
        if cfg["unpack"]:
            return self.unpack(proxy)
        return self._proxied[key][0]


proxy_cache = _ProxyRegistery()


def proxied_call(proxy, fn, *a, **kw):
    subject = proxy_cache.get(proxy)
    subject_loc = id(subject)
    if isinstance(fn, str):
        fn = getattr(subject, fn)
        outcome = fn(*a, **kw)
    else:
        outcome = fn(subject, *a, *kw)
    o_id = id(outcome)
    l_id = id(subject)
    if fn in _inplace:
        proxy_cache.proxy(proxy, outcome, unpack=False)
        return proxy
    return outcome


class BasicProxy(object):

    def __repr__(self):
        subject = proxy_cache.get(self)
        return subject.__repr__()

    def __len__(self):
        subject = proxy_cache.get(self)
        return len(subject)

    def __bool__(self):
        subject = proxy_cache.get(self)
        return bool(subject)

    def __setattr__(self, attr, val):
        subject = proxy_cache.get(self)
        setattr(subject, attr, val)

    def __delattr__(self, attr):
        subject = proxy_cache.get(self)
        delattr(subject, attr)

    def __getattribute__(self, attr):
        subject = proxy_cache.get(self)
        if attr == "__subject__":
            return subject
        try:
            return getattr(subject, attr)
        except AttributeError:
            if attr == '__conform__' and type(subject) in _python_types:
                # Conform is an ooddball rejected, but used, way of converting a value
                # Problem is builtins probably don't support it since it was a rejected
                # PEP but the caller may find our Proxy and as it to conform.
                return lambda *a: subject
            raise


def generate_method(name_or_fn):
    fn = None
    if callable(name_or_fn):
        fn = name_or_fn
    if fn is None:
        fn = imported_operators.get(op)
    if fn is None:
        fn = f"__{op.replace('_','')}__"
    return lambda s, *a, **kw: proxied_call(s, fn, *a, **kw)


methods = {}
for op in all_op:
    meth_name = f'__{op.replace("_","")}__'
    if meth_name not in methods:
        methods[meth_name] = generate_method(op)

for op in set(dir(object)) | set(dir(int)):
    if op[0:2] == "__":
        meth_name = f'__{op.replace("_","")}__'
        if meth_name not in methods:
            methods[meth_name] = generate_method(meth_name)

for op in [len, ]:
    methods[f"__{op.__name__}__"] = lambda s, * \
        a, **kw: proxied_call(s, op, *a, **kw)

del methods["__new__"]
del methods["__init__"]
del methods["__getattribute__"]
ComplexProxyMixin = type('ComplexProxy', (object, ), methods)
Proxy = type('Proxy', (BasicProxy, ComplexProxyMixin), {})


def proxy(proxied, config=None, **kw):
    """Proxying can be confusing largely in part that there are lots of edgecases and how you want your proxy to work might vary. In and effort to offer as much configs can be passed into to customize behavior in edge cases. Configs """
    prx = Proxy()
    proxy_cache.proxy(prx, proxied, **kw)
    return prx


def CallbackProxy(cb):
    return proxy(cb, load_once=False)


def LazyProxy(cb):
    return proxy(cb, load_once=True)

