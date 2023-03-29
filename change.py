from restAPIwrapper import GerritRest
from client import GerritClient
from utils import urljoin

class GerritChange(GerritClient):
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

    def __init__(self, host, gerritID, auth=None, verify=True, adapter=None):
        """See class docstring."""
        super().__init__(host, auth=auth, verify=verify, adapter=adapter)
        self.id = gerritID
        self._endpoint = "/a/changes/{}".format(self.id)
        self.url = urljoin(self.host, self._endpoint)

    @GerritRest.get
    def query(self, *args, **kwargs):
        return urljoin(self.host, "/a/changes/")

    @GerritRest.get
    def detail(self, *args, **kwargs):
        return urljoin(self.url, "/detail/")

    @GerritRest.get
    def info(self, *args, **kwargs):
        return urljoin(self.url)

    def is_merge(self):
        info = self.info(o=["ALL_COMMITS", "CURRENT_REVISION"])
        if len(info.revisions.__getattribute__(info.current_revision).commit.parents) == 2:
            return True
        else:
            return False

    def revision(self, revisionID):
        return GerritChangeRevision(self.host, self.id, revisionID, **self.kwargs)

    def current_revision(self):
        return GerritChangeRevision(self.host, self.id, "current", **self.kwargs)

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

    def __init__(self, host, gerritID, revisionID, auth=None, verify=True, adapter=None):
        """See class docstring."""
        super().__init__(host, gerritID, auth=auth, verify=verify, adapter=adapter)
        self.revisionID = revisionID
        self._endpoint = "/a/changes/{}/revisions/{}".format(self.id, self.revisionID)
        self.url = urljoin(self.host, self._endpoint)

    @GerritRest.get
    def files(self, *args, **kwargs):
        return urljoin(self.url, "/files/")

    def file(self, fileID):
        return GerritChangeRevisionFile(self.host, self.id, self.revisionID, fileID, **self.kwargs)

class GerritChangeRevisionFile(GerritChangeRevision):
    """docstring for GerritChangeRevisionFile"""
    def __init__(self, host, gerritID, revisionID, fileID, auth=None, verify=True, adapter=None):
        super(GerritChangeRevisionFile, self).__init__(host, gerritID, revisionID, auth=auth, verify=verify, adapter=adapter)
        self.fileID = fileID
        self._endpoint = "/a/changes/{}/revisions/{}/files/{}".format(self.id, self.revisionID, self.fileID)
        self.url = urljoin(self.host, self._endpoint)

    @GerritRest.get
    def content(self, *args, **kwargs):
        return urljoin(self.url, "/content/")
        