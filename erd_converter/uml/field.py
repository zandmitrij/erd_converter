from __future__ import annotations

import abc
import dataclasses
import re
import typing as tp

from typing_extensions import Self
from erd_converter.base import BaseField, Field, IntegerField, VarcharField


FIELD_PATTERN = re.compile(r'^\s*([a-zA-Z_]\w*)\s+(\w+(?:\(\d+\))?(?:\[\w+\])?)\s*(?:\[(.*?)\])?\s*$')


T = tp.TypeVar('T')


class _BaseUMLField(BaseField[T]):

    @abc.abstractclassmethod
    def from_parsed_str(cls, name: str, data: str, options: str) -> Self:
        ...


def get_nullable(options: list[str]) -> bool:
    if 'null' in options:
        return True
    if 'not null' in options:
        return False
    return False


DEFAULT_VARCHAR_SIZE = 256


def parse_size(data: str) -> int:
    match = re.match(r'^varchar(?:\((\d+)\))?$', data)
    if not match:
        return DEFAULT_VARCHAR_SIZE
    size = match.group(1)
    return int(size) if size else DEFAULT_VARCHAR_SIZE


@dataclasses.dataclass
class UMLVarcharField(_BaseUMLField[VarcharField]):
    name: str
    size: int
    primary_key: bool = False
    nullable: bool = False

    @classmethod
    def from_parsed_str(cls, name: str, data: str, options: str | None) -> Self:
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
        return f'{self.name} {self.type}{size}{options}'


@dataclasses.dataclass
class UMLIntegerField(_BaseUMLField[IntegerField]):
    name: str
    primary_key: bool = False
    nullable: bool = False

    @classmethod
    def from_parsed_str(cls, name: str, options: str | None) -> Self:
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
class UMLBooleanField(_BaseUMLField[IntegerField]):
    name: str
    primary_key: bool = False
    nullable: bool = False

    @classmethod
    def from_parsed_str(cls, name: str, options: str | None) -> Self:
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
class UMLForeignKeyField(_BaseUMLField):
    name: str
    type: str
    ref_table: str
    ref_operator: str
    ref_field: str
    primary_key: bool = False
    nullable: bool = False

    @classmethod
    def from_parsed_str(cls, name: str, data: str, options: str) -> Self:
        options_split = [x.lower() for x in options.split(', ')]
        print(options)
        primary_key = 'pk' in options_split
        nullable = get_nullable(options_split)
        ref_table, ref_field, ref_operator = get_ref(options_split)
        return cls(
            name=name,
            type=data,
            ref_table=ref_table,
            ref_operator=ref_operator,
            ref_field=ref_field,
            primary_key=primary_key,
            nullable=nullable,
        )

    def __str__(self) -> str:
        return ''


class UMLArrayField(_BaseUMLField):
    @classmethod
    def from_parsed_str(cls, name, data, options) -> Self:
        ...


class UMLJsonField(_BaseUMLField):
    @classmethod
    def from_parsed_str(cls, name, data, options) -> Self:
        ...



def create_uml_field(line: str):
    field_matches = re.finditer(FIELD_PATTERN, line)
    try:
        match = next(field_matches)
    except StopIteration:
        raise ValueError(f'Invalid line {line}')
    
    name, data, options = match.groups()

    if options is not None and 'ref:' in options:
        return UMLForeignKeyField.from_parsed_str(name, data, options)

    if data.startswith('int'):
        return UMLIntegerField.from_parsed_str(name, options)

    if data.startswith('boolean'):
        return UMLBooleanField.from_parsed_str(name, options)

    if data.startswith('varchar'):
        return UMLVarcharField.from_parsed_str(name, data, options)

    if data.startswith('array'):
        return UMLArrayField.from_parsed_str(name, data, options)

    if data.startswith('json'):
        return UMLJsonField.from_parsed_str()
    raise NotImplementedError()
    # if not options:
    #     return cls(name=name, type=data)

    # options_split = [x.lower() for x in options.split(',')]
    # primary_key = 'pk' in options_split
    # nullable = 'null' in options_split

    # return cls(
    #     name=name,
    #     type=data_type,
    #     size=field_size,
    #     primary_key=primary_key,
    #     nullable=nullable,
    #     reference=reference,
    # )


class UMLField(BaseField):
    name: str
    type: str
    size: int | None = None
    primary_key: bool = False
    nullable: bool = False
    reference: str | None = None

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