from Gerrit.restAPIwrapper import GerritRest
from Gerrit.client import GerritClient
from Gerrit.utils import urljoin, urlformat

class GerritAccess(GerritClient):
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
    _endpoint = "/a/access/{}"

    def __init__(self, host, auth=None, verify=True, adapter=None):
        """See class docstring."""
        super().__init__(host, auth=auth, verify=verify, adapter=adapter)

    @GerritRest.get
    def query(self, *args, **kwargs):
        return urljoin(self.host, urlformat(GerritAccess._endpoint, ""))
