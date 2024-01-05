from __future__ import annotations

import abc

from typing_extensions import Self

from .table import Table


class BaseTable(abc.ABC):
    name: str
    fields: list

    def to_table(self) -> Table:
        """Abstract method to implement to get Field instance from your custom class

        Returns:
            Field: field class instance
        """
        return Table(name=self.name, fields=[field.to_field() for field in self.fields])


    @abc.abstractclassmethod
    def from_table(field: Table) -> Self:
        """Abstract method to implement to get your custom class from Field instance

        Args:
            field (Field): field class instance

        Returns:
            Self: your class
        """
        ...
