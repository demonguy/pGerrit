import requests
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
import requests_cache

requests_cache.install_cache(expire_after=900, include_get_headers=True)

class GerritClient(object):
    """Interface to the Gerrit REST API.
    :arg str url: The full URL to the server, including the `http(s)://`
        prefix. If `auth` is given, `url` will be automatically adjusted to
        include Gerrit's authentication suffix.
    :arg auth: (optional) Authentication handler.  Must be derived from
        `requests.auth.AuthBase`.
    :arg boolean verify: (optional) Set to False to disable verification of
        SSL certificates.
    :arg requests.adapters.BaseAdapter adapter: (optional) Custom connection
        adapter. See
        https://requests.readthedocs.io/en/master/api/#requests.adapters.BaseAdapter
    """

    def __init__(self, host, auth=None, verify=True, adapter=None):
        """See class docstring."""
        self.host = host
        self.session = requests.session()
        if not adapter:
            retry = Retry(
                total=5,
                read=5,
                connect=5,
                backoff_factor=0.3,
                status_forcelist=(500, 502, 504),
            )
            adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.auth = auth

        self.kwargs = {"auth": auth, "verify": verify, "adapter":adapter}

        if not self.host.endswith("/"):
            self.host += "/"

    def __del__(self):
        self.session.close()

    def change(self, gerritID):
        from pGerrit.change import GerritChange
        return GerritChange(self.host, gerritID, **self.kwargs)

    def access(self):
        from pGerrit.Access import GerritAccess
        return GerritAccess(self.host, **self.kwargs)