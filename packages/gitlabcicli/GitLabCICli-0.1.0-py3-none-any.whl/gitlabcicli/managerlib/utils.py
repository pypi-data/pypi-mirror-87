"""Useful functions and more."""

from __future__ import annotations

import typing

from .errors import DoesNotExist, QueryError

if typing.TYPE_CHECKING:
    from .model import Model


class classproperty(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, owner):
        return self.func(owner)


def check_single_result(results: typing.List[Model]) -> Model:
    """
    Check if there is only one result in the results list and return it. Raise exceptions otherwise.
    """

    if len(results) == 1:
        return results[0]

    if len(results) > 1:
        raise QueryError(f"Expected one result but got {len(results)}.")
    raise DoesNotExist()
