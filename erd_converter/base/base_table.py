from __future__ import annotations

import abc
import typing as tp

from typing_extensions import Self

from .table import Table
from .base_field import BaseField
from .field import Field


T = tp.TypeVar('T', bound=Field)
F = tp.TypeVar('F', bound=BaseField)


class BaseTable(abc.ABC):
    name: str
    fields: list[F]
    field_convert: tp.ClassVar[dict[type[T], type[F]]]

    def to_table(self) -> Table:
        return Table(name=self.name, fields=[field.to_field() for field in self.fields])

    @classmethod
    def __convert_field(cls, field: Field) -> F:
        return cls.field_convert[field.__class__].from_field(field)

    @classmethod
    def from_table(cls, table: Table) -> Self:
        return cls(name=table.name, fields=[cls.__convert_field(field) for field in table.fields])
