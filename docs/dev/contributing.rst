.. _contributing:

Contributor's Guide
===================

If you're interested in contributing to pGerrit.
Thank you very much! Here are some tips of contributing

Code explain
------------

How does the code work?
~~~~~~~~~~~~~~~~~~~~~~~

**The decorator**

Because of time limit, I didn't implement all REST API of Gerrit
(Maybe I can try ChatGPT4.0 later:) ). But adding a new REST API
is pretty easy and elegant::

   @GerritRest.get
   @GerritRest.url_wrapper
   def detail(self, *args, **kwargs):
       pass

Calling this method will invoke request to `http://{your_host_name}/a/changes/{change_id}/detail <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-change-detail>`__

The @GerritRest.url_wrapper decorator is used to assemble the URL.
In the REST API detail interface, you should send a GET request to access
the URL ``http://{your_host_name}/a/changes/{change_id}/detail``.This decorator
assembles the URL, and the last line
``urljoin(self.host, urlformat(cls_d._endpoint, *args), name)`` is equivalent
to urljoin("{your_host_name}", "/a/changes/{your_change_id}", "detail").
You can now understand what cls_d._endpoint and name actually represent.

The @GerritRest.get decorator is the function responsible for submitting HTTP
requests and accessing the data. It retrieves the URL from the decorated
function and sends a GET request to the URL directly.
The returned JSON data is then wrapped as a SimpleNamespace instance.

Transforming Json into SimpleNamespace allows you to avoid the
square brackets hell . (e.g. ``detail.branch`` rather than ``detail["branch"]``)

Running test
~~~~~~~~~~~~

The unit test codes are in tests/test.py. You should also write a unit test
if you add a new API.
However the test is highly depends on the target Gerrit environment. So we
read environment varibles for testing


First, find a change that meets requirements below

1. change should be in master branch
2. change is already merged
3. change has a topic
4. you can set a topic on this change
5. this change must have at least one reviewer
6. you can set label Code-review +1 on this change

then export variables below::

   export GERRIT_USERNAME=chengyang # use your own username
   export GERRIT_PASSWORD=pFFPgP/giebge0xxxxxxxxxxxxxxxxxx  # This is retreived from Gerrit->Settings->HTTP Credentials
   export GERRIT_HOST=https://{your host}/
   export GERRIT_CHANGE_NUMBER=1234567  #find a change that meets requirement above

then run ``python -m unittest tests/test.py``

Code Contributions
------------------

Steps for Submitting Code
~~~~~~~~~~~~~~~~~~~~~~~~~

When contributing code, you'll want to follow this checklist:

1. Fork the repository on GitHub.
2. Run the tests to confirm they all pass on your system. If they don't, you'll
   need to investigate why they fail. If you're unable to diagnose this
   yourself, raise it as a bug report
3. Write tests that demonstrate your bug or feature. Ensure that they fail.
4. Make your change.
5. Run the entire test suite again, confirming that all tests pass *including
   the ones you just added*.
6. Send a GitHub Pull Request to the main repository's ``main`` branch.
   GitHub Pull Requests are the expected method of code collaboration on this
   project.

Documentation Contributions
---------------------------

Documentation improvements are always welcome! The documentation files live in
the ``docs/`` directory of the codebase. They're written in
`reStructuredText`_, and use `Sphinx`_ to generate the full suite of
documentation.

When contributing documentation, please do your best to follow the style of the
documentation files. This means a soft-limit of 79 characters wide in your text
files and a semi-formal, yet friendly and approachable, prose style.

When presenting Python code, use single-quoted strings (``'hello'`` instead of
``"hello"``).

The API references are from doc strings in the .py source file. And using
``autodocs`` to generate documentation.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx-doc.org/index.html
