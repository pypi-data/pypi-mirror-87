"""The Project API model and additional things."""

import typing
from datetime import datetime, date
from enum import Enum

from gitlabcicli.managerlib import (
    BoolField,
    DateField,
    DateTimeField,
    IntField,
    ListField,
    Model,
    PositiveIntField,
    StrField,
    StrIntField,
)


class ProjectVisibility(Enum):
    """Possible project visibilities."""

    PRIVATE = "private"
    INTERNAL = "internal"
    PUBLIC = "public"


class Project(Model):
    """The model for a project on GitLab"""

    resource_name = "projects"

    id: int = PositiveIntField()
    description: str = StrField()
    default_branch: str = StrField(default="master", nullable=True)
    visibility = StrField(choices=ProjectVisibility)
    ssh_url_to_repo: str = StrField(readonly=True)
    http_url_to_repo: str = StrField(readonly=True)
    web_url: str = StrField(readonly=True)
    readme_url: str = StrField(readonly=True, nullable=True)
    tag_list: typing.List[str] = ListField([StrField()], readonly=True)
    #  "owner": {
    #      "id": 3,
    #      "name": "Diaspora",
    #      "created_at": "2013-09-30T13:46:02Z"
    #  },
    name: str = StrField()
    name_with_namespace: str = StrField()
    path: str = StrField()
    path_with_namespace: str = StrField()
    issues_enabled: bool = BoolField()
    open_issues_count: int = PositiveIntField(readonly=True)
    merge_requests_enabled: bool = BoolField()
    jobs_enabled: bool = BoolField()
    wiki_enabled: bool = BoolField()
    snippets_enabled: bool = BoolField()
    can_create_merge_request_in: bool = BoolField()
    resolve_outdated_diff_discussions: bool = BoolField()
    container_registry_enabled: bool = BoolField()
    created_at: datetime = DateTimeField(readonly=True)
    last_activity_at: datetime = DateTimeField(readonly=True)
    creator_id: int = PositiveIntField(readonly=True)
    #  "namespace": {
    #      "id": 3,
    #      "name": "Diaspora",
    #      "path": "diaspora",
    #      "kind": "group",
    #      "full_path": "diaspora"
    #  },
    import_status = StrField(readonly=True)
    archived: bool = BoolField(default=False)
    avatar_url: str = StrField(nullable=True, readonly=True)
    shared_runners_enabled: bool = BoolField()
    forks_count: int = PositiveIntField(readonly=True)
    star_count: int = PositiveIntField(readonly=True)
    runners_token: str = StrField()
    ci_default_git_depth: int = PositiveIntField(nullable=True)
    public_jobs: bool = BoolField()
    shared_with_groups: typing.List = ListField([StrIntField()], readonly=True)
    only_allow_merge_if_pipeline_succeeds: bool = BoolField(default=False)
    only_allow_merge_if_all_discussions_are_resolved: bool = BoolField(default=False)
    remove_source_branch_after_merge: bool = BoolField(default=False, nullable=True)
    request_access_enabled: bool = BoolField()
    merge_method: str = StrField(default="merge")
    autoclose_referenced_issues: bool = BoolField(default=True)
    suggestion_commit_message: str = StrField(nullable=True, default=None)
    marked_for_deletion_on: date = DateField(readonly=True, nullable=True, default=None)
    #  "statistics": {
    #      "commit_count": 37,
    #      "storage_size": 1038090,
    #      "repository_size": 1038090,
    #      "wiki_size" : 0,
    #      "lfs_objects_size": 0,
    #      "job_artifacts_size": 0,
    #      "packages_size": 0
    #  },
    #  "_links": {
    #      "self": "http://example.com/api/v4/projects",
    #      "issues": "http://example.com/api/v4/projects/1/issues",
    #      "merge_requests": "http://example.com/api/v4/projects/1/merge_requests",
    #      "repo_branches": "http://example.com/api/v4/projects/1/repository_branches",
    #      "labels": "http://example.com/api/v4/projects/1/labels",
    #      "events": "http://example.com/api/v4/projects/1/events",
    #      "members": "http://example.com/api/v4/projects/1/members"
    #  },
