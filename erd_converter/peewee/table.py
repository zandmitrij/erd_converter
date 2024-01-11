from __future__ import annotations

import dataclasses
import typing as tp

from erd_converter import base as bf
from . import field as peewee_field
from . import utils


@dataclasses.dataclass
class PeeweeTable(bf.BaseTable):
    name: str
    fields: list[peewee_field.PeeweeField] = dataclasses.field(default_factory=lambda: [])
    field_convert: tp.ClassVar[dict] = {
        bf.Integer: peewee_field.PeeweeIntegerField,
        bf.Varchar: peewee_field.PeeweeVarcharField,
        bf.ForeignKeyField: peewee_field.PeeweeForeignKeyField,
        bf.Array: peewee_field.PeeweeArrayField,
        bf.Boolean: peewee_field.PeeweeBooleanField,
        bf.Json: peewee_field.PeeweeJsonField,
        bf.DateTime: peewee_field.PeeweeDateTimeField,
        bf.Float: peewee_field.PeeweeFloatField,
        bf.Bytes: peewee_field.PeeweeBytesField,
    }

    def __str__(self) -> str:
        table_name = utils.get_peewee_table_class_name(self.name)
        res = f'\nclass {table_name}(BaseModel):\n'
        for field in self.fields:
            res += f'    {field}\n'
        res += '\n'
        res += '    class Meta:\n'
        res += f"        db_table = '{self.name}'\n\n"
        return res
