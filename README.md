[![](docs/_static/logo.png)](https://pypi.org/project/pGerrit/)

[![Documentation](https://img.shields.io/readthedocs/pgerrit)](https://pgerrit.readthedocs.io/en/latest/)

[![PyPI](https://img.shields.io/pypi/v/pGerrit.svg?color=blue)](https://pypi.org/project/pGerrit/)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/pGerrit.svg)](https://pypi.org/project/pGerrit/)


## Summary
**pGerrit** is a lightweight Python library for calling Gerrit's [REST API](https://gerrit-review.googlesource.com/Documentation/rest-api.html). Essentially, pGerrit is designed to make it easy to access the REST API and retrieve relevant data, much like accessing properties of classes and objects. 
<!-- RTD-IGNORE -->
Complete project documentation can be found at [here](https://pgerrit.readthedocs.io/en/latest/).
<!-- END-RTD-IGNORE -->

## Features
* 🍰 **Clear design:** Every REST API endpoint is a class. Every entity of the endpoint is an object
* 🚀 **Easy of use** You can access the state of entity by access the property of the object
* ⚙️ **Easy to contribute** Add a new REST API is pretty easy by using decorator.

## Quickstart

### Installation
```bash
pip install pGerrit
```

### Run the code
Run the code below
```python
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
```

```
branch name: androidx-master-dev
project name: platform/frameworks/support
created time: 2020-04-15 17:53:11.000000000
updated time: 2020-04-16 16:58:26.000000000

Check this url to make sure info above is correct
https://android-review.googlesource.com/c/platform/frameworks/support/+/1285870
```
## Tips

### Chinese users
For Chinese users, Google is blocked by GFW. So you may need a proxy or VPN to get code above to work.
If you'd like to try this on your private Gerrit, you may need to pass `username` and `http_password` to `GerritClient` class. Check [document](https://pgerrit.readthedocs.io/en/latest/user/quickstart/#use-it-on-private-gerrit) here.

### The snippet above hangs there
If this code snippet hangs there and return after 2 minutes. You can try `wget https://android-review.googlesource.com`. If it also hangs there, you probably enabled your ipv6 but your ISP doesn't provide you corresponding services.
You can [disable ipv6](https://itsfoss.com/disable-ipv6-ubuntu-linux/) by following command:
```bash
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.lo.disable_ipv6=1

sudo sysctl -p
```

## Next Steps
To find out more about what you can do with pGerrit, see:

* [Quick Start](https://pgerrit.readthedocs.io/en/latest/user/quickstart/)
* [Advanced Usage](https://pgerrit.readthedocs.io/en/latest/user/advanced/)
* [API Reference](https://pgerrit.readthedocs.io/en/latest/api/)
