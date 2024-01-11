from __future__ import annotations

import dataclasses
import typing as tp

from typing_extensions import Self

from erd_converter import base as bf
from . import utils


T = tp.TypeVar('T')


class PeeweeField(bf.BaseField[T]):
    name: str
    options: str
    field_type: tp.ClassVar[str]

    @classmethod
    def from_str(cls, line: str) -> Self:
        raise NotImplementedError

    def __str__(self) -> str:
        return f'{self.name} = {self.field_type}({self.options})'


@dataclasses.dataclass
class PeeweeIntegerField(PeeweeField[bf.Integer]):
    name: str
    primary_key: bool = False
    nullable: bool = False
    field_type: tp.ClassVar[str] = 'IntegerField'

    @property
    def options(self) -> str:
        options = []
        if self.nullable:
            options.append('null=True')
        return ', '.join(options)

    def __str__(self) -> str:
        field_type = 'AutoField' if self.primary_key else self.field_type
        return f'{self.name} = {field_type}({self.options})'


@dataclasses.dataclass
class PeeweeFloatField(PeeweeField[bf.Float]):
    name: str
    primary_key: bool = False
    nullable: bool = False
    field_type: tp.ClassVar[str] = 'FloatField'

    @property
    def options(self) -> str:
        options = []
        if self.nullable:
            options.append('null=True')
        return ', '.join(options)


@dataclasses.dataclass
class PeeweeVarcharField(PeeweeField[bf.Varchar]):
    name: str
    size: int
    primary_key: bool = False
    nullable: bool = False
    field_type: tp.ClassVar[str] = 'CharField'

    @property
    def options(self) -> str:
        options = []
        if self.size != 256:
            options.append(f'max_length={self.size}')
        if self.nullable:
            options.append('null=True')
        return ', '.join(options)


@dataclasses.dataclass
class PeeweeBooleanField(PeeweeField[bf.Boolean]):
    name: str
    nullable: bool = False
    field_type: tp.ClassVar[str] = 'BooleanField'

    @property
    def options(self) -> str:
        options = []
        if self.nullable:
            options.append('null=True')
        return ', '.join(options)


@dataclasses.dataclass
class PeeweeDateTimeField(PeeweeField[bf.DateTime]):
    name: str
    nullable: bool = False
    field_type: tp.ClassVar[str] = 'DateTimeField'

    @property
    def options(self) -> str:
        options = []
        if self.nullable:
            options.append('null=True')
        return ', '.join(options)


@dataclasses.dataclass
class PeeweeForeignKeyField(PeeweeField[bf.ForeignKeyField]):
    name: str
    type: str
    ref_table: str
    ref_operator: str
    ref_field: str
    nullable: bool = False
    lazy_load: bool = False
    field_type: tp.ClassVar[str] = 'ForeignKeyField'

    @property
    def options(self) -> str:
        ref_table = utils.get_peewee_table_class_name(self.ref_table)
        return ', '.join((ref_table, f"field='{self.ref_field}'", f'lazy_load={self.lazy_load}'))


@dataclasses.dataclass
class PeeweeArrayField(PeeweeField[bf.Array]):
    name: str
    subfield: PeeweeIntegerField | PeeweeVarcharField | PeeweeBooleanField
    field_type: tp.ClassVar[str] = 'ArrayField'
    field_convert = {
        bf.Integer: PeeweeIntegerField,
        bf.Varchar: PeeweeVarcharField,
        bf.Boolean: PeeweeBooleanField,
    }

    @property
    def _options(self) -> str:
        return ''

    @property
    def field_kwargs(self) -> dict:
        kw = {}
        if not self.subfield.nullable:
            kw['null'] = False
        return kw

    @property
    def options(self) -> str:
        options = [self.subfield.field_type]
        if (kw := self.field_kwargs):
            options.append(f'field_kwargs={kw}')
        if self._options:
            options.append(self._options)
        options.append('index=False')
        return ', '.join(options)

    def to_field(self) -> bf.Array:
        subfield = self.subfield.to_field()
        return bf.Array(name=self.name, subfield=subfield)

    @classmethod
    def __convert_field(cls, field: bf.Integer | bf.Varchar | bf.Boolean) -> PeeweeIntegerField | PeeweeBooleanField | PeeweeVarcharField:
        return cls.field_convert[field.__class__].from_field(field)

    @classmethod
    def from_field(cls, field: bf.Array) -> Self:
        subfield = cls.__convert_field(field.subfield)
        return cls(name=field.name, subfield=subfield)


@dataclasses.dataclass
class PeeweeJsonField(PeeweeField[bf.Json]):
    name: str
    nullable: bool = False
    field_type: tp.ClassVar[str] = 'JSONField'

    @property
    def options(self) -> str:
        options = []
        options.append('dumps=functools.partial(json.dumps, ensure_ascii=False)')
        if self.nullable:
            options.append('null=True')
        return ', '.join(options)


@dataclasses.dataclass
class PeeweeBytesField(PeeweeField[bf.Bytes]):
    name: str
    nullable: bool = False
    field_type: tp.ClassVar[str] = 'BlobField'

    @property
    def options(self) -> str:
        options = []
        if self.nullable:
            options.append('null=True')
        return ', '.join(options)        
