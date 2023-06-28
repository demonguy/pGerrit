import sys
import os
import requests

import unittest
from pGerrit.client import GerritClient
from pGerrit.change import GerritChange, GerritChangeRevision, GerritChangeRevisionFile, GerritChangeEdit, GerritChangeReviewer
from pGerrit.queryDescriptor import GerritChangeEditQueryDescriptor, GerritChangeReviewerQueryDescriptor
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

g_file_id = "COMMIT_MSG"

g_pj = os.environ.get("GERRIT_PROJECT_NAME")
assert g_pj is not None


class TestChange(unittest.TestCase):
    """docstring for TestGerrit"""
    def setUp(self):
        requests.packages.urllib3.disable_warnings()
        self.auth = HTTPBasicAuth(g_username, g_password)
        self.client = GerritClient(g_host, auth=self.auth, verify=False, cache=False)
        self.change = self.client.change(g_id)

    def tearDown(self):
        pass

    def testChangeQuery(self):
        results = self.client.change.query(q=g_id)
        self.assertIsInstance(results, list)
        for result in results:
            self.assertIsInstance(result, SimpleNamespace)

    def testChangeInfo(self):
        info = self.change.info(o=["ALL_COMMITS", "CURRENT_REVISION"])
        self.assertIsInstance(info, SimpleNamespace)
        self.assertEqual(info.branch, "master")

    def testChangeDetail(self):
        detail = self.change.detail(o=["ALL_COMMITS", "CURRENT_REVISION"])
        self.assertIsInstance(detail, SimpleNamespace)
        self.assertEqual(detail.branch, "master")

    def testChangeTopic(self):
        topic = self.change.topic()
        self.assertIsInstance(topic, str)

    def testSetChangeTopic(self):
        target_topic = "test_set_topic"
        self.change.set_topic(target_topic)
        topic = self.change.topic()
        self.assertEqual(topic, target_topic)

    def testDeleteChangeTopic(self):
        self.change.delete_topic()
        topic = self.change.topic()
        self.assertEqual(topic, "")

    def testChangeSubmitted_together(self):
        submitted_together = self.change.submitted_together()
        self.assertIsInstance(submitted_together, list)

    def testChange_in(self):
        _in = self.change.in_()
        self.assertIsInstance(_in, SimpleNamespace)

    def testChangeComments(self):
        comments = self.change.comments()
        self.assertIsInstance(comments, SimpleNamespace)

    def testChangeRobotComments(self):
        robot_comments = self.change.robotcomments()
        if len(vars(robot_comments)) == 0:
            return

        self.assertIsInstance(robot_comments, dict)
        for key, value in robot_comments.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, list)
            for comment in value:
                self.assertIsInstance(comment, SimpleNamespace)

    def testChangeDrafts(self):
        drafts = self.change.drafts()
        self.assertIsInstance(drafts, SimpleNamespace)

    def testChangeCheck(self):
        check = self.change.check()
        self.assertIsInstance(check, SimpleNamespace)

    def testChangeHashtags(self):
        hashtags = self.change.hashtags()
        if isinstance(hashtags, SimpleNamespace) and len(vars(hashtags)) == 0:
            return

        self.assertIsInstance(hashtags, list)
        for hashtag in hashtags:
            self.assertIsInstance(hashtag, str)

    def testSetChangeHashtag(self):
        target_hashtags = ["test1", "test2"]
        self.change.set_hashtags(payload={"add":target_hashtags})
        hashtags = self.change.hashtags()
        self.change.set_hashtags(payload={"remove":target_hashtags})
        self.assertEqual(set(hashtags), set(target_hashtags))

    @unittest.skip("This change cannot be rebased, so skip")
    def testChangeRebase(self):
        rebase = self.change.rebase()
        # self.assertIsInstance(edit, SimpleNamespace)

    def testChangeCreateMerge(self):
        createMerge = self.change.merge(payload={
            "merge": {
                "source": self.change.revision("1").commit().commit,
                "allow_conflicts": "True"
            }
        })
        self.assertEqual(createMerge.status_code, 200)

    def testChangeIsMerge(self):
        self.assertTrue(self.change.is_merge())

    def testChangeCurrentRevision(self):
        revision = self.change.current_revision()
        self.assertIsInstance(revision, GerritChangeRevision)

    def testChangeRevision(self):
        revision = self.change.revision("current")
        self.assertIsInstance(revision, GerritChangeRevision)

    def testChangeEdit(self):
        edit = self.change.edit
        self.assertIsInstance(edit, GerritChangeEditQueryDescriptor)

    def testChangeReviewer(self):
        reviewer = self.change.reviewer
        self.assertIsInstance(reviewer, GerritChangeReviewerQueryDescriptor)

