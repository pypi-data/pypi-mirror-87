"""The Pipeline API model and additional things."""

import typing
from datetime import datetime
from enum import Enum

from gitlabcicli.managerlib import (
    BoolField,
    DateTimeField,
    IntField,
    Model,
    StrField,
    StrIntField,
)


class Pipeline(Model):
    #  The ID or URL-encoded path of the project owned by the authenticated user
    id: typing.Union[int, str] = StrIntField()
    # The scope of pipelines, one of: running, pending, finished, branches, tags
    scope: str = StrField()
    # The status of pipelines, one of: running, pending, success, failed, canceled, skipped, created, manual
    status: str = StrField()
    # The ref of pipelines
    ref: str = StrField()
    # The SHA of pipelines
    sha: str = StrField()
    # Returns pipelines with invalid configurations
    yaml_errors: bool = BoolField(default=False)
    # The name of the user who triggered pipelines
    name: str = StrField()
    # The username of the user who triggered pipelines
    username: str = StrField()
    # Return pipelines updated after the specified date. Format: ISO 8601 YYYY-MM-DDTHH:MM:SSZ
    updated_after: datetime = DateTimeField()
    # Return pipelines updated before the specified date. Format: ISO 8601 YYYY-MM-DDTHH:MM:SSZ
    updated_before: datetime = DateTimeField()
    # Order pipelines by id, status, ref, updated_at or user_id (default: id)
    order_by: str = StrField()
    # Sort pipelines in asc or desc order (default: desc)
    sort: str = StrField()
