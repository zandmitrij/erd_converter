from __future__ import annotations

import dataclasses
import re

from typing_extensions import Self
from erd_converter.base import BaseField, Field


@dataclasses.dataclass
class UMLField(BaseField):
    name: str
    type: str
    primary_key: bool = False
    nullable: bool = False
    reference: str | None = None

    @classmethod
    def from_str(cls, line: str) -> Self:
        field_matches = re.finditer(r'^\s*([a-zA-Z_]\w*)\s+(\w+)\s*(?:\[(.*?)\])?$', line)
        try:
            match = next(field_matches)
        except StopIteration:
            raise ValueError(f'Invalid line {line}')
        name, data_type, options = match.groups()

        if not options:
            return cls(name=name, type=data_type)

        options_split = [x.lower() for x in options.split(',')]
        primary_key = 'pk' in options_split
        nullable = 'null' in options_split

        reference_match = re.search(r'ref:\s*-\s*(\w+\.\w+)', options)
        reference = reference_match.group(1) if reference_match else None
        return cls(
            name=name,
            type=data_type,
            primary_key=primary_key,
            nullable=nullable,
            reference=reference,
        )

    def to_field(self) -> Field:
        return Field(
            name=self.name,
            type=self.type,
            primary_key=self.primary_key,
            nullable=self.nullable,
            reference=self.reference,
        )

    @classmethod
    def from_field(cls, field: Field) -> Self:
        return cls(
            name=field.name,
            type=field.type,
            primary_key=field.primary_key,
            nullable=field.nullable,
            reference=field.reference,
        )
