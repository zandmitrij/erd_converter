from __future__ import annotations

import dataclasses

from typing_extensions import Self

from erd_converter.base import BaseTable, Table
from .field import PeeweeField
from .utils import get_peewee_table_class_name


@dataclasses.dataclass
class PeeweeTable(BaseTable):
    name: str
    fields: list[PeeweeField] = dataclasses.field(default_factory=lambda: [])

    def to_table(self) -> Table:
        return Table(name=self.name, fields=[field.to_field() for field in self.fields])

    @classmethod
    def from_table(cls, table: Table) -> Self:
        return cls(name=table.name, fields=[PeeweeField.from_field(field) for field in table.fields])

    def __str__(self) -> str:
        table_name = get_peewee_table_class_name(self.name)
        res = f'\nclass {table_name}(BaseModel):\n'
        for field in self.fields:
            res += f'    {field}\n'
        res += '\n'
        res += '    class Meta:\n'
        res += f"        db_table = '{self.name}'\n\n"
        return res
