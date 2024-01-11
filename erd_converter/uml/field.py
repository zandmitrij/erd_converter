from __future__ import annotations

import abc
import dataclasses
import re
import typing as tp

from typing_extensions import Self
from erd_converter import base as bf

from .utils import get_data_type, get_nullable


FIELD_PATTERN = re.compile(r'^\s*([a-zA-Z_]\w*)\s+(\w+(?:\(\d+\))?(?:\[\w+\])?)\s*(?:\[(.*?)\])?\s*$')


T = tp.TypeVar('T')


class UMLField(bf.BaseField[T]):
    pass


DEFAULT_VARCHAR_SIZE = 256


def parse_size(data: str) -> int:
    match = re.match(r'^varchar(?:\((\d+)\))?$', data)
    if not match:
        return DEFAULT_VARCHAR_SIZE
    size = match.group(1)
    return int(size) if size else DEFAULT_VARCHAR_SIZE


@dataclasses.dataclass
class UMLVarcharField(UMLField[bf.Varchar]):
    name: str
    size: int
    primary_key: bool = False
    nullable: bool = False

    @classmethod
    def from_str(cls, line: str) -> Self:
        match = re.search(FIELD_PATTERN, line)
        
        if not match:
            raise ValueError(f'Invalid line {line}')

        name, data, options = match.groups()
    
        size = parse_size(data)

        if not options:
            return cls(name, size=size)
        
        options_split = [x.lower() for x in options.split(',')]
        primary_key = 'pk' in options_split
        nullable = get_nullable(options_split)
        return cls(name, size=size, primary_key=primary_key, nullable=nullable)

    def __str__(self) -> str:
        options = ''
        if self.nullable:
            options += 'null'
        elif self.primary_key:
            options += 'pk'
        if options:
            options = f' [{options}]'

        size = '' if self.size == 256 else f'({self.size})' 
        return f'{self.name} varchar{size}{options}'


@dataclasses.dataclass
class UMLIntegerField(UMLField[bf.Integer]):
    name: str
    primary_key: bool = False
    nullable: bool = False

    @classmethod
    def from_str(cls, line: str) -> Self:
        match = re.search(FIELD_PATTERN, line)
        
        if not match:
            raise ValueError(f'Invalid line {line}')

        name, _, options = match.groups()
    
        if options is None:
            return cls(name)

        options_split = [x.lower() for x in options.split(',')]
        primary_key = 'pk' in options_split
        nullable = get_nullable(options_split)

        return cls(name=name, primary_key=primary_key, nullable=nullable)

    def __str__(self) -> str:
        options = ''
        if self.nullable:
            options += 'null'
        elif self.primary_key:
            options += 'pk'
        if options:
            options = f' [{options}]'
        return f'{self.name} int{options}'


@dataclasses.dataclass
class UMLBooleanField(UMLField[bf.Boolean]):
    name: str
    nullable: bool = False

    @classmethod
    def from_str(cls, line: str) -> Self:
        match = re.search(FIELD_PATTERN, line)
        
        if not match:
            raise ValueError(f'Invalid line {line}')

        name, _, options = match.groups()
    
        if options is None:
            return cls(name)

        options_split = [x.lower() for x in options.split(',')]
        nullable = get_nullable(options_split)

        return cls(name=name, nullable=nullable)

    def __str__(self) -> str:
        options = ''
        if self.nullable:
            options += 'null'
        elif self.primary_key:
            options += 'pk'
        if options:
            options = f' [{options}]'
        return f'{self.name} boolean{options}'


def parse_ref(s: str) -> tuple[str, str, str]:
    match = re.match(r'^ref:\s*([<>-])\s*([a-zA-Z_][a-zA-Z0-9_.]*)$', s)
    if not match:
        raise ValueError(f'incorrect ref:{s}')
    operator = match.group(1)
    identifier = match.group(2)
    table, field = identifier.split('.')
    return table, field, operator


def get_ref(options: list[str]) -> tuple[str, str, str]:
    try:
        ref = next(opt for opt in options if 'ref:' in opt)
    except StopIteration:
        raise ValueError('ref not in options')
    return parse_ref(ref)


@dataclasses.dataclass
class UMLForeignKeyField(UMLField[bf.ForeignKeyField]):
    name: str
    type: str
    ref_table: str
    ref_operator: str
    ref_field: str
    nullable: bool = False

    @classmethod
    def from_str(cls, line: str) -> Self:
        match = re.search(FIELD_PATTERN, line)
        
        if not match:
            raise ValueError(f'Invalid line {line}')

        name, data_type, options = match.groups()
        
        options_split = [x.lower() for x in options.split(', ')]
        nullable = get_nullable(options_split)
        ref_table, ref_field, ref_operator = get_ref(options_split)
        return cls(
            name=name,
            type=data_type,
            ref_table=ref_table,
            ref_operator=ref_operator,
            ref_field=ref_field,
            nullable=nullable,
        )

    def __str__(self) -> str:
        return ''


