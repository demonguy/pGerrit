from pGerrit.restAPIwrapper import GerritRest
from pGerrit.client import GerritClient
from pGerrit.utils import urljoin, urlformat

class GerritChange(GerritClient):
    """Class maps /changes/ endpoint of Gerrit REST API

    :return: An instance of GerritChange.
    :rtype: pGerrit.change.GerritChange

    You won't need to instantiate this Class directly.
    Use ``pGerrit.GerritClient.change``
    """
    _endpoint = "/a/changes/{}"
    _args = ["id"]

    def __init__(self, host, gerritID, auth=None, verify=True, adapter=None, cache=True, cache_expire=3):
        """See class docstring."""
        super().__init__(host, auth=auth, verify=verify, adapter=adapter, cache=cache, cache_expire=cache_expire)
        self.id = gerritID

        self.args = [host, gerritID]
        self.kwargs = {"auth": auth, "verify": verify, "adapter":adapter, "cache":cache, "cache_expire":cache_expire}

    @classmethod
    @GerritRest.get()
    def query(cls, *args, **kwargs):
        """Performs a GET request to query for changes from the Gerrit API.

        **API URL**: `/a/changes/ <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-changes>`__

        **Input type**: `QueryOptions <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-changes>`__

        **Return type**: List[`ChangeInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#change-info>`__]

        Usage::

            change.query(
                q="owner:self status:merged",
                **{
                    "no-limit": "",
                    "o": [
                        "CURRENT_REVISION",
                        "CURRENT_COMMIT"
                    ]
                }
            )
        """
        return urljoin(cls.host, urlformat(GerritChange._endpoint, ""))

    @classmethod
    @GerritRest.post
    def create(cls, payload=None, *args, **kwargs):
        """Performs a POST request to create for changes from the Gerrit API.

        **API URL**: `/a/changes/ <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#create-change>`__

        **Input type**: `ChangeInput <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#create-change>`__

        **Return type**: List[`ChangeInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#change-info>`__]

        Usage::

            change.create(payload=
                {
                    "project": "xxx",
                    "branch": "xxx",
                    "subject": "xxx"
                }
            )
        """
        return urljoin(cls.host, urlformat(GerritChange._endpoint, ""))

    @GerritRest.get()
    def info(self, *args, **kwargs):
        """Performs a GET request to retrieve information about a change.

        **API URL**: `/a/changes/{change_id} <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-change>`__

        **Input type**: `QueryOptions <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-changes>`__

        **Return type**: `ChangeInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#change-info>`__

        Usage::

            change.info(**{o":["CURRENT_REVISION", "CURRENT_COMMIT"]})

        """
        return urljoin(self.host, urlformat(GerritChange._endpoint, self.id))

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def detail(self, *args, **kwargs):
        """Performs a GET request to retrieve detailed information about a change.

        **API URL**: `/a/changes/{change_id}/detail <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-change-detail>`__

        **Input type**: `QueryOptions <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-changes>`__

        **Return type**: `ChangeInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#change-info>`__ with additional fields

        Usage::

            change.detail(**{"o":["CURRENT_REVISION", "CURRENT_COMMIT"]})

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def topic(self, *args, **kwargs):
        """Performs a GET request to retrieve the topic of a change.

        **API URL**: `/a/changes/{change_id}/topic <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-topic>`__

        **Input type**: None

        **Return type**: str

        Usage::

            change.topic()

        """
        pass

    @GerritRest.put
    @GerritRest.url_wrapper("topic")
    def set_topic(self, *args, **kwargs):
        """Performs a PUT request to set the topic of a change.

        **API URL**: `/a/changes/{change_id}/topic <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#set-topic>`__

        **Input type**: `TopicInput <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#topic-input>`__

        **Return type**: str

        Usage::

            change.set_topic({"topic": "new-topic"})

        """
        pass

    @GerritRest.delete
    @GerritRest.url_wrapper("topic")
    def delete_topic(self, *args, **kwargs):
        """Performs a PUT request to set the topic of a change.

        **API URL**: `/a/changes/{change_id}/topic <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#set-topic>`__

        **Input type**: None

        **Return type**: None

        Usage::

            change.delete_topic()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def submitted_together(self, *args, **kwargs):
        """Performs a GET request to retrieve the list of changes that would be submitted together with a change.

        **API URL**: `/a/changes/{change_id}/submitted_together <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#submitted-together>`__

        **Input type**: None

        **Return type**: `SubmittedTogetherInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#submitted-together-info>`__

        Usage::

            change.submitted_together()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper("in")
    def in_(self, *args, **kwargs):
        """Performs a GET request to retrieve the list of changes that are included in a change.

        **API URL**: `/a/changes/{change_id}/in <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-related-changes>`__

        **Input type**: None

        **Return type**: `RelatedChangesInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#related-changes-info>`__

        Usage::

            change.in_()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def comments(self, *args, **kwargs):
        """Performs a GET request to retrieve comments on a change.

        **API URL**: `/a/changes/{change_id}/comments <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-change-comments>`__

        **Input type**: None

        **Return type**: Dict[str, List[`CommentInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#comment-info>`__]]

        Usage::

            change.comments()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def robotcomments(self, *args, **kwargs):
        """Performs a GET request to retrieve robot comments on a change.

        **API URL**: `/a/changes/{change_id}/robotcomments <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-robot-comments>`__

        **Input type**: None

        **Return type**: Dict[str, List[`RobotCommentInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#robot-comment-info>`__]]

        Usage::

            change.robotcomments()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def drafts(self, *args, **kwargs):
        """Performs a GET request to retrieve draft comments on a change.

        **API URL**: `/a/changes/{change_id}/drafts <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-drafts>`__

        **Input type**: None

        **Return type**: Dict[str, List[`CommentInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#comment-info>`__]]

        Usage::

            change.drafts()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def check(self, *args, **kwargs):
        """Performs a GET request to check the consistency of a change.

        **API URL**: `/a/changes/{change_id}/check <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#check-change>`__

        **Input type**: None

        **Return type**: List[`ChangeInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#change-info>`__ with ``problems`` fields]

        Usage::

            change.check()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def hashtags(self, *args, **kwargs):
        """Performs a GET request to retrieve the hashtags associated with a change.

        **API URL**: `/a/changes/{change_id}/hashtags <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-hashtags>`__

        **Input type**: None

        **Return type**: List[str]

        Usage::

            change.hashtags()

        """
        pass

    @GerritRest.post
    @GerritRest.url_wrapper("hashtags")
    def set_hashtags(self, payload=None, *args, **kwargs):
        """Performs a POST request to add or remove hashtags from a change.

        **API URL**: `/a/changes/{change_id}/hashtags <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#set-hashtags>`__

        **Input type**: `HashtagsInput <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#hashtags-input>`__

        **Return type**: List[str]

        Usage::

            change.set_hashtags(payload={"add":["tag1"], "remove":["tag2"]})

        """
        pass

    @GerritRest.post
    @GerritRest.url_wrapper()
    def rebase(self, payload=None, headers=None):
        """Performs a POST request to rebase a change.

        **API URL**: `/a/changes/{change_id}/rebase <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#rebase-change>`__

        **Input type**: `RebaseInput <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#rebase-input>`__ (optional)

        **Return type**: `ChangeInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#change-info>`__

        Usage::

            change.rebase()

        """
        pass

    @GerritRest.post
    @GerritRest.url_wrapper()
    def merge(self, payload=None, headers=None):
        """Performs a POST request to create merge patch set for change.

        **API URL**: `/a/changes/{change_id}/merge <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#create-merge-patch-set-for-change>`__

        **Input type**: `MergePatchSetInput <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#merge-patch-set-input>`__

        **Return type**: `ChangeInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#change-info>`__

        Usage::

            change.merge()

        """
        pass

    @GerritRest.delete
    @GerritRest.url_wrapper("")
    def delete_change(self, payload=None, headers=None):
        """Performs a DELETE request to delete a change.

        **API URL**: `/a/changes/{change_id} <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#delete-change>`__

        **Input type**: None

        **Return type**: None

        Usage::

            change.delete_change()

        """
        pass

    def is_merge(self):
        """Checks if the change is a merge change.

        Usage::

            is_merge_change = change.is_merge()

        """
        revision = self.current_revision()
        if len(revision.commit().parents) == 2:
            return True
        else:
            return False


    def revision(self, revisionID):
        """Creates a GerritChangeRevision object for a specific revision of the change.

        :param revisionID: The `revision ID <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#ids>`__ (commit SHA1 or numeric ID)

        Usage::

            change_revision = change.revision(revisionID)

        """
        return GerritChangeRevision(self.host, self.id, revisionID, auth=self.session.auth, verify=self.verify, adapter=self.adapter, cache=self.cache, cache_expire=self.cache_expire)

    def current_revision(self):
        """Creates a GerritChangeRevision object for the current revision of the change.

        Usage::

            current_revision = change.current_revision()

        """
        return GerritChangeRevision(self.host, self.id, "current", auth=self.session.auth, verify=self.verify, adapter=self.adapter, cache=self.cache, cache_expire=self.cache_expire)

    @property
    def edit(self):
        """Provides an instance of GerritChangeEditQueryDescriptor for the given Gerrit client configuration.

        :return: An instance of GerritChangeEditQueryDescriptor.
        :rtype: pGerrit.queryDescriptor.GerritChangeEditQueryDescriptor

        Usage::

            change = GerritChange(...)
            edit_info = change.edit.info()
            edited_content = change.edit("COMMIT_MSG").edit_retrieve()

        """
        from pGerrit.queryDescriptor import GerritChangeEditQueryDescriptor
        return GerritChangeEditQueryDescriptor(self)

    @property
    def reviewer(self):
        """Provides an instance of GerritChangeReviewerQueryDescriptor for the given Gerrit client configuration.

        :return: An instance of GerritChangeReviewerQueryDescriptor.
        :rtype: pGerrit.queryDescriptor.GerritChangeReviewerQueryDescriptor

        Usage::

            change = GerritChange(...)
            reviewers = change.reviewer.query()
            suggested_reviewers = change.reviewer.suggest_reviewers(q="john")
            result = change.reviewer.add_reviewer({"reviewer": "example@example.com"})

        """
        from pGerrit.queryDescriptor import GerritChangeReviewerQueryDescriptor
        return GerritChangeReviewerQueryDescriptor(self)

