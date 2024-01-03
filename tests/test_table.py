from __future__ import annotations

import pytest

from pathlib import Path

from erd_converter.table import UMLTable
from erd_converter.field import UMLField


@pytest.fixture
def table_experiment() -> list[str]:
    filepath = Path(__file__).parent / 'experiment.uml'
    lines = []
    with open(filepath, 'r') as f:
        for line in f:
            lines.append((line.strip()))
    return lines


def test_creating_uml_table_from_str(table_experiment):
    table = UMLTable.from_str(table_experiment)
    assert isinstance(table, UMLTable)
    assert table.name == 'experiment'
    assert len(table.fields) == 2
    assert all(isinstance(field, UMLField) for field in table.fields)
