from __future__ import annotations

import pytest

from erd_converter.uml.field import UMLIntegerField, create_uml_field, UMLVarcharField, UMLForeignKeyField
from erd_converter.peewee.field import PeeweeIntegerField, PeeweeForeignKeyField, PeeweeArrayField, PeeweeBov


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


@pytest.mark.parametrize(
    argnames=['inp', 'out'],
    argvalues=[
        ('entity_id int [ref: > experiment_entity.id]', "entity_id = ForeignKeyField(ExperimentEntity, field='id', lazy_load=False)"),
    ],
)
def test_convert_uml_fk_field_to_peewee(inp, out):
    field = create_uml_field(inp).to_field()
    peewee_field = PeeweeForeignKeyField.from_field(field)
    assert str(peewee_field) == out



@pytest.mark.parametrize(
    argnames=['inp', 'out'],
    argvalues=[
        ('entity_id int [ref: > experiment_entity.id]', "entity_id = ForeignKeyField(ExperimentEntity, field='id', lazy_load=False)"),
    ],
)
def test_convert_uml_bool_field_to_peewee(inp, out):
    field = create_uml_field(inp).to_field()
    peewee_field = PeeweeForeignKeyField.from_field(field)
    assert str(peewee_field) == out


@pytest.mark.parametrize(
    argnames=['inp', 'out'],
    argvalues=[
        ('dependents array[varchar(512)]', "dependents = ArrayField(CharField, field_args={})")
    ],
)
def test_convert_uml_array_field_to_peewee(inp, out):
    field = create_uml_field(inp).to_field()
    peewee_field = PeeweeArrayField.from_field(field)
    assert str(peewee_field) == out
