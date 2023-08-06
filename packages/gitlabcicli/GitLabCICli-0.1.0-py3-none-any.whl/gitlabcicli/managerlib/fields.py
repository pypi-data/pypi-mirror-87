"""Fields for models."""

import typing
from abc import abstractmethod, abstractproperty
from collections.abc import Iterable
from datetime import date, datetime

from .errors import ValidationError

if typing.TYPE_CHECKING:
    from enum import Enum


class EmptyParameter:
    """Dummy class for empty parameters."""


# TODO inherit from field?
# TODO differentiate between required for creation and required for instanziation
class Field:
    """The field all fields have to inherit from."""

    def __init__(
        self,
        description: str = "",
        default: typing.Any = EmptyParameter,
        nullable: bool = False,
        choices: "Enum" = None,
        readonly: bool = False,
        validators: typing.List[typing.Callable[[typing.Any], None]] = [],
        is_id_field: bool = False,
    ):
        self.description = description
        self.default = default
        self.nullable = nullable
        self.choices = choices
        self.readonly = readonly
        self.required = default == EmptyParameter
        self.validators = validators
        self.is_id_field = is_id_field

    def clean(self, value: typing.Any, _field_name: typing.Optional[str] = None):
        """Validate and clean the value."""

        if value is None:
            if self.nullable:
                return None
            else:
                raise ValidationError(
                    f"Value must not be None if field '{_field_name}'."
                    if _field_name
                    else "Value must not be None"
                )

        if self.choices:
            choices = {enum.value: enum for enum in self.choices}

            if value in choices:
                value = choices[value]
            else:
                raise ValidationError(
                    f"Invalid value '{value}' for given choices for field '{_field_name}'"
                    if _field_name
                    else f"Invalid value '{value}' for given choices"
                )

        for validator in self.validators:
            validator(value)

        return value

    @abstractproperty
    def python_type(self):
        """Return the corresponding python type."""


class StrField(Field):

    python_type = str

    def clean(self, value, **kwargs):
        if value is not None:
            try:
                value = str(value)
            except (ValueError, TypeError) as err:
                raise ValidationError(err)
            value = value.strip()

        value = super().clean(value, **kwargs)

        return value


class IntField(Field):

    python_type = int

    def clean(self, value, **kwargs):
        if value is not None:
            try:
                value = int(value)
            except (ValueError, TypeError) as err:
                raise ValidationError(err)

        value = super().clean(value, **kwargs)

        return value


class PositiveIntField(IntField):
    def clean(self, value, _field_name: typing.Optional[str] = None):
        value: int = super().clean(value, _field_name=_field_name)

        if value is not None and value < 0:
            raise ValidationError(
                f"Value must not be smaller than zero in field '{_field_name}'."
                if _field_name
                else "Value must not be smaller than zero."
            )

        return value


class BoolField(Field):

    python_type = bool

    def clean(self, value, **kwargs):
        if value is not None:
            try:
                value = bool(value)
            except ValueError as err:
                raise ValidationError(err)

        value = super().clean(value, **kwargs)

        return value


class StrIntField(Field):

    field = None
    python_type = None

    def clean(self, value, **kwargs):
        errs = []
        try:
            field = IntField(
                description=self.description,
                default=self.default,
                nullable=self.nullable,
                choices=self.choices,
                readonly=self.readonly,
                validators=self.validators,
                is_id_field=self.is_id_field,
            )
            value = field.clean(value, **kwargs)
            self.field = field
            self.python_type = int

            return value
        except ValidationError as err:
            errs.append(err)

        try:
            field = StrField(
                description=self.description,
                default=self.default,
                nullable=self.nullable,
                choices=self.choices,
                readonly=self.readonly,
                validators=self.validators,
                is_id_field=self.is_id_field,
            )
            value = field.clean(value, **kwargs)
            self.field = field
            self.python_type = str

            return value
        except ValidationError as err:
            errs.append(err)

        raise ValidationError(errs)


class ListField(Field):
    def __init__(
        self,
        child_fields: typing.List[Field],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.child_fields = child_fields
        # inherit arguments to child fields:

        for child_field in child_fields:
            if child_field.default == EmptyParameter:
                child_field.default = self.default

            if child_field.choices is None:
                child_field.choices = self.choices
            child_field.readonly |= self.readonly
            child_field.validators.extend(self.validators)

    def clean(self, value, _field_name: typing.Optional[str] = None):
        if not isinstance(value, Iterable):
            raise ValidationError(
                f"Value for field '{_field_name}' is not iterable."
                if _field_name
                else "Value is not iterable."
            )

        def clean_subvalue(value, **kwargs):
            validation_errors = []

            for child_field in self.child_fields:
                try:
                    return child_field.clean(value, **kwargs)
                except ValidationError as err:
                    validation_errors.append(err)

            raise ValidationError(validation_errors)

        value = [clean_subvalue(entry, _field_name=_field_name) for entry in value]

        return value


class DateField(Field):

    python_type = date

    def clean(self, value, **kwargs):
        if value is None:
            pass
        elif isinstance(value, date):
            pass
        elif isinstance(value, str):
            value = date.fromisoformat(value)
        elif isinstance(value, int):
            value = date.fromtimestamp(value)
        else:
            ValidationError(value)

        value = super().clean(value, **kwargs)

        return value


class DateTimeField(Field):

    python_type = datetime

    def clean(self, value, **kwargs):
        if value is None:
            pass
        elif isinstance(value, datetime):
            pass
        elif isinstance(value, str):
            value = datetime.fromisoformat(value)
        elif isinstance(value, int):
            value = datetime.fromtimestamp(value)
        else:
            ValidationError(value)

        value = super().clean(value, **kwargs)

        return value
