# This file is to implement query classmethod from GerritClient withous passing host arguement
# In oder to make IDE autocomple work , we need to return exact type from __call__ method
from pGerrit.change import GerritChange
from pGerrit.Access import GerritAccess

class QueryDescriptor(object):
    def __init__(self, factory_obj):
        self.factory_obj = factory_obj

    def query(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        pass

class GerritChangeQueryDescriptor(QueryDescriptor):
    def __init__(self, factory_obj):
        super().__init__(factory_obj)

    def query(self, *args, **kwargs):
        return GerritChange.query.__func__(self.factory_obj, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        '''
        :return: An instance of GerritChange.
        :rtype: pGerrit.change.GerritChange
        '''
        return GerritChange(*self.factory_obj.args, *args,  **self.factory_obj.kwargs, **kwargs)

class GerritAccessQueryDescriptor(QueryDescriptor):
    def __init__(self, factory_obj):
        super().__init__(factory_obj)

    def query(self, *args, **kwargs):
        return GerritAccess.query.__func__(self.factory_obj, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        '''
        :return: An instance of GerritAccess.
        :rtype: pGerrit.Access.GerritAccess
        '''
        return GerritAccess(*self.factory_obj.args, *args, **self.factory_obj.kwargs, **kwargs)