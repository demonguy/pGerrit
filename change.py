from Gerrit.restAPIwrapper import GerritRest
from Gerrit.client import GerritClient
from Gerrit.utils import urljoin, urlformat

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
        self._endpoint = urlformat("/a/changes/{}", self.id)
        self.url = urljoin(self.host, self._endpoint)

    @GerritRest.get
    def query(self, *args, **kwargs):
        return urljoin(self.host, "/a/changes/")

    @GerritRest.get
    def detail(self, *args, **kwargs):
        return urljoin(self.url, "/detail")

    @GerritRest.get
    def info(self, *args, **kwargs):
        return self.url

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
        self._endpoint = urlformat("/a/changes/{}/revisions/{}", self.id, self.revisionID)
        self.url = urljoin(self.host, self._endpoint)

    @GerritRest.get
    def files(self, *args, **kwargs):
        return urljoin(self.url, "/files")

    @GerritRest.get
    def commit(self, *args, **kwargs):
        return urljoin(self.url, "/commit")

    def file(self, fileID):
        return GerritChangeRevisionFile(self.host, self.id, self.revisionID, fileID, **self.kwargs)

    def getParentInfo(self):
        # assume there are only 1 or 2 parents
        current_info = self.query(q=self.commit().commit)[0]
        if len(self.commit().parents) == 1:
            parent = self.commit().parents[0]
            info = self.query(q=parent.commit)[0]
            return ({"id":info._number, "revision":parent.commit}, None)
        else:
            for parent in self.commit().parents:
                info = self.query(q=parent.commit)[0]
                if info.branch == current_info.branch:
                    local = {"id":info._number, "revision":parent.commit}
                else:
                    remote = {"id":info._number, "revision":parent.commit}
            return (local, remote)

class GerritChangeRevisionFile(GerritChangeRevision):
    """docstring for GerritChangeRevisionFile"""
    def __init__(self, host, gerritID, revisionID, fileID, auth=None, verify=True, adapter=None):
        super(GerritChangeRevisionFile, self).__init__(host, gerritID, revisionID, auth=auth, verify=verify, adapter=adapter)
        self.fileID = fileID
        self._endpoint = urlformat("/a/changes/{}/revisions/{}/files/{}", self.id, self.revisionID, self.fileID)
        self.url = urljoin(self.host, self._endpoint)

    @GerritRest.get
    def content(self, *args, **kwargs):
        return urljoin(self.url, "/content")

    @GerritRest.get
    def diff(self, *args, **kwargs):
        return urljoin(self.url, "/diff")

    def is_binary(self):
        diff = self.diff()
        if hasattr(diff, "binary") and diff.binary == True:
            return True
        else:
            return False

    @GerritRest.put
    def edit(self, payload, headers=None):
        return urljoin(self.host, "/a/changes/", self.id, "/edit/", self.fileID)
