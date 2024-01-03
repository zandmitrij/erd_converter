from pathlib import Path

from erd_converter.iterators import UMLIterator
from erd_converter.table import UMLTable


def test_iterator():
    filepath = Path(__file__).parent / 'experiment.uml'

    with UMLIterator(filepath) as uml:
        table = next(uml)
        assert isinstance(table, UMLTable)