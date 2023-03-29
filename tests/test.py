import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import requests

import unittest
from pGerrit.client import GerritClient
from pGerrit.change import GerritChange, GerritChangeRevision, GerritChangeRevisionFile
from pGerrit.utils import urljoin
from requests.auth import HTTPBasicAuth
from pGerrit.utils import urljoin
from types import SimpleNamespace

import requests_cache
requests_cache.disabled()

# To run this test, User need to set environment variable below, the change should match following status in order to pass all tests
# 1. change should be in master branch
# 2. change is already merged
# 3. change has a topic
# 4. you can set a topic on this change
# 5. this change must have at least one reviewer
# 6. you can set label Code-review on this change +1

# export GERRIT_USERNAME=chengyang # use your own username
# export GERRIT_PASSWORD=pFFPgP/giebge0xxxxxxxxxxxxxxxxxx  # This is retreived from Gerrit->Settings->HTTP Credentials
# export GERRIT_HOST=https://android-review.googlesource.com/
# export GERRIT_CHANGE_NUMBER=1234567  #find a change that meets requirement above

# then run python -m unittest pGerrit/tests/test.py

g_username = os.environ.get("GERRIT_USERNAME")
assert g_username is not None

g_password = os.environ.get("GERRIT_PASSWORD")
assert g_password is not None

g_host =  os.environ.get("GERRIT_HOST")
assert g_host is not None

g_id = os.environ.get("GERRIT_CHANGE_NUMBER")
assert g_id is not None


class TestChange(unittest.TestCase):
    """docstring for TestGerrit"""
    def setUp(self):
        requests.packages.urllib3.disable_warnings()
        self.auth = HTTPBasicAuth(g_username, g_password)
        self.client = GerritClient(g_host, auth=self.auth, verify=False)
        self.change = self.client.change(g_id)

    def tearDown(self):
        pass

    def testChangeDetail(self):
        detail = self.change.detail(o=["ALL_COMMITS", "CURRENT_REVISION"])
        self.assertIsInstance(detail, SimpleNamespace)
        self.assertEqual(detail.branch, "master")

    def testChangeInfo(self):
        info = self.change.info(o=["ALL_COMMITS", "CURRENT_REVISION"])
        self.assertIsInstance(info, SimpleNamespace)
        self.assertEqual(info.branch, "master")

    def testChangeIsMerge(self):
        self.assertTrue(self.change.is_merge())

    def testChangeCurrentRevision(self):
        revision = self.change.current_revision()
        self.assertIsInstance(revision, GerritChangeRevision)

    def testChangeRevision(self):
        revision = self.change.revision("current")
        self.assertIsInstance(revision, GerritChangeRevision)

    def testChangeQuery(self):
        results = self.client.change.query(q=g_id)
        self.assertIsInstance(results, list)
        for result in results:
            self.assertIsInstance(result, SimpleNamespace)

    def testChangeTopic(self):
        topic = self.change.topic()
        self.assertIsInstance(topic, str)

    def testSetChangeTopic(self):
        target_topic = "test_set_topic"
        self.change.set_topic(target_topic)
        topic = self.change.topic()
        self.assertEqual(topic, target_topic)

    def testChangeSubmitted_together(self):
        submitted_together = self.change.submitted_together()
        self.assertIsInstance(submitted_together, list)

    def testChange_in(self):
        _in = self.change._in()
        self.assertIsInstance(_in, SimpleNamespace)

    def testChangeComments(self):
        comments = self.change.comments()
        self.assertIsInstance(comments, SimpleNamespace)

    def testChangeDrafts(self):
        drafts = self.change.drafts()
        self.assertIsInstance(drafts, SimpleNamespace)

    def testChangeCheck(self):
        check = self.change.check()
        self.assertIsInstance(check, SimpleNamespace)

    @unittest.skip("This change cannot be rebased, so skip")
    def testChangeRebase(self):
        rebase = self.change.rebase()
        # self.assertIsInstance(edit, SimpleNamespace)

    @unittest.skip("Edit will return empty unless the change is in the edit status")
    def testChangeEdit(self):
        edit = self.change.edit()
        self.assertIsInstance(edit, SimpleNamespace)

    @unittest.skip("Edit will return empty unless the change is in the edit status")
    def testChangeEditPublish(self):
        edit = self.change.edit_publish()
        self.assertIsInstance(edit, SimpleNamespace)

    @unittest.skip("Edit will return empty unless the change is in the edit status")
    def testChangeEditDelete(self):
        edit = self.change.edit_delete()
        self.assertIsInstance(edit, SimpleNamespace)

    def testChangeReviewers(self):
        reviewers = self.change.reviewers()
        self.assertIsInstance(reviewers[0], SimpleNamespace)

    def testChangeAddReviewers(self):
        payload = {"reviewer":g_username}
        res = self.change.add_reviewer(payload=payload)
        self.assertEqual(res.status_code, 200)

    def testChangeSuggest_reviewers(self):
        suggest_reviewers = self.change.suggest_reviewers()
        self.assertIsInstance(suggest_reviewers[0], SimpleNamespace)

