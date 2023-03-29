from pGerrit.client import GerritClient
from requests.auth import HTTPBasicAuth
import requests
requests.packages.urllib3.disable_warnings()

auth = HTTPBasicAuth("xxxxxxxxxxxx","xxxxxxxxxxxxxx")
client = GerritClient("https://android-review.googlesource.com/", auth=auth, verify=False)
change = client.change("1285870")
current = change.current_revision()

detail = change.detail()

print("project name:" + detail.project)
print("branch name:" + detail.branch)
print("created time:" + detail.created)
print("updated time:" + detail.updated)