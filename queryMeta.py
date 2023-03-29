#This file is for implementiing GerritClient.change.query and GerritClient.change(xxxxx).

from pGerrit.client import GerritClient

class QueryMeta(type):
    def __new__(cls, name, bases, attrs):
        if GerritClient in bases:
            attrs['__call__'] = meta_call
        return super().__new__(cls, name, bases, attrs)

def meta_call(self, *args, **kwargs):
    if len(args) == 0:
        return self
    else:
        return self.__class__(self.host, gerritID=args[0] if len(args) > 0 else kwargs["gerritID"], auth=self.session.auth, verify=self.verify, adapter=self.adapter)