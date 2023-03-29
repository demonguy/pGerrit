from pGerrit.client import GerritClient
from requests.auth import HTTPBasicAuth
import json
import requests
requests.packages.urllib3.disable_warnings()

auth = HTTPBasicAuth("xxxxxxxxxx", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
client = GerritClient("https://android-review.googlesource.com/", auth=auth, verify=False)
change = client.change("1285870")
revision = change.revision("current")
result = revision.cherrypick({"destination":"sdk-release"})

# cherrypick already completed. we just format the information returned by server
try:
    result._content = result._content.replace(b")]}'\n", b"")
    j = json.loads(result.content)
    print(json.dumps(j, indent=4, sort_keys=True))
except:
    print(result.content)