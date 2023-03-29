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
    _endpoint = "/a/changes/{}"

    def __init__(self, host, gerritID, auth=None, verify=True, adapter=None):
        """See class docstring."""
        super().__init__(host, auth=auth, verify=verify, adapter=adapter)
        self.id = gerritID

    @GerritRest.get
    def query(self, *args, **kwargs):
        return urljoin(self.host, "/a/changes/")

    @GerritRest.get
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

    @GerritRest.get
    def detail(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChange._endpoint, self.id), "/detail")

    @GerritRest.get
    def topic(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChange._endpoint, self.id), "/topic")

    @GerritRest.get
    def submitted_together(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChange._endpoint, self.id), "/submitted_together")

    @GerritRest.get
    def _in(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChange._endpoint, self.id), "/in")

    @GerritRest.get
    def comments(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChange._endpoint, self.id), "/comments")

    @GerritRest.get
    def drafts(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChange._endpoint, self.id), "/drafts")

    @GerritRest.get
    def check(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChange._endpoint, self.id), "/check")

    @GerritRest.get
    def edit(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChange._endpoint, self.id), "/edit")

    @GerritRest.get
    def reviewers(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChange._endpoint, self.id), "/reviewers")

    @GerritRest.get
    def suggest_reviewers(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChange._endpoint, self.id), "/suggest_reviewers")

    @GerritRest.post
    def edit_publish(self, payload=None, headers=None):
        return urljoin(self.host, urlformat(GerritChange._endpoint, self.id), "/edit:publish")

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
    _endpoint ="/a/changes/{}/revisions/{}"

    def __init__(self, host, gerritID, revisionID, auth=None, verify=True, adapter=None):
        """See class docstring."""
        super().__init__(host, gerritID, auth=auth, verify=verify, adapter=adapter)
        self.revisionID = revisionID

    @GerritRest.get
    def commit(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChangeRevision._endpoint, self.id, self.revisionID), "/commit")

    @GerritRest.get
    def actions(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChangeRevision._endpoint, self.id, self.revisionID), "/actions")

    @GerritRest.get
    def review(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChangeRevision._endpoint, self.id, self.revisionID), "/review")

    @GerritRest.get
    def related(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChangeRevision._endpoint, self.id, self.revisionID), "/related")

    @GerritRest.get
    def patch(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChangeRevision._endpoint, self.id, self.revisionID), "/patch")

    @GerritRest.get
    def mergeable(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChangeRevision._endpoint, self.id, self.revisionID), "/mergeable")

    @GerritRest.get
    def submit_type(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChangeRevision._endpoint, self.id, self.revisionID), "/submit_type")

    @GerritRest.get
    def drafts(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChangeRevision._endpoint, self.id, self.revisionID), "/drafts")

    @GerritRest.get
    def comments(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChangeRevision._endpoint, self.id, self.revisionID), "/comments")

    @GerritRest.get
    def files(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChangeRevision._endpoint, self.id, self.revisionID), "/files")

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
    _endpoint = "/a/changes/{}/revisions/{}/files/{}"

    def __init__(self, host, gerritID, revisionID, fileID, auth=None, verify=True, adapter=None):
        super(GerritChangeRevisionFile, self).__init__(host, gerritID, revisionID, auth=auth, verify=verify, adapter=adapter)
        self.fileID = fileID

    @GerritRest.get
    def content(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChangeRevisionFile._endpoint, self.id, self.revisionID, self.fileID), "/content")

    @GerritRest.get
    def diff(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChangeRevisionFile._endpoint, self.id, self.revisionID, self.fileID), "/diff")

    @GerritRest.get
    def download(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChangeRevisionFile._endpoint, self.id, self.revisionID, self.fileID), "/download")

    @GerritRest.get
    def blame(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritChangeRevisionFile._endpoint, self.id, self.revisionID, self.fileID), "/blame")

    def is_binary(self):
        file_info = getattr(self.files(), self.fileID)
        if hasattr(file_info, "binary") and file_info.binary == True:
            return True
        else:
            return False

    @GerritRest.put
    def edit(self, payload, headers=None):
        return urljoin(self.host, "/a/changes/", self.id, "/edit/", self.fileID)
