from __future__ import annotations

import abc
import dataclasses
import typing as tp

from typing_extensions import Self


T = tp.TypeVar('T')


class BaseField(abc.ABC, tp.Generic[T]):
    
    @classmethod
    def model_type(cls) -> type[T]:
        return tp.get_args(cls.__orig_bases__[0])[0]

    def to_field(self) -> T:
        model_type = self.model_type()
        return model_type(**dataclasses.asdict(self))

    @classmethod
    def from_field(cls, field: T) -> Self:
        return cls(**dataclasses.asdict(field))

    @abc.abstractclassmethod
    def from_str(cls, line: str) -> Self:
        ...
