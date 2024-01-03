from __future__ import annotations

import abc
import dataclasses

from typing_extensions import Self


@dataclasses.dataclass
class Field:
    name: str
    type: str
    primary_key: bool = False
    nullable: bool = False
    reference: str | None = None


class BaseField(abc.ABC):
    @abc.abstractmethod
    def to_field(self) -> Field:
        """Abstract method to implement to get Field instance from your custom class

        Returns:
            Field: field class instance
        """
        ...

    @abc.abstractclassmethod
    def from_field(field: Field) -> Self:
        """Abstract method to implement to get your custom class from Field instance

        Args:
            field (Field): field class instance

        Returns:
            Self: your class
        """
        ...
