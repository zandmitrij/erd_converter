from __future__ import annotations

import pytest

from erd_converter.uml.field import UMLIntegerField, create_uml_field, UMLVarcharField, UMLForeignKeyField
from erd_converter.peewee.field import PeeweeIntegerField


@pytest.mark.parametrize(
    argnames=['inp', 'out'],
    argvalues=[
        ('id int [pk]', 'id = AutoField()'),
        ('foo int [null]', 'foo = IntegerField(null=True)'),
        ('foo int [not null]', 'foo = IntegerField()'),
    ],
)
def test_convert_uml_field_to_peewee(inp, out):
    field = create_uml_field(inp).to_field()
    peewee_field = PeeweeIntegerField.from_field(field)
    assert str(peewee_field) == out
