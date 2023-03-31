pGerrit: Python Gerrit REST API
===============================

Release v\ |version|.

.. image:: https://img.shields.io/pypi/pyversions/pGerrit.svg
    :target: https://pypi.org/project/pGerrit/
    :alt: Python Version Support Badge

**pGerrit** is an elegant and simple Google Gerrit REST API library for Python.

-------------------

**Quick example of usage**::

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

**pGerrit** allows you to access endpoint by accessing corresponding class, and acess return value by object attributes
There's no need to care about REST API url

Features
----------------
- Decorator design pattern
- Get rid of REST API url
- Easy to add more APIs

The User Guide
--------------

This part of the documentation focuses on step-by-step
instructions for getting the most out of pGerrit.

.. toctree::
   :maxdepth: 2

   user/quickstart
   user/advanced

The API Documentation / Guide
-----------------------------

If you are looking for information on a specific function, class, or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api


The Contributor Guide
---------------------

If you want to contribute to the project, this part of the documentation is for
you.

.. toctree::
   :maxdepth: 2

   dev/contributing

