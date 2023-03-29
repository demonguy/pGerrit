from pGerrit.client import GerritClient
from requests.auth import HTTPBasicAuth
import requests
requests.packages.urllib3.disable_warnings()

auth = HTTPBasicAuth("xxxxxxxxxxxxx","xxxxxxxxxxxxxxxxx")
client = GerritClient("https://android-review.googlesource.com/", auth=auth, verify=False)
change = client.change("1285870")
change.revision("current").set_review({"labels":{"Code-Review":1}})
change.revision("current").set_review({"labels":{"Code-Review":0}})