from pGerrit.restAPIwrapper import GerritRest
from pGerrit.client import GerritClient
from pGerrit.utils import urljoin, urlformat

class GerritProject(GerritClient):
    """Class maps /projects/ endpoint of Gerrit REST API

    :return: An instance of GerritProject.
    :rtype: pGerrit.project.GerritProject

    You won't need to instantiate this Class directly.
    Use ``pGerrit.GerritClient.project``
    """
    _endpoint = "/a/projects/{}"
    _args = ["pj"]

    def __init__(self, host, project, auth=None, verify=True, adapter=None, cache=True, cache_expire=3):
        """See class docstring."""
        super().__init__(host, auth=auth, verify=verify, adapter=adapter, cache=cache, cache_expire=cache_expire)
        self.pj = project

        self.args = [host, project]
        self.kwargs = {"auth": auth, "verify": verify, "adapter":adapter, "cache":cache, "cache_expire":cache_expire}

    @classmethod
    @GerritRest.get()
    def query(cls, *args, **kwargs):
        """Performs a GET request to query for projects from the Gerrit API.

        **API URL**: `/a/projects/ <https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#list-projects>`

        **Input type**: `QueryOptions <https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#list-projects>`

        **Return type**: `ProjectInfo  <https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#project-info>`

        Usage::

            project.query(
                query="name:test"
            )
        """
        return urljoin(cls.host, urlformat(GerritProject._endpoint, ""))
    
    @GerritRest.get()
    @GerritRest.url_wrapper()
    def access(self, *args, **kwargs):
        """Performs a GET request to list access rights for project from the Gerrit API.

        **API URL**: `/a/projects/ <https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#get-access>`

        **Input type**: `QueryOptions <https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#get-access>`

        **Return type**: `ProjectAccessInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-access.html#project-access-info>`

        Usage::
            project.access()
        """
        pass