.. _advanced:

Advanced Usage
==============

This document present some detail usage of the library

Pass argument 
-------------

Sometimes we need to pass argument to Gerrit REST API, such like ``CURRENT_REVISION``.
This can be down by passing them to ``*args`` and ``**kwargs``::

    change.detail(**{"o":["CURRENT_REVISION", "CURRENT_COMMIT"]})

Query changes
-------------

Searching changes can be done by query method of GerritChange class::

    from pGerrit.client import GerritClient
    from requests.auth import HTTPBasicAuth

    auth = HTTPBasicAuth("xxxxxxxxxxxx","xxxxxxxxxxxxxx")
    client = GerritClient("https://xxxx.gerrit.com/", auth=auth)

    changes = change.query(q="owner:self status:merged", **{"no-limit":"", "o":["CURRENT_REVISION", "CURRENT_COMMIT"]})

    for change in changes:
        print("branch name:" + change.branch)

Disable cache
-------------

By default, our library use ``requests-cache`` to cache GET method
in case of big amount of requests in short time to Gerrit server.

But if you need to retreive result exactly from Server rather than
cache, you can disable it in GerritClient object::

    client = GerritClient("https://xxxx.gerrit.com/", cache=False)

Handling exceptions
-------------------

You can use ``try catch`` to handle exceptions::

    from Gerrit.exception import  GerritError
    from Gerrit.client import GerritClient
    from requests.auth import HTTPBasicAuth

    auth = HTTPBasicAuth("xxxxxxxxxxxxxxxx","xxxxxxxxxxxxxxxxxx")
    client = GerritClient("http://xxxxxxxxx.gerrit.com/", auth=auth)

    try:
      change = client.change("111111111111111111111") #obviously this is a non-exist change
      detail = change.detail()
    except GerritError as e:
      print(e.status, e.content)
    else:
      pass
    finally:
      pass

Result
    ``404 b'Not found: 111111111111111111111\n'``