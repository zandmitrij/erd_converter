from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class Field:
    name: str
    type: str
    primary_key: bool = False
    nullable: bool = False
    reference: str | None = None


@dataclasses.dataclass
class Integer:
    name: str
    primary_key: bool = False
    nullable: bool = False


@dataclasses.dataclass
class Varchar:
    name: str
    size: int
    primary_key: bool = False
    nullable: bool = False


@dataclasses.dataclass
class ForeignKeyField:
    name: str
    type: str
    ref_table: str
    ref_operator: str
    ref_field: str
    nullable: bool = False


@dataclasses.dataclass
class Boolean:
    name: str
    nullable: bool = False


@dataclasses.dataclass
class Float:
    name: str
    nullable: bool = False


@dataclasses.dataclass
class Bytes:
    name: str
    nullable: bool = False


@dataclasses.dataclass
class DateTime:
    name: str
    nullable: bool = False


@dataclasses.dataclass
class Array:
    name: str
    subfield: Integer | Boolean | Varchar


@dataclasses.dataclass
class Json:
    name: str
    nullable: bool = False