class GerritChangeEdit(GerritChange):
    """Class maps /a/changes/{change_id}/edit endpoint of Gerrit REST API

    :return: An instance of GerritChangeEdit.
    :rtype: pGerrit.change.GerritChangeEdit

    You won't need to instantiate this Class directly.
    Use ``pGerrit.change.GerritChange.revision``
    """
    _endpoint = "/a/changes/{}/edit/{}"
    _args = ["id", "fileID"]

    def __init__(self, host, gerritID, fileID, auth=None, verify=True, adapter=None, cache=True, cache_expire=3):
        """See class docstring."""
        super().__init__(host, gerritID, auth=auth, verify=verify, adapter=adapter, cache=cache, cache_expire=cache_expire)
        self.fileID = fileID

    @classmethod
    @GerritRest.get()
    def info(self, *args, **kwargs):
        """Performs a GET request to retrieve information about the change edit.

        **API URL**: `/a/changes/{change_id}/edit <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#edit-endpoints>`__

        **Input type**: None

        **Return type**: `EditInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#edit-info>`__

        Usage::

            edit.info()

        """
        return urljoin(self.host, urlformat(GerritChangeEdit._endpoint, self.id, ""))

    @classmethod
    @GerritRest.post
    @GerritRest.url_wrapper("edit:publish")
    def edit_publish(self, payload=None, headers=None):
        """Performs a POST request to publish a change edit.

        **API URL**: `/a/changes/{change_id}/edit/edit:publish <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#publish-edit>`__

        **Input type**: `PublishChangeEditInput <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#publish-change-edit-input>`__ (optional)

        **Return type**: None

        Usage::

            edit.edit_publish()

        """
        pass

    @classmethod
    @GerritRest.post
    @GerritRest.url_wrapper("edit")
    def edit_restore(self, payload=None, headers=None):
        """Performs a POST request to restore a change edit.

        **API URL**: `/a/changes/{change_id}/edit <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#post-edit>`__

        **Input type**: `ChangeEditInput <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#change-edit-input>`__
        
        **Return type**: None

        Usage::

            edit.edit_restore({"restore_path": "foo"})

        """
        pass

    @classmethod
    @GerritRest.delete
    @GerritRest.url_wrapper("edit")
    def edit_delete(self, headers=None):
        """Performs a DELETE request to delete a change edit.

        **API URL**: `/a/changes/{change_id}/edit <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#delete-edit>`__

        **Input type**: None

        **Return type**: None

        Usage::

            edit.edit_delete()

        """
        pass

    @GerritRest.put
    @GerritRest.url_wrapper()
    def edit_file(self, payload, headers=None):
        """Performs a PUT request to edit a specific file in a change revision.

        **API URL**: `/a/changes/{change_id}/edit/{file_id} <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#edit-file>`__

        **Input type**: str

        **Return type**: None

        Usage::

            edit_file.edit(payload='new_file_content')

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def edit_retrieve(self, headers=None):
        """Performs a GET request to retrieve the content of a specific file in a change revision after editing.

        **API URL**: `/a/changes/{change_id}/edit/{file_id} <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-edit>`__

        **Input type**: None

        **Return type**: str

        Usage::

            edited_content = edit_file.edit_retrieve()

        """
        pass

class GerritChangeReviewer(GerritChange):
    """Class maps /a/changes/{change_id}/reviewers/{account_id} endpoint of Gerrit REST API

    :return: An instance of GerritChangeReviewer.
    :rtype: pGerrit.change.GerritChangeReviewer

    You won't need to instantiate this Class directly.
    Use ``pGerrit.change.GerritChange.reviewer``
    """
    _endpoint = "/a/changes/{}/reviewers/{}"
    _args = ["id", "account_id"]

    def __init__(self, host, gerritID, account_id, auth=None, verify=True, adapter=None, cache=True, cache_expire=3):
        """See class docstring."""
        super().__init__(host, gerritID, auth=auth, verify=verify, adapter=adapter, cache=cache, cache_expire=cache_expire)
        self.account_id = account_id

    @classmethod
    @GerritRest.get()
    def query(self, *args, **kwargs):
        """Performs a GET request to retrieve information about the change edit.

        **API URL**: `/a/changes/{change_id}/reviewers/ <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-reviewers>`__

        **Input type**: None
        """
        return urljoin(self.host, urlformat(GerritChangeReviewer._endpoint, self.id, ""))

    @classmethod
    @GerritRest.get()
    def suggest_reviewers(self, *args, **kwargs):
        """Performs a GET request to retrieve a list of suggested reviewers for a change.

        **API URL**: `/a/changes/{change_id}/suggest_reviewers <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#suggest-reviewers>`__

        **Input type**: `SuggestReviewersOptions <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#suggest-reviewers>`__

        **Return type**: List[`SuggestedReviewerInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#suggested-reviewer-info>`__]

        Usage::

            reviewer.suggest_reviewers(q="john")

        """
        return urljoin(self.host, urlformat("/a/changes/{}/suggest_reviewers", self.id, "suggest_reviewers"))

    @classmethod
    @GerritRest.post
    def add_reviewer(self, payload=None, *args, **kwargs):
        """Performs a POST request to add a reviewer to a change.

        **API URL**: `/a/changes/{change_id}/reviewers <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#add-reviewer>`__

        **Input type**: `ReviewerInput <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#reviewer-input>`__

        **Return type**: `ReviewerResult <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#reviewer-result>`__

        Usage::

            reviewer.add_reviewer({"reviewer": "example@example.com"})

        """
        return urljoin(self.host, urlformat(self._endpoint, self.id, ""))


class GerritChangeRevision(GerritChange):
    """Class maps /a/changes/{change_id}/revisions/{revision_id} endpoint of Gerrit REST API

    :return: An instance of GerritChangeRevision.
    :rtype: pGerrit.change.GerritChangeRevision

    You won't need to instantiate this Class directly.
    Use ``pGerrit.change.GerritChange.revision``
    """
    _endpoint = "/a/changes/{}/revisions/{}"
    _args = ["id", "revisionID"]

    def __init__(self, host, gerritID, revisionID, auth=None, verify=True, adapter=None, cache=True, cache_expire=3):
        """See class docstring."""
        super().__init__(host, gerritID, auth=auth, verify=verify, adapter=adapter, cache=cache, cache_expire=cache_expire)
        self.revisionID = revisionID

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def commit(self, *args, **kwargs):
        """Performs a GET request to retrieve the commit associated with the change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/commit <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-commit>`__

        **Input type**: None

        **Return type**: `CommitInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#commit-info>`__

        Usage::

            commit_info = revision.commit()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def actions(self, *args, **kwargs):
        """Performs a GET request to retrieve the available actions for the change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/actions <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-revision-actions>`__

        **Input type**: None

        **Return type**: Dict[str, `ActionInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#action-info>`__]

        Usage::

            actions = revision.actions()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def review(self, *args, **kwargs):
        """Performs a GET request to retrieve the review labels for the change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/review <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-review>`__

        **Input type**: None

        **Return type**: `ReviewInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#review-info>`__

        Usage::

            review_info = revision.review()

        """
        pass

    @GerritRest.post
    @GerritRest.url_wrapper("review")
    def set_review(self, payload=None, headers=None):
        """Performs a POST request to set a review for the change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/review <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#set-review>`__

        **Input type**: `ReviewInput <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#review-input>`__

        **Return type**: `ReviewResult <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#review-result>`__

        Usage::

            review_result = revision.set_review(payload)

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def related(self, *args, **kwargs):
        """Performs a GET request to retrieve related changes and revisions for the change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/related <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-related-changes>`__

        **Input type**: None

        **Return type**: `RelatedChangesInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#related-changes-info>`__

        Usage::

            related_changes = revision.related()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def patch(self, *args, **kwargs):
        """Performs a GET request to retrieve the patch for the change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/patch <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-patch>`__

        **Input type**: None

        **Return type**: str (Base64-encoded patch text)

        Usage::

            patch_text = revision.patch()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def mergeable(self, *args, **kwargs):
        """Performs a GET request to check if the change revision is mergeable.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/mergeable <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-mergeable>`__

        **Input type**: None

        **Return type**: `MergeableInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#mergeable-info>`__

        Usage::

            mergeable_info = revision.mergeable()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def submit_type(self, *args, **kwargs):
        """Performs a GET request to retrieve the submit type of the change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/submit_type <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-submit-type>`__

        **Input type**: None

        **Return type**: str (Submit type)

        Usage::

            submit_type = revision.submit_type()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def drafts(self, *args, **kwargs):
        """Performs a GET request to retrieve the draft comments on the change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/drafts <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-drafts>`__

        **Input type**: None

        **Return type**: List[`CommentInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#comment-info>`__]

        Usage::

            drafts = revision.drafts()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def comments(self, *args, **kwargs):
        """Performs a GET request to retrieve the published comments on the change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/comments <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-comments>`__

        **Input type**: None

        **Return type**: Dict[str, List[`CommentInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#comment-info>`__]]

        Usage::

            comments = revision.comments()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def files(self, *args, **kwargs):
        """Performs a GET request to retrieve the files of the change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/files <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-files>`__

        **Input type**: None

        **Return type**: Dict[str, `FileInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#file-info>`__]

        Usage::

            files = revision.files()

        """
        pass

    @GerritRest.post
    @GerritRest.url_wrapper()
    def cherrypick(self, payload=None, headers=None):
        """Performs a POST request to cherry-pick the change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/cherrypick <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#cherry-pick>`__

        **Input type**: `CherryPickInput <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#cherrypick-input>`__

        **Return type**: `ChangeInfo <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#change-info>`__

        Usage::

            cherrypick_result = revision.cherrypick(payload={"destination": "branch_name"})

        """
        pass

    def file(self, fileID):
        """Get the GerritChangeRevisionFile instance for a specific file in the change revision.

        :arg str fileID: The ID of the file.

        :return: A GerritChangeRevisionFile instance for the specified file.
        :rtype: pGerrit.change.GerritChangeRevisionFile

        Usage::

            file_instance = revision.file(fileID)

        """
        return GerritChangeRevisionFile(self.host, self.id, self.revisionID, fileID, auth=self.session.auth, verify=self.verify, adapter=self.adapter, cache=self.cache, cache_expire=self.cache_expire)

    def reviewer(self, accountID):
        """Get the GerritChangeRevisionReviewer instance for a specific reviewer of the change revision.

        :arg str accountID: The ID of the reviewer.

        :return: A GerritChangeRevisionReviewer instance for the specified reviewer.
        :rtype: pGerrit.change.GerritChangeRevisionReviewer

        Usage::

            reviewer_instance = revision.reviewer(accountID)

        """
        return GerritChangeRevisionReviewer(self.host, self.id, self.revisionID, accountID, auth=self.session.auth, verify=self.verify, adapter=self.adapter, cache=self.cache, cache_expire=self.cache_expire)

class GerritChangeRevisionReviewer(GerritChangeRevision):
    """Class maps /a/changes/{change_id}/revisions/{revision_id}/reviewers/{account_id} endpoint of Gerrit REST API

    :return: An instance of GerritChangeRevisionReviewer.
    :rtype: pGerrit.change.GerritChangeRevisionReviewer

    You won't need to instantiate this Class directly.
    Use ``pGerrit.change.GerritChangeRevision.reviwer``
    """
    _endpoint = "/a/changes/{}/revisions/{}/reviewers/{}"
    _args = ["id", "accountID", "revisionID", "accountID"]

    def __init__(self, host, gerritID, revisionID, accountID, auth=None, verify=True, adapter=None, cache=True, cache_expire=3):
        """See class docstring."""
        super().__init__(host, gerritID, revisionID, auth=auth, verify=verify, adapter=adapter, cache=cache, cache_expire=cache_expire)
        self.accountID = accountID

    @GerritRest.get()
    def list(self, *args, **kwargs):
        """List reviewers of a specific change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/reviewers/ <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#list-reviewers>`__

        :return: A list of reviewers for the specified change revision.
        :rtype: list

        Usage::

            reviewers = revision_reviewer.list()

        """
        return urljoin(self.host, urlformat(self._endpoint, self.id, self.revisionID, ""))

    @GerritRest.delete
    def delete_vote(self, label, *args, **kwargs):
        """Delete a vote from a specific reviewer on a change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/reviewers/{account_id}/votes/{label} <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#delete-vote>`__

        :arg str label: The label of the vote to be deleted.

        :return: None

        Usage::

            revision_reviewer.delete_vote(label)

        """
        return urljoin(self.host, urlformat(self._endpoint, self.id, self.revisionID, self.accountID), "votes", label)


class GerritChangeRevisionFile(GerritChangeRevision):
    """Class maps /a/changes/{change_id}/revisions/{revision_id}/files/{file_id} endpoint of Gerrit REST API

    :return: An instance of GerritChangeRevisionFile.
    :rtype: pGerrit.change.GerritChangeRevisionFile

    You won't need to instantiate this Class directly.
    Use ``pGerrit.change.GerritChangeRevision.file``
    """
    _endpoint = "/a/changes/{}/revisions/{}/files/{}"
    _args = ["id", "revisionID", "fileID"]

    def __init__(self, host, gerritID, revisionID, fileID, auth=None, verify=True, adapter=None, cache=True, cache_expire=3):
        super().__init__(host, gerritID, revisionID, auth=auth, verify=verify, adapter=adapter, cache=cache, cache_expire=cache_expire)
        self.fileID = fileID

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def content(self, *args, **kwargs):
        """Retrieve the content of a specific file in a change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/files/{file_id}/content <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-content>`__

        :return: The content of the specified file in the change revision.
        :rtype: str

        Usage::

            file_content = revision_file.content()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def diff(self, *args, **kwargs):
        """Retrieve the diff of a specific file in a change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/files/{file_id}/diff <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-diff>`__

        :return: The diff of the specified file in the change revision.
        :rtype: dict

        Usage::

            file_diff = revision_file.diff()

        """
        pass

    @GerritRest.get(raw=True)
    @GerritRest.url_wrapper()
    def download(self, *args, **kwargs):
        """Download the content of a specific file in a change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/files/{file_id}/download <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#download-content>`__

        :return: The downloaded content of the specified file in the change revision.
        :rtype: bytes

        Usage::

            downloaded_content = revision_file.download()

        """
        pass

    @GerritRest.get()
    @GerritRest.url_wrapper()
    def blame(self, *args, **kwargs):
        """Retrieve the blame information for a specific file in a change revision.

        **API URL**: `/a/changes/{change_id}/revisions/{revision_id}/files/{file_id}/blame <https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#get-blame>`__

        :return: The blame information of the specified file in the change revision.
        :rtype: list

        Usage::

            blame_info = revision_file.blame()

        """
        pass

    def is_binary(self):
        """Check if the file is a binary file.

        :return: True if the file is a binary file, False otherwise.
        :rtype: bool

        Usage::

            is_binary_file = revision_file.is_binary()

        """
        file_info = getattr(self.files(), self.fileID)
        if hasattr(file_info, "binary") and file_info.binary == True:
            return True
        else:
            return False

    @GerritRest.get()
    def get_history_log(self, commit=None, *args, **kwargs):
        """Retrieve the history log of a specific file in a change revision.

        :param commit: (optional) The commit hash to get the history log from.
                       If not provided, the current commit will be used.
        :type commit: str

        :return: The history log of the specified file in the change revision.
        :rtype: str

        Usage::

            history_log = revision_file.get_history_log(commit='commit_hash')

        """
        project = self.info().project
        commit = commit or self.commit().commit
        return urljoin(self.host, "a/plugins", "gitiles", project, "+log", commit, self.fileID)
