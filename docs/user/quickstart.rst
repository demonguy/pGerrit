.. _quickstart:

Quickstart
==========

Let's get started with some simple examples.


Print change info of AOSP Gerrit
--------------------------------

Since Google AOSP Gerrit doesn't require authentication for read permission
We can just run code below::

    from pGerrit.client import GerritClient

    client = GerritClient("https://android-review.googlesource.com/")
    change = client.change("1285870")
    detail = change.detail()

    print("")
    print("branch name: " + detail.branch)
    print("project name: " + detail.project)
    print("created time: " + detail.created)
    print("updated time: " + detail.updated)
    print("")
    print("Check this url to make sure info above is correct")
    print("https://android-review.googlesource.com/c/platform/frameworks/support/+/1285870")

That's all well and good

Use it on private Gerrit
------------------------

If you want to use pGerrit on your private Gerrit host. Then you probably
need to get a HTTP password for authentication.

If your Gerrit administrator stay default configuration, then you can find your HTTP password
by ``Settings``->``HTTPCredentials``->``GENERATE NEW PASSWORD``. And your username at
``Settings``->``Profile``->``Username``

Then you can use it like below::

    from pGerrit.client import GerritClient
    from requests.auth import HTTPBasicAuth

    auth = HTTPBasicAuth("xxxxxxxxxxxx","xxxxxxxxxxxxxx")
    client = GerritClient("https://xxxx.gerrit.com/", auth=auth)
    change = client.change("your_change_id")
    current = change.current_revision()

    detail = change.detail()

    print("project name:" + detail.project)
    print("branch name:" + detail.branch)
    print("created time:" + detail.created)
    print("updated time:" + detail.updated)

--------------------------

Ready for more? Check out the :ref:`advanced <advanced>` section.
