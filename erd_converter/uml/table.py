from __future__ import annotations

import dataclasses
import typing as tp

from typing_extensions import Self

from .field import UMLField
from erd_converter.base import BaseTable, Table


@dataclasses.dataclass
class UMLTable(BaseTable):
    name: str
    fields: list[UMLField] = dataclasses.field(default_factory=lambda: [])

    def to_table(self) -> Table:
        return Table(name=self.name, fields=[field.to_field() for field in self.fields])

    @classmethod
    def from_table(cls, table: Table) -> Self:
        return cls(name=table.name, fields=[UMLField.from_field(field) for field in table.fields])

    @classmethod
    def from_str(cls, lines: tp.Iterable[str]) -> Self:
        lines = iter(lines)
        first_line = next(lines).strip()
        if not first_line.startswith('table') or not first_line.endswith('{'):
            raise ValueError(f'Incorrect firstline in table {first_line}')
        _, table_name, _ = first_line.split()
        table = cls(table_name)
        for line in lines:
            line = line.strip()
            if line == '}':                
                return table
            field = UMLField.from_str(line)
            table.fields.append(field)