class TestChangeRevisionReviewer(unittest.TestCase):
    """docstring for Test"""
    def setUp(self):
        requests.packages.urllib3.disable_warnings()
        self.auth = HTTPBasicAuth(g_username, g_password)
        self.client = GerritClient(g_host, auth=self.auth, verify=False)
        self.change = self.client.change(g_id)
        self.revision = self.change.revision("1")
        self.current = self.change.current_revision()
        self.reviewer = self.current.reviwer("")

    def tearDown(self):
        pass

    def testRevisionReviwerList(self):
        files = self.reviewer.list()
        self.assertIsInstance(files, list)

    @unittest.skip("Delete vote can only delete others vote, so cannot be idempotent")
    def testRevisionReviwerDeleteVote(self):
        files = self.reviewer.delete_vote()
        self.assertIsInstance(files, SimpleNamespace)

class TestChangeRevision(unittest.TestCase):
    """docstring for Test"""
    def setUp(self):
        requests.packages.urllib3.disable_warnings()
        self.auth = HTTPBasicAuth(g_username, g_password)
        self.client = GerritClient(g_host, auth=self.auth, verify=False)
        self.change = self.client.change(g_id)
        self.revision = self.change.revision("1")
        self.current = self.change.current_revision()

    def tearDown(self):
        pass

    def testRevisionFiles(self):
        files = self.revision.files()
        self.assertIsInstance(files, SimpleNamespace)

    def testRevisionCommit(self):
        commit = self.revision.commit()
        self.assertIsInstance(commit, SimpleNamespace)

    def testRevisionActions(self):
        actions = self.revision.actions()
        self.assertIsInstance(actions, SimpleNamespace)

    def testRevisionReview(self):
        review = self.revision.review()
        self.assertIsInstance(review, SimpleNamespace)

    def testRevisionRelated(self):
        related = self.revision.related()
        self.assertIsInstance(related, SimpleNamespace)

    # this change has 2 parents, so patch interface will raise error
    @unittest.expectedFailure
    def testRevisionPatch(self):
        patch = self.revision.patch()
        self.assertIsInstance(patch, SimpleNamespace)

    # this change is abandoned, so mergeable interface will rasie error
    # @unittest.expectedFailure
    @unittest.skip
    def testRevisionMergeable(self):
        mergeable = self.revision.mergeable()
        self.assertIsInstance(mergeable, SimpleNamespace)

    def testRevisionSubmit_type(self):
        submit_type = self.revision.submit_type()
        self.assertIsInstance(submit_type, str)

    def testRevisionDrafts(self):
        drafts = self.revision.drafts()
        self.assertIsInstance(drafts, SimpleNamespace)

    def testRevisionComments(self):
        comments = self.revision.comments()
        self.assertIsInstance(comments, SimpleNamespace)

    @unittest.skip
    def testRevisionSetReview(self):
        info = {"labels":{"Code-Review":1}}
        res = self.revision.set_review(payload=info)
        info["labels"]["Code-Review"] = 0
        res = self.revision.set_review(payload=info)
        self.assertEqual(res.status_code, 200)

class TestRevisionFile(unittest.TestCase):
    """docstring for TestRevisionFile"""
    """docstring for Test"""
    def setUp(self):
        requests.packages.urllib3.disable_warnings()
        self.auth = HTTPBasicAuth(g_username, g_password)
        self.client = GerritClient(g_host, auth=self.auth, verify=False)
        self.change = self.client.change(g_id)
        self.current = self.change.current_revision()
        self.file = self.current.file("1")

    def tearDown(self):
        pass

    def testRevisionFileContent(self):
        content = self.file.content()
        self.assertIsInstance(content, str)

    def testRevisionFileDiff(self):
        diff = self.file.diff()
        self.assertIsInstance(diff, SimpleNamespace)

    # this interface will return binary, so json decoder cannot handle it perfectly
    @unittest.skip
    def testRevisionFileDownload(self):
        download = self.file.download()
        self.assertIsInstance(download, SimpleNamespace)

    def testRevisionFileBlame(self):
        blame = self.file.blame()
        self.assertIsInstance(blame[0], SimpleNamespace)

    def testRevisionFileIsBinary(self):
        self.assertFalse(self.file.is_binary())

    def testRevisionGetHistoryLog(self):
        logs = self.file.get_history_log(format="JSON")
        for log in logs.log:
            self.assertIsInstance(log, SimpleNamespace)

class TestAccess(unittest.TestCase):
    """docstring for TestGerrit"""
    def setUp(self):
        requests.packages.urllib3.disable_warnings()
        self.auth = HTTPBasicAuth(g_username, g_password)
        self.client = GerritClient(g_host, auth=self.auth, verify=False)

    def tearDown(self):
        pass

    def testAccessQuery(self):
        access = self.client.access.query(project="All-Projects")
        self.assertIsInstance(access, SimpleNamespace)

