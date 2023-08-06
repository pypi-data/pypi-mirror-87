"""The API interface."""

from __future__ import annotations

import logging
import typing
from abc import abstractmethod

from requests import Session

from .errors import APIError, OperationalError
from .model import Model
from .utils import check_single_result

try:
    from hyper.contrib import HTTP20Adapter
except ImportError:
    HTTP20Adapter = None


LOGGER = logging.getLogger()


class APIDriver:
    """
    The abstract class all API implementations must inherit from.

    It follows more or less the CRUD design.
    """

    def __init__(self):
        self._model: typing.Optional[typing.Type[Model]] = None

    def use(self, model: typing.Type[Model]) -> APIDriver:
        """
        Configure the api driver to use a specific model for the next operation(s).
        """
        self._model = model

        return self

    def _check_model_set(self) -> None:
        """Raise an exception if no model is set with ``.use()``."""

        if not self._model:
            raise OperationalError("No model class set. Use `.use()` before.")

    def create(self, instance: Model) -> Model:
        """Create an instance of ``instance`` on the server side."""
        self._check_model_set()
        instance.validate()
        raise NotImplementedError()

    def get(self, **filter) -> typing.Optional[Model]:
        """Get a single instance for a given ``filter``."""
        self._check_model_set()
        raise NotImplementedError()

    def list(
        self,
        filter: typing.Optional[typing.Dict[str, typing.Any]] = None,
        order_by: typing.Optional[typing.List[str]] = None,
    ) -> typing.Iterable[Model]:
        """Get all matching instances for a given ``filter``."""
        self._check_model_set()
        raise NotImplementedError()

    def update(self) -> Model:
        """Update a ressource."""
        self._check_model_set()
        raise NotImplementedError()

    def delete(self) -> None:
        """Delete a ressource."""
        self._check_model_set()
        raise NotImplementedError()

    def __str__(self):
        model_name = self._model.__name__ if self._model else "-"

        return f"<{self.__class__.__name__} ({model_name})>"


class SimpleReadOnlyRESTAPIDriver(APIDriver):
    """A simple read only REST API Driver that may work for some REST APIs."""

    API_PATH = ""

    def __init__(self, host: str):
        super().__init__()
        self.session = Session()
        self.host = host

        if HTTP20Adapter:
            self.session.mount(self.host, HTTP20Adapter())

    @property
    def resource_url(self):
        """:return: The URL to the resource, that is configured using ``.use()``."""
        self._check_model_set()

        return f"{self.host}{self.API_PATH}/{self._model.resource_name}"

    def get(self, **filter):
        matching_instances = self.list(**filter)

        return check_single_result(matching_instances)

    def list(
        self,
        filter: typing.Optional[typing.Dict[str, typing.Any]] = None,
        order_by: typing.Optional[typing.List[str]] = None,
    ) -> typing.Iterable[Model]:
        self._check_model_set()

        response = self.session.get(
            self.resource_url,
            params={
                **(self.create_filter_params(**filter) if filter else {}),
                **(self.create_order_params(*order_by) if order_by else {}),
            },
        )
        try:
            result = response.json()
        except Exception:
            LOGGER.debug("No JSON in response")
            LOGGER.debug(response.text)

        LOGGER.debug(result)

        if not response.ok or result is None:
            raise APIError(result, response)

        if not isinstance(result, list):
            raise OperationalError(
                f"Expected a list as API response but got {type(result)}"
            )

        results = [self._model.from_api(data) for data in result]

        return results

    @abstractmethod
    def create_filter_params(
        self,
        **filter,
    ) -> typing.Dict[str, typing.Union[str, int, bool]]:
        """Create the GET-parameters for a given ``filter``."""

    @abstractmethod
    def create_order_params(
        self,
        *properties,
    ) -> typing.Dict[str, typing.Union[str, int, bool]]:
        """
        Create the GET-parameters for sorting the results.

        :param properties: Property names of the model in this notation `-id`, `+name`, `date_created`.
        """

    def __str__(self):
        model_name = self._model.__name__ if self._model else "-"

        return f"<{self.__class__.__name__} {self.host} ({model_name})>"
