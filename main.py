from __future__ import annotations

import typing as tp
from pathlib import Path

import typer

from erd_converter.peewee.table import PeeweeTable
from erd_converter.uml.iterator import UMLIterator


def iterate_tables_from_uml_file(file: Path) -> tp.Iterator[str] :
    with UMLIterator(file) as uml:
        for table in uml:
            peewee_table = PeeweeTable.from_table(table.to_table())
            yield str(peewee_table)
    

def main(
    file: Path = typer.Option(..., exists=True, dir_okay=False, readable=True),
    res_file: Path = typer.Option(..., exists=False),
) -> None:

    with open(res_file, 'w') as wf:
        wf.writelines(iterate_tables_from_uml_file(file))


if __name__ == "__main__":
    typer.run(main)
