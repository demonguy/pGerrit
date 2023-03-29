from functools import wraps
import requests
from types import SimpleNamespace
from pGerrit.utils import urljoin, urlformat
from pGerrit.exception import GerritError
import json


class GerritRest(object):
    """
    docstring for RestAPI
    """
    def get(raw=False):
        def dec_get(func):
            @wraps(func)
            def decorator_get(self, headers={"Accept":"application/json"}, *args, **kwargs):
                if raw:
                    headers = None
                url = func(self, headers=headers, *args, **kwargs)
                url = url if self.session.auth else url.replace("/a/", "/")
                res = self.session.get(url, headers=headers, verify=self.kwargs["verify"], params=kwargs)
                res._content = res._content.replace(b")]}'\n", b"")
                if res.status_code != 200:
                    raise GerritError(res.status_code, res.content)

                if raw:
                    return res
                else:
                    return res.json(object_hook=lambda d: SimpleNamespace(**d))
            return decorator_get
        return dec_get

    def put(func):
        @wraps(func)
        def decorator_put(self, payload=None, headers={"content-type":"application/json"}, *args, **kwargs):
            url = func(self, payload, headers=headers, *args, **kwargs)
            url = url if self.session.auth else url.replace("/a/", "/")
            res = self.session.put(url, payload, headers=headers, verify=self.kwargs["verify"], params=kwargs)
            # res._content = res._content.replace(b")]}'\n", b"")
            # des.resultType
            return res
        return decorator_put

    def post(func):
        @wraps(func)
        def decorator_post(self, payload=None, headers={"content-type":"application/json"}, *args, **kwargs):
            url = func(self, payload, headers=headers, *args, **kwargs)
            url = url if self.session.auth else url.replace("/a/", "/")
            res = self.session.post(url, json.dumps(payload), headers=headers, verify=self.kwargs["verify"], params=kwargs)
            # res._content = res._content.replace(b")]}'\n", b"")
            # des.resultType
            return res
        return decorator_post

    def delete(func):
        @wraps(func)
        def decorator_delete(self, headers={"Accept":"application/json"}, *args, **kwargs):
            url = func(self, headers=headers, *args, **kwargs)
            url = url if self.session.auth else url.replace("/a/", "/")
            res = self.session.delete(url, headers=headers, verify=self.kwargs["verify"], params=kwargs)
            # res._content = res._content.replace(b")]}'\n", b"")
            # des.resultType
            return res
        return decorator_delete

    def url_wrapper(end=None):
        def wrapper(func):
            @wraps(func)
            def decorator_url(self, *args, **kwargs):
                from pGerrit.change import GerritChange, GerritChangeRevision, GerritChangeRevisionFile
                name = end if end != None else func.__name__
                # find the class defined the method
                cls_d = eval(func.__qualname__.split(".")[-2])
                # extend all arguments which need to be inserted into endpoint
                args = []
                for arg_name in cls_d._args:
                    args.append(getattr(self, arg_name))

                return urljoin(self.host, urlformat(cls_d._endpoint, *args), name)
            return decorator_url
        return wrapper

