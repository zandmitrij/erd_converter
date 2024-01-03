from __future__ import annotations

import abc
import dataclasses

from typing_extensions import Self

from .field import Field


@dataclasses.dataclass
class Table:
    name: str
    fields: list[Field] = dataclasses.field(default_factory=lambda: [])


class BaseTable(abc.ABC):
    @abc.abstractmethod
    def to_table(self) -> Table:
        """Abstract method to implement to get Field instance from your custom class

        Returns:
            Field: field class instance
        """
        ...

    @abc.abstractclassmethod
    def from_table(field: Table) -> Self:
        """Abstract method to implement to get your custom class from Field instance

        Args:
            field (Field): field class instance

        Returns:
            Self: your class
        """
        ...
