from pGerrit.restAPIwrapper import GerritRest
from pGerrit.client import GerritClient
from pGerrit.utils import urljoin, urlformat
from pGerrit.queryMeta import QueryMeta

class GerritAccess(GerritClient, metaclass=QueryMeta):
    """Class maps /access/ endpoint of Gerrit REST API

    :return: An instance of GerritAccess.
    :rtype: pGerrit.GerritAccess

    You won't need to instantiate this Class directly.
    Use ``pGerrit.GerritClient.access``
    """
    _endpoint = "/a/access/{}"

    def __init__(self, host, auth=None, verify=True, adapter=None):
        """See class docstring."""
        super().__init__(host, auth=auth, verify=verify, adapter=adapter)

    @GerritRest.get()
    def query(self, *args, **kwargs):
        """Performs a GET request to query for access rights from the Gerrit API.

        **API URL**: `/a/access/ <https://gerrit-review.googlesource.com/Documentation/rest-api-access.html#list-access>`__

        **Input type**: `QueryOptions <https://gerrit-review.googlesource.com/Documentation/rest-api-access.html#list-access>`__

        **Return type**: Dict[`str`, `ProjectAccessInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-access.html#project-access-info>`__]

        Usage::

            access_rights = gerrit_access.query(**{"project": "All-Projects"})

        """
        return urljoin(self.host, urlformat(GerritAccess._endpoint, ""))
