import requests
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
import requests_cache

class GerritClient(object):
    """
    A class representing a Gerrit REST API client.

    :param str host: The full URL to the server, including the `http(s)://` prefix.
    :param auth: (optional) Authentication handler. Must be derived from `requests.auth.HTTPDigestAuth`.
    :type auth: requests.auth.HTTPDigestAuth or None
    :param cookies: (optional) Cookie jar to be used in the session.
    :type cookies: requests.cookies.RequestsCookieJar or dict
    :param bool verify: (optional) Set to False to disable verification of SSL certificates.
    :param adapter: (optional) Custom connection adapter. Normally we use it to set `urllib3.util.Rety` object.
                    By default, there is 5 times retry behaviour.
    :type adapter: requests.adapters.BaseAdapter or None
    :param bool cache: (optional) Set to True to enable cache support. Defaults to True.
    :param int cache_expire: (optional) The number of seconds to expire the cache after. Defaults to 3.

    :return: An instance of GerritClient.
    :rtype: pGerrit.GerritClient
    """

    def __init__(self, host, auth=None, verify=True, adapter=None, cache=True, cache_expire=3):
        """See class docstring."""
        self.host = host
        if cache:
            self.session = requests_cache.CachedSession(expire_after=cache_expire)
        else:
            self.session = requests.session()

        if host.startswith('http://'):
            raise RuntimeError("Http protocol is not supported by latest Gerrit anymore. Use Https instead")
        
        self.verify = verify
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
        self.adapter = adapter
        self.cache = cache
        self.cache_expire = cache_expire

        if auth:
            self.session.auth = auth

        self.args = [host]
        self.kwargs = {"auth": auth, "verify": verify, "adapter":adapter, "cache":cache, "cache_expire":cache_expire}

        if not self.host.endswith("/"):
            self.host += "/"

    def __del__(self):
        self.session.close()

    @property
    def change(self):
        """Provides an instance of GerritChange for the given Gerrit client configuration.

        :param str id: the Change-id of Gerrit

        :return: An instance of GerritChangeQueryDescriptor.
        :rtype: pGerrit.queryDescriptor.GerritChangeQueryDescriptor

        Usage::

            gerrit_client = GerritClient(...)
            changes = gerrit_client.change.query(...)
            change = gerrit_client.change(12345).detail()
        """
        from pGerrit.queryDescriptor import GerritChangeQueryDescriptor
        return GerritChangeQueryDescriptor(self)

    @property
    def access(self):
        """Provides an instance of GerritAccess for the given Gerrit client configuration.

        :return: An instance of GerritAccessQueryDescriptor.
        :rtype: pGerrit.queryDescriptor.GerritAccessQueryDescriptor

        Usage::

            gerrit_client = GerritClient(...)
            access = gerrit_client.access.query(...)
        """
        from pGerrit.queryDescriptor import GerritAccessQueryDescriptor
        return GerritAccessQueryDescriptor(self)

    @property
    def project(self):
        """Provides an instance of GerritProject for the given Gerrit client configuration.

        :return: An instance of GerritProjectQueryDescriptor.
        :rtype: pGerrit.queryDescriptor.GerritProjectQueryDescriptor

        Usage::

            gerrit_client = GerritClient(...)
            projects = gerrit_client.project.query(...)
            project = gerrit_client.project("test")
        """
        from pGerrit.queryDescriptor import GerritProjectQueryDescriptor
        return GerritProjectQueryDescriptor(self)
