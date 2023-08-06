"""The model class all models have to inherit from."""

from __future__ import annotations

import typing

from .fields import Field
from .utils import classproperty


# TODO differentiate between required for creation and required for instanziation
class Model:
    """The model class all models have to inherit from."""

    def __init__(self, **kwargs):
        # evaluate fields
        self._fields = {
            name: value
            for name, value in self.__class__.__dict__.items()
            if isinstance(value, Field)
        }
        self._required_fields = {
            name for name, value in self._fields.items() if value.required
        }
        self._id_field = None

        for name, field in self._fields.items():
            if field.is_id_field:
                if self._id_field:
                    raise ValueError(
                        f"There are multiple id_fields defined for this model {self.__class__}."
                    )
                else:
                    self._id_field = name
        if not self._id_field:
            if "id" in self._fields:
                self._id_field = "id"
            elif "pk" in self._fields:
                self._id_field = "pk"
        # warning no id field defined

        if not kwargs:
            # mode 1: no args, return an empty instance

            return

        # mode 2: all args must be specified

        for name, value in kwargs.items():
            if name in self._fields:
                field = self._fields[name]
                value = field.clean(value)
                setattr(self, value)
            else:
                raise ValueError(f'Invalid argument "{name}".')

        missing_args = set()

        for name, description in self._fields.items():
            value = getattr(self, name)

            if not isinstance(value, Field):
                # field already initialized

                continue
            elif description.required:
                # required field not initialized
                missing_args.add(name)
            else:
                # not required, use default value
                setattr(self, name, description.default)

        if missing_args:
            raise ValueError(f'Missing argument for {", ".join(missing_args)}')

    @classmethod
    def from_api(cls, data: typing.Dict[typing.Any, typing.Any]) -> Model:
        """
        Create an instance from values fetched from the remote API.

        We do not expect to get all values.
        Additional data will be ignored.
        """

        class Unresolved:
            """We did not yet see any value for this field."""

        instance = cls()

        for name, field in instance._fields.items():
            if name in data:
                value = field.clean(data[name], _field_name=name)
                setattr(instance, name, value)
            else:
                setattr(instance, name, Unresolved)

        return instance

    def validate(self):
        """Validate instance for creation."""

        for name, field in self._fields.items():
            value = getattr(self, name)

            if name in self._fields:
                field.validate(value)
            else:
                raise ValueError(f'Invalid argument "{name}".')

    @classproperty
    def resource_name(cls):
        """
        :return: The qualified resource name (e. g. API path) for this class.

        This is a default implementation and can be overridden or set to something static.
        """

        return cls.__name__.rsplit(".", 1)[-1].lower()

    @property
    def id(self):
        """:return: A unique ID."""
        id_field_value = None

        if self._id_field:
            id_field_value = getattr(self, self._id_field, None)

        return id_field_value

    def __str__(self):
        return f"<{self.__class__.__name__} ({self.id})>"
