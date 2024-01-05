from __future__ import annotations

import pytest

from erd_converter.uml.field import UMLIntegerField, create_uml_field, UMLVarcharField, UMLForeignKeyField


@pytest.mark.parametrize(
    argnames=['line', 'res_params'],
    argvalues=[
        ('id int [pk]', ('id', 'int', True, False)),
        ('count int [not null]', ('count', 'int', False, False)),
        ('foo int [null]', ('foo', 'int', False, True)),
        ('bar int', ('bar', 'int', False, False)),
    ],
)
def test_uml_integer_field_from_str(line: str, res_params: tuple[str, str, bool, bool]):
    res = create_uml_field(line)

    assert isinstance(res, UMLIntegerField)
    
    name, res_type, is_pk, is_nullable = res_params
    assert res.name == name
    assert res.type == res_type
    assert res.primary_key == is_pk
    assert res.nullable == is_nullable


@pytest.mark.parametrize(
    argnames=['inp', 'out'],
    argvalues=[
        ('id int [pk]', 'id int [pk]'),
        ('count int [not null]', 'count int'),
        ('foo int [null]', 'foo int [null]'),
    ],
)
def test_integer_field_from_str_to_str(inp: str, out: str):
    res = str(create_uml_field(inp))
    assert res == out


@pytest.mark.parametrize(
    argnames=['line', 'res_params'],
    argvalues=[
        ('name varchar', ('name', 'varchar', 256, False, False)),
        ('description varchar(512)', ('description', 'varchar', 512, False, False)),
        ('description varchar(125) [null]', ('description', 'varchar', 125, False, True)),
        ('description varchar [not null]', ('description', 'varchar', 256, False, False)),
    ],
)
def test_create_uml_varchar_field_from_str(line: str, res_params: tuple[str, str, int, bool, bool]):
    res = create_uml_field(line)
    assert isinstance(res, UMLVarcharField)
    
    name, res_type, size, is_pk, is_null = res_params
    assert res.name == name
    assert res.type == res_type
    assert res.size == size
    assert res.primary_key == is_pk
    assert res.nullable == is_null


@pytest.mark.parametrize(
    argnames=['inp', 'out'],
    argvalues=[
        ('name varchar', 'name varchar'),
        ('description varchar(512)', 'description varchar(512)'),
        ('description varchar(125) [null]', 'description varchar(125) [null]'),
        ('description varchar [not null]', 'description varchar'),
    ],
)
def test_varchar_field_from_str_to_str(inp: str, out: str):
    res = str(create_uml_field(inp))
    assert res == out


@pytest.mark.parametrize(
    argnames=['line', 'res_params'],
    argvalues=[
        ('user_id int [null, ref: > user.id]', ('user_id', 'int', 'user', 'id', '>', True)),
        ('user_id int [not null, ref: > user.id]', ('user_id', 'int', 'user', 'id', '>', False)),
        ('user_id int [ref: > user.id]', ('user_id', 'int', 'user', 'id', '>', False)),
        ('user_id int [ref: - user.id]', ('user_id', 'int', 'user', 'id', '-', False)),
    ],
)
def test_create_fk_uml_field_from_str(line: str, res_params: tuple[str, str, str, str, bool]):
    res = create_uml_field(line)

    name, res_type, ref_table, ref_field, ref_operator, nullable = res_params
    assert isinstance(res, UMLForeignKeyField)
    assert res.name == name
    assert res.type == res_type
    assert res.ref_table == ref_table
    assert res.ref_field == ref_field
    assert res.ref_operator == ref_operator
    assert res.nullable == nullable
