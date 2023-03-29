from pGerrit.restAPIwrapper import GerritRest
from pGerrit.client import GerritClient
from pGerrit.utils import urljoin, urlformat
from pGerrit.queryMeta import QueryMeta

class GerritChange(GerritClient, metaclass=QueryMeta):
    """Interface to the Gerrit REST API.
    :arg str url: The full URL to the server, including the `http(s)://`
        prefix.
    :arg auth: (optional) Authentication handler.  Must be derived from
        `requests.auth.HTTPDigestAuth`.
    :arg boolean verify: (optional) Set to False to disable verification of
        SSL certificates.
    :arg requests.adapters.BaseAdapter adapter: (optional) Custom connection
        adapter. See
        https://requests.readthedocs.io/en/master/api/#requests.adapters.BaseAdapter
    """
    _endpoint = "/a/changes/{}"
    _args = ["id"]

    def __init__(self, host, gerritID=None, auth=None, verify=True, adapter=None):
        """See class docstring."""
        super().__init__(host, auth=auth, verify=verify, adapter=adapter)
        self.id = gerritID

    @GerritRest.get()
    def query(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChange._endpoint, ""))

    @GerritRest.get()
    def info(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChange._endpoint, self.id))

    def revision(self, revisionID):
        return GerritChangeRevision(self.host, self.id, revisionID, **self.kwargs)

    def current_revision(self):
        return GerritChangeRevision(self.host, self.id, "current", **self.kwargs)

    def is_merge(self):
        revision = self.current_revision()
        if len(revision.commit().parents) == 2:
            return True
        else:
            return False

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def detail(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def topic(self, *args, **kwargs):
        pass

    @GerritRest.put
    @GerritRest.url_wrapper("topic")
    def set_topic(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def submitted_together(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper("in")
    def _in(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def comments(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def robotcomments(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def drafts(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def check(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def edit(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def reviewers(self, *args, **kwargs):
        pass

    @GerritRest.post
    @GerritRest.url_wrapper("reviewers")
    def add_reviewer(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def suggest_reviewers(self, *args, **kwargs):
        pass

    @GerritRest.post
    @GerritRest.url_wrapper()
    def rebase(self, payload=None, headers=None):
        pass

    @GerritRest.post
    @GerritRest.url_wrapper("edit:publish")
    def edit_publish(self, payload=None, headers=None):
        pass

    @GerritRest.post
    @GerritRest.url_wrapper("edit")
    def edit_restore(self, payload=None, headers=None):
        pass

    @GerritRest.delete
    @GerritRest.url_wrapper("edit")
    def edit_delete(self, payload=None, headers=None):
        pass

    @GerritRest.delete
    @GerritRest.url_wrapper("")
    def delete_change(self, payload=None, headers=None):
        pass

class GerritChangeRevision(GerritChange):
    """Interface to the Gerrit REST API.
    :arg str url: The full URL to the server, including the `http(s)://`
        prefix. If `auth` is given, `url` will be automatically adjusted to
        include Gerrit's authentication suffix.
    :arg auth: (optional) Authentication handler.  Must be derived from
        `requests.auth.HTTPDigestAuth`.
    :arg boolean verify: (optional) Set to False to disable verification of
        SSL certificates.
    :arg requests.adapters.BaseAdapter adapter: (optional) Custom connection
        adapter. See
        https://requests.readthedocs.io/en/master/api/#requests.adapters.BaseAdapter
    """
    _endpoint = "/a/changes/{}/revisions/{}"
    _args = ["id", "revisionID"]

    def __init__(self, host, gerritID, revisionID, auth=None, verify=True, adapter=None):
        """See class docstring."""
        super().__init__(host, gerritID, auth=auth, verify=verify, adapter=adapter)
        self.revisionID = revisionID

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def commit(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def actions(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def review(self, *args, **kwargs):
        pass

    @GerritRest.post
    @GerritRest.url_wrapper("review")
    def set_review(self, payload=None, headers=None):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def related(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def patch(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def mergeable(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def submit_type(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def drafts(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def comments(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def files(self, *args, **kwargs):
        pass

    @GerritRest.post
    @GerritRest.url_wrapper()
    def cherrypick(self, payload=None, headers=None):
        pass

    def file(self, fileID):
        return GerritChangeRevisionFile(self.host, self.id, self.revisionID, fileID, **self.kwargs)

    def reviwer(self, accountID):
        return GerritChangeRevisionReviewer(self.host, self.id, self.revisionID, accountID, **self.kwargs)

class GerritChangeRevisionReviewer(GerritChangeRevision):
    """Interface to the Gerrit REST API.
    :arg str url: The full URL to the server, including the `http(s)://`
        prefix. If `auth` is given, `url` will be automatically adjusted to
        include Gerrit's authentication suffix.
    :arg auth: (optional) Authentication handler.  Must be derived from
        `requests.auth.HTTPDigestAuth`.
    :arg boolean verify: (optional) Set to False to disable verification of
        SSL certificates.
    :arg requests.adapters.BaseAdapter adapter: (optional) Custom connection
        adapter. See
        https://requests.readthedocs.io/en/master/api/#requests.adapters.BaseAdapter
    """
    _endpoint = "/a/changes/{}/revisions/{}/reviewers/{}"
    _args = ["id", "accountID", "revisionID", "accountID"]

    def __init__(self, host, gerritID, revisionID, accountID, auth=None, verify=True, adapter=None):
        """See class docstring."""
        super().__init__(host, gerritID, revisionID, auth=auth, verify=verify, adapter=adapter)
        self.accountID = accountID

    @GerritRest.get()
    def list(self, *args, **kwargs):
        return urljoin(self.host, urlformat(self._endpoint, self.id, self.revisionID, ""))

    @GerritRest.delete
    def delete_vote(self, label, *args, **kwargs):
        return urljoin(self.host, urlformat(self._endpoint, self.id, self.revisionID, self.accountID), "votes", label)


class GerritChangeRevisionFile(GerritChangeRevision):
    """docstring for GerritChangeRevisionFile"""
    _endpoint = "/a/changes/{}/revisions/{}/files/{}"
    _args = ["id", "revisionID", "fileID"]

    def __init__(self, host, gerritID, revisionID, fileID, auth=None, verify=True, adapter=None):
        super(GerritChangeRevisionFile, self).__init__(host, gerritID, revisionID, auth=auth, verify=verify, adapter=adapter)
        self.fileID = fileID

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def content(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def diff(self, *args, **kwargs):
        pass

    @GerritRest.get(raw=True)
    @GerritRest.url_wrapper()
    def download(self, *args, **kwargs):
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def blame(self, *args, **kwargs):
        pass

    def is_binary(self):
        file_info = getattr(self.files(), self.fileID)
        if hasattr(file_info, "binary") and file_info.binary == True:
            return True
        else:
            return False

    @GerritRest.get()
    def get_history_log(self, commit=None, *args, **kwargs):
        project = self.info().project
        commit = commit or self.commit().commit
        return urljoin(self.host, "a/plugins", "gitiles", project, "+log", commit, self.fileID)

    @GerritRest.put
    def edit(self, payload, headers=None):
        return urljoin(self.host, "/a/changes/", self.id, "/edit/", urlformat("{}", self.fileID))

    @GerritRest.get()
    def edit_retrieve(self, headers=None):
        return urljoin(self.host, "/a/changes/", self.id, "/edit/", urlformat("{}", self.fileID))

