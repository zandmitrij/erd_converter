from __future__ import annotations

import dataclasses

from typing_extensions import Self

from erd_converter.base import BaseField, Field
from .utils import get_peewee_table_class_name


@dataclasses.dataclass
class PeeweeField(BaseField):
    name: str
    type: str
    primary_key: bool = False
    nullable: bool = False
    reference: str | None = None

    def to_field(self) -> Field:
        return NotImplemented()

    @classmethod
    def from_field(cls, field: Field) -> Self:
        return cls(
            name=field.name,
            type=field.type,
            primary_key=field.primary_key,
            nullable=field.nullable,
            reference=field.reference,
        )

    def get_peewee_type(self) -> str:
        if self.reference:
            return 'ForeignKeyField'
        if self.type == 'int':
            if self.primary_key:
                return 'AutoField'
            return 'IntegerField'
        if self.type == 'varchar':
            return 'CharField'
        if self.type == 'json':
            return 'JSONField'
        if self.type == 'boolean':
            return 'BooleanField'

    def get_peewee_field_definition(self) -> str:
        field_type = self.get_peewee_type()
        options = []

        if self.nullable:
            options.append('null=True')
        op = ','.join(options)
        if field_type == 'ForeignKeyField':
            ref_table, ref_field = self.reference.split('.')
            ref_table_name = get_peewee_table_class_name(ref_table)
            op = f"field='{ref_field}', lazy_load=False, " + op
            return f'ForeignKeyField({ref_table_name}, {op})'

        return f'{field_type}({op})'

    def __str__(self) -> str:
        field_definition = self.get_peewee_field_definition()
        return f'{self.name} = {field_definition}'
