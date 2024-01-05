from __future__ import annotations

import dataclasses
import typing as tp

from typing_extensions import Self

from erd_converter.base import BaseTable, Table, IntegerField, VarcharField
from .field import BasePeeweeField, PeeweeIntegerField, PeeweeVarcharField
from .utils import get_peewee_table_class_name


@dataclasses.dataclass
class PeeweeTable(BaseTable):
    name: str
    fields: list[BasePeeweeField] = dataclasses.field(default_factory=lambda: [])
    field_convert: tp.ClassVar[dict] = {
        IntegerField: PeeweeIntegerField,
        VarcharField: PeeweeVarcharField,
    }

    def to_table(self) -> Table:
        return Table(name=self.name, fields=[field.to_field() for field in self.fields])

    @classmethod
    def from_table(cls, table: Table) -> Self:
        fields = []
        for field in table.fields:
            f = cls.field_convert[field.__class__].from_field(field)
            fields.append(f)
        return cls(name=table.name, fields=fields)

    def __str__(self) -> str:
        table_name = get_peewee_table_class_name(self.name)
        res = f'\nclass {table_name}(BaseModel):\n'
        for field in self.fields:
            res += f'    {field}\n'
        res += '\n'
        res += '    class Meta:\n'
        res += f"        db_table = '{self.name}'\n\n"
        return res
