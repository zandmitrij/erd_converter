from __future__ import annotations

import typing as tp
from pathlib import Path

from .table import UMLTable


class UMLIterator(tp.Iterator[UMLTable]):
    def __init__(self, filepath: Path) -> None:
        self.__filepath = filepath

    def __enter__(self) -> UMLIterator:
        self.__file = open(self.__filepath, 'r')
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if not self.__file.closed:
            self.__file.close()

    def __iter__(self) -> tp.Iterator[UMLTable]:
        return self

    def __next__(self) -> UMLTable:
        lines = []
        while True:
            try:
                line = next(self.__file)
            except StopIteration:
                raise StopIteration()
            if not line.strip() or line.startswith('//'):
                continue
            elif line.strip() == '}':
                lines.append(line)
                return UMLTable.from_str(lines)
            lines.append(line)
