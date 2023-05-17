from functools import wraps
from types import SimpleNamespace
from pGerrit.utils import urljoin, urlformat
import json
from typing import Callable

class GerritRest(object):
    """
    docstring for RestAPI
    """
    def get(raw=False) -> Callable:
        def dec_get(func):
            @wraps(func)
            def decorator_get(self, headers={"Accept":"application/json"}, *args, **kwargs):
                if raw:
                    headers = None
                url = func(self, headers=headers, *args, **kwargs)
                url = url if self.session.auth else url.replace("/a/", "/")
                res = self.session.get(url, headers=headers, verify=self.kwargs["verify"], params=kwargs)
                res._content = res._content.replace(b")]}'\n", b"")
                res.raise_for_status()

                if raw:
                    return res
                elif res.content == b'':
                    return res.content
                else:
                    return res.json(object_hook=lambda d: SimpleNamespace(**d))
            return decorator_get
        return dec_get

    def put(func) -> Callable:
        @wraps(func)
        def decorator_put(self, payload=None, headers={"content-type":"application/json"}, *args, **kwargs):
            url = func(self, payload, headers=headers, *args, **kwargs)
            url = url if self.session.auth else url.replace("/a/", "/")
            res = self.session.put(url, payload, headers=headers, verify=self.kwargs["verify"], params=kwargs)
            res.raise_for_status()
            # res._content = res._content.replace(b")]}'\n", b"")
            # des.resultType
            return res
        return decorator_put

    def post(func) -> Callable:
        @wraps(func)
        def decorator_post(self, payload=None, headers={"content-type":"application/json"}, *args, **kwargs):
            url = func(self, payload, headers=headers, *args, **kwargs)
            url = url if self.session.auth else url.replace("/a/", "/")
            res = self.session.post(url, json.dumps(payload), headers=headers, verify=self.kwargs["verify"], params=kwargs)
            res.raise_for_status()         
            # res._content = res._content.replace(b")]}'\n", b"")
            # des.resultType
            return res
        return decorator_post

    def delete(func) -> Callable:
        @wraps(func)
        def decorator_delete(self, headers={"Accept":"application/json"}, *args, **kwargs):
            url = func(self, headers=headers, *args, **kwargs)
            url = url if self.session.auth else url.replace("/a/", "/")
            res = self.session.delete(url, headers=headers, verify=self.kwargs["verify"], params=kwargs)
            res.raise_for_status()
            # res._content = res._content.replace(b")]}'\n", b"")
            # des.resultType
            return res
        return decorator_delete

    def url_wrapper(end=None) -> Callable:
        def wrapper(func):
            @wraps(func)
            def decorator_url(self, *args, **kwargs):
                from pGerrit.change import GerritChange, GerritChangeRevision, GerritChangeRevisionFile, GerritChangeEdit, GerritChangeReviewer
                from pGerrit.project import GerritProject
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

