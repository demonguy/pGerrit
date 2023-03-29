from functools import wraps
import requests
from types import SimpleNamespace
from Gerrit.utils import urljoin


class GerritRest(object):
    """
    docstring for RestAPI
    """
    def get(func):
        @wraps(func)
        def decorator_get(self, *args, **kwargs):
            url = func(self)
            self.session.headers["Accept"] = "application/json"
            res = self.session.get(url, verify=self.kwargs["verify"], params=kwargs)
            res._content = res._content.replace(b")]}'\n", b"")
            # des.resultType
            try:
                return res.json(object_hook=lambda d: SimpleNamespace(**d))
            except Exception as e:
                raise RuntimeError(e.__class__.__name__ + " raised, server response:" + str(res.content))
        return decorator_get

    def put(func):
        @wraps(func)
        def decorator_put(self, payload=None, headers=None, **kwargs):
            url = func(self, payload, headers=headers)
            res = self.session.put(url, payload, headers=headers, verify=self.kwargs["verify"], params=kwargs)
            # res._content = res._content.replace(b")]}'\n", b"")
            # des.resultType
            return res
        return decorator_put

    def post(func):
        @wraps(func)
        def decorator_post(self, payload=None, headers=None, **kwargs):
            url = func(self, payload, headers=headers)
            res = self.session.post(url, payload, headers=headers, verify=self.kwargs["verify"], params=kwargs)
            # res._content = res._content.replace(b")]}'\n", b"")
            # des.resultType
            return res
        return decorator_post