ARRAY_FIELD_PATTERN = re.compile(r'^\s*(?P<variable_name>[a-zA-Z_]\w*)\s+(?P<data_type>\w+(?:\(\d+\))?)\s*(?:\[(?P<values>.*?)\])?\s*(?:\[(?P<options>[\w\s,]+)\])?\s*$')


@dataclasses.dataclass
class UMLArrayField(UMLField[bf.Array]):
    name: str
    subfield: UMLIntegerField | UMLBooleanField | UMLVarcharField 
    field_convert = {
        bf.Integer: UMLIntegerField,
        bf.Varchar: UMLVarcharField,
        bf.Boolean: UMLBooleanField,
    }

    @classmethod
    def __convert_field(cls, field: bf.Integer | bf.Varchar | bf.Boolean) -> UMLIntegerField | UMLBooleanField | UMLVarcharField:
        return cls.field_convert[field.__class__].from_field(field)

    def to_field(self) -> bf.Array:
        subfield = self.subfield.to_field()
        return bf.Array(name=self.name, subfield=subfield)

    @classmethod
    def from_field(cls, field: bf.Array) -> Self:
        subfield = cls.__convert_field(field.subfield)
        return cls(name=field.name, subfield=subfield)

    @classmethod
    def from_str(cls, line: str) -> Self:
        match = re.search(ARRAY_FIELD_PATTERN, line)
        
        if not match:
            raise ValueError(f'Invalid line {line}')

        name, _, subfield, options = match.groups()

        subfield_ = create_uml_field(f'default {subfield}')

        return cls(name=name, subfield=subfield_)


@dataclasses.dataclass
class UMLJsonField(UMLField[bf.Json]):
    name: str
    nullable: bool = False

    @classmethod
    def from_str(cls, line: str) -> Self:
        match = re.search(FIELD_PATTERN, line)

        if not match:
            raise ValueError(f'Invalid line {line}')

        name, _, options = match.groups()
    
        if options is None:
            return cls(name)

        options_split = [x.lower() for x in options.split(',')]
        nullable = get_nullable(options_split)

        return cls(name=name, nullable=nullable)


@dataclasses.dataclass
class UMLDateTimeField(UMLField[bf.DateTime]):
    name: str
    nullable: bool = False

    @classmethod
    def from_str(cls, line: str) -> Self:
        match = re.search(FIELD_PATTERN, line)

        if not match:
            raise ValueError(f'Invalid line {line}')

        name, _, options = match.groups()
    
        if options is None:
            return cls(name)

        options_split = [x.lower() for x in options.split(',')]
        nullable = get_nullable(options_split)

        return cls(name=name, nullable=nullable)


@dataclasses.dataclass
class UMLFloatField(UMLField[bf.Float]):
    name: str
    nullable: bool = False

    @classmethod
    def from_str(cls, line: str) -> Self:
        match = re.search(FIELD_PATTERN, line)

        if not match:
            raise ValueError(f'Invalid line {line}')

        name, _, options = match.groups()
    
        if options is None:
            return cls(name)

        options_split = [x.lower() for x in options.split(',')]
        nullable = get_nullable(options_split)

        return cls(name=name, nullable=nullable)


@dataclasses.dataclass
class UMLBytesField(UMLField[bf.Bytes]):
    name: str
    nullable: bool = False

    @classmethod
    def from_str(cls, line: str) -> Self:
        match = re.search(FIELD_PATTERN, line)

        if not match:
            raise ValueError(f'Invalid line {line}')

        name, _, options = match.groups()
    
        if options is None:
            return cls(name)

        options_split = [x.lower() for x in options.split(',')]
        nullable = get_nullable(options_split)

        return cls(name=name, nullable=nullable)


DATA_TYPES : dict[str, UMLField] = {
    'varchar': UMLVarcharField,
    'int': UMLIntegerField,
    'array': UMLArrayField,
    'json': UMLJsonField,
    'fk': UMLForeignKeyField,
    'boolean': UMLBooleanField,
    'datetime': UMLDateTimeField,
    'float': UMLFloatField,
    'bytea': UMLBytesField,
}


def create_uml_field(line: str):
    data_type = get_data_type(line)

    try:
        dtype = DATA_TYPES[data_type]
    except KeyError:
        raise ValueError(f'Cannot find datatype `{data_type}`')
    return dtype.from_str(line)
