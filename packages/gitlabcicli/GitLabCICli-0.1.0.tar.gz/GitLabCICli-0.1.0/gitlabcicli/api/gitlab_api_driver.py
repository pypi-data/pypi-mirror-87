"""The API driver for GitLab API."""

import typing

from requests import Session

from gitlabcicli.managerlib import OperationalError, SimpleReadOnlyRESTAPIDriver

from .models import Pipeline, Project

try:
    from hyper.contrib import HTTP20Adapter
except ImportError:
    HTTP20Adapter = None


class GitLabAPIDriver(SimpleReadOnlyRESTAPIDriver):
    """The API driver for GitLab API."""

    API_PATH = "/api/v4"

    def __init__(self, host: str, private_token: typing.Optional[str] = None):
        super().__init__(host)

        if private_token:
            self.session.headers["PRIVATE-TOKEN"] = private_token

    def create_filter_params(
        self,
        **filter,
    ) -> typing.Dict[str, typing.Union[str, int, bool]]:
        self._check_model_set()

        if self._model is Pipeline:
            # TODO

            return filter
        elif self._model is Project:
            if "name" in filter:
                query = {
                    "search": filter.pop("name"),
                }

            if filter:
                raise OperationalError("You only can filter projects by name.")

            return query
        else:
            raise OperationalError(f"Unknown model configured: {self._model}")

    def create_order_params(
        self,
        *properties,
    ) -> typing.Dict[str, typing.Union[str, int, bool]]:
        self._check_model_set()

        if self._model is Pipeline:
            # TODO

            return {}
        elif self._model is Project:
            if len(properties) > 1:
                raise OperationalError("You can only order by one property of Project.")

            prop: str = properties[0]
            sort = "desc" if prop.startswith("-") else "asc"
            prop = prop.lstrip("+-")
            filterable_props = {"id", "name", "created_at", "last_activity_at"}
            if prop not in filterable_props:
                raise OperationalError(
                    f'You can only filter by {", ",join(filterable_props)}'
                )

            return {"order_by": prop, "sort": sort}
        else:
            raise OperationalError(f"Unknown model configured: {self._model}")
