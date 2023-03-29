from functools import wraps
import requests
from types import SimpleNamespace
from Gerrit.utils import urljoin, urlformat
import json


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
                raise RuntimeError(e.__class__.__name__ + " raised\nserver response:" + str(res.content) + "\nurl:" + url)
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
            headers = headers or self.session.headers
            headers["Content-Type"] = "application/json"
            res = self.session.post(url, json.dumps(payload), headers=headers, verify=self.kwargs["verify"], params=kwargs)
            # res._content = res._content.replace(b")]}'\n", b"")
            # des.resultType
            return res
        return decorator_post

    def url_wrapper(end=None):
        def wrapper(func):
            @wraps(func)
            def decorator_url(self, *args, **kwargs):
                from Gerrit.change import GerritChange, GerritChangeRevision, GerritChangeRevisionFile
                name = end or func.__name__
                # find the class defined the method
                cls_d = eval(func.__qualname__.split(".")[-2])
                # extend all arguments which need to be inserted into endpoint
                args = []
                for arg_name in cls_d._args:
                    args.append(getattr(self, arg_name))

                return urljoin(self.host, urlformat(cls_d._endpoint, *args), name)
            return decorator_url
        return wrapper

