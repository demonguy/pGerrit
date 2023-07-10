# This file is to implement query classmethod from GerritClient withous passing host arguement
# In oder to make IDE autocomple work , we need to return exact type from __call__ method
from pGerrit.change import GerritChange, GerritChangeEdit, GerritChangeReviewer
from pGerrit.Access import GerritAccess
from pGerrit.project import GerritProject

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

    def create(self, payload=None, *args, **kwargs):
        return GerritChange.create.__func__(self.factory_obj, payload=payload, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        '''
        :return: An instance of GerritChange.
        :rtype: pGerrit.change.GerritChange
        '''
        return GerritChange(*self.factory_obj.args, *args,  **self.factory_obj.kwargs, **kwargs)

class GerritChangeEditQueryDescriptor(QueryDescriptor):
    def __init__(self, factory_obj):
        super().__init__(factory_obj)

    def info(self, *args, **kwargs):
        return GerritChangeEdit.info.__func__(self.factory_obj, *args, **kwargs)

    def edit_publish(self, payload=None, headers=None):
        return GerritChangeEdit.edit_publish.__func__(self.factory_obj, payload=payload, headers=headers)

    def edit_restore(self, payload=None, headers=None):
        return GerritChangeEdit.edit_restore.__func__(self.factory_obj, payload=payload, headers=headers)

    def edit_delete(self, headers=None):
        return GerritChangeEdit.edit_delete.__func__(self.factory_obj, headers=headers)

    def __call__(self, *args, **kwargs):
        '''
        :return: An instance of GerritChangeEdit.
        :rtype: pGerrit.change.GerritChangeEdit
        '''
        return GerritChangeEdit(*self.factory_obj.args, *args, **self.factory_obj.kwargs, **kwargs)

class GerritChangeReviewerQueryDescriptor(QueryDescriptor):
    def __init__(self, factory_obj):
        super().__init__(factory_obj)

    def query(self, *args, **kwargs):
        return GerritChangeReviewer.query.__func__(self.factory_obj, *args, **kwargs)

    def suggest_reviewers(self, *args, **kwargs):
        return GerritChangeReviewer.suggest_reviewers.__func__(self.factory_obj, *args, **kwargs)

    def add_reviewer(self, *args, **kwargs):
        return GerritChangeReviewer.add_reviewer.__func__(self.factory_obj, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        '''
        :return: An instance of GerritChangeReviewer.
        :rtype: pGerrit.change.GerritChangeReviewer
        '''
        return GerritChangeReviewer(*self.factory_obj.args, *args, **self.factory_obj.kwargs, **kwargs)

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
    
class GerritProjectQueryDescriptor(QueryDescriptor):
    def __init__(self, factory_obj):
        super().__init__(factory_obj)

    def query(self, *args, **kwargs):
        return GerritProject.query.__func__(self.factory_obj, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        '''
        :return: An instance of GerritProject.
        :rtype: pGerrit.project.GerritProject
        '''
        return GerritProject(*self.factory_obj.args, *args, **self.factory_obj.kwargs, **kwargs)