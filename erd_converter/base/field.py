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
class IntegerField:
    name: str
    primary_key: bool = False
    nullable: bool = False


@dataclasses.dataclass
class VarcharField:
    name: str
    size: int
    primary_key: bool = False
    nullable: bool = False
