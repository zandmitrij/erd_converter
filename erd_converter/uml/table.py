from __future__ import annotations

import dataclasses
import typing as tp

from typing_extensions import Self

from erd_converter import base
from . import field as f


@dataclasses.dataclass
class UMLTable(base.BaseTable):
    name: str
    fields: list[f.UMLField] = dataclasses.field(default_factory=lambda: [])
    # TODO: add field_convert_dict
    field_convert = {}

    @classmethod
    def from_str(cls, lines: tp.Iterable[str]) -> Self:
        lines = iter(lines)
        first_line = next(lines).strip()
        if not first_line.startswith('table') or not first_line.endswith('{'):
            raise ValueError(f'Incorrect firstline in table {first_line}')
        try:
            _, table_name, _ = first_line.split()
        except ValueError:
            raise ValueError(f'Incorrect line {first_line}')
        table = cls(table_name)
        for line in lines:
            line = line.strip()
            if line == '}':                
                return table
            field = f.create_uml_field(line)
            table.fields.append(field)