class TestChangeRevisionReviewer(unittest.TestCase):
    """docstring for Test"""
    def setUp(self):
        requests.packages.urllib3.disable_warnings()
        self.auth = HTTPBasicAuth(g_username, g_password)
        self.client = GerritClient(g_host, auth=self.auth, verify=False)
        self.change = self.client.change(g_id)
        self.revision = self.change.revision("1")
        self.current = self.change.current_revision()
        self.reviewer = self.current.reviewer("")

    def tearDown(self):
        pass

    def testRevisionReviewerList(self):
        files = self.reviewer.list()
        self.assertIsInstance(files, list)

    @unittest.skip("Delete vote can only delete others vote, so cannot be idempotent")
    def testRevisionReviewerDeleteVote(self):
        files = self.reviewer.delete_vote()
        self.assertIsInstance(files, SimpleNamespace)

class TestGerritChangeReviewer(unittest.TestCase):

    def setUp(self):
        requests.packages.urllib3.disable_warnings()
        self.auth = HTTPBasicAuth(g_username, g_password)
        self.client = GerritClient(g_host, auth=self.auth, verify=False)
        self.change = self.client.change(g_id)
        self.revision = self.change.revision("1")
        self.current = self.change.current_revision()
        self.reviewer = self.change.reviewer

    def test_query(self):
        reviewers = self.reviewer.query()
        if isinstance(reviewers, SimpleNamespace) and len(vars(reviewers)) == 0:
            return

        self.assertIsInstance(reviewers, list)
        for reviewer in reviewers:
            self.assertIsInstance(reviewer, SimpleNamespace)

    def test_suggest_reviewers(self):
        suggested_reviewers = self.reviewer.suggest_reviewers(q="john")
        self.assertIsInstance(suggested_reviewers, list)

    @unittest.skip
    def test_add_reviewer(self):
        response = self.gerrit_reviewer.add_reviewer({"reviewer": "example@example.com"})
        self.assertIsNotNone(response)

class TestGerritChangeEdit(unittest.TestCase):

    def setUp(self):
        requests.packages.urllib3.disable_warnings()
        self.auth = HTTPBasicAuth(g_username, g_password)
        self.client = GerritClient(g_host, auth=self.auth, verify=False)
        self.change = self.client.change(g_id)
        self.edit = self.change.edit(g_file_id)

    def test_info(self):
        info = self.change.edit.info()
        self.assertIsNotNone(info)

    @unittest.skip
    def test_edit_publish(self):
        # Create an edit before trying to publish
        self.edit.edit_file(payload='new_file_content')
        self.edit.edit_publish()

    @unittest.skip
    def test_edit_restore(self):
        # Create an edit before trying to restore
        self.edit.edit_file(payload='new_file_content')
        self.edit.edit_restore({"restore_path": "foo"})

    @unittest.skip
    def test_edit_delete(self):
        # Create an edit before trying to delete
        self.edit.edit_file(payload='new_file_content')
        self.edit.edit_delete()

    @unittest.skip
    def test_edit_file(self):
        self.edit.edit_file(payload='new_file_content')

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

class TestProject(unittest.TestCase):
    """docstring for TestGerrit"""
    def setUp(self):
        requests.packages.urllib3.disable_warnings()
        self.auth = HTTPBasicAuth(g_username, g_password)
        self.client = GerritClient(g_host, auth=self.auth, verify=False)
        self.project = self.client.project(g_pj)

    def tearDown(self):
        pass

    def testProjectQuery(self):
        results = self.client.project.query(query=g_pj)
        self.assertIsInstance(results, list)
        for result in results:
            self.assertIsInstance(result, SimpleNamespace)

    def testProjectAccess(self):
        access = self.project.access()
        self.assertIsInstance(access, SimpleNamespace)

if __name__ == "__main__":
    unittest.main()