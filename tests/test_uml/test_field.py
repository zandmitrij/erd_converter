from __future__ import annotations

import pytest

from erd_converter.uml import field as uml_field


@pytest.mark.parametrize(
    argnames=['line', 'res_params'],
    argvalues=[
        ('id int [pk]', ('id', True, False)),
        ('count int [not null]', ('count', False, False)),
        ('foo int [null]', ('foo', False, True)),
        ('bar int', ('bar', False, False)),
    ],
)
def test_uml_integer_field_from_str(line: str, res_params: tuple[str, bool, bool]):
    res = uml_field.create_uml_field(line)

    assert isinstance(res, uml_field.UMLIntegerField)
    
    name, is_pk, is_nullable = res_params
    assert res.name == name
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
    res = str(uml_field.create_uml_field(inp))
    assert res == out


@pytest.mark.parametrize(
    argnames=['line', 'res_params'],
    argvalues=[
        ('name varchar', ('name', 256, False, False)),
        ('description varchar(512)', ('description', 512, False, False)),
        ('description varchar(125) [null]', ('description', 125, False, True)),
        ('description varchar [not null]', ('description', 256, False, False)),
    ],
)
def test_create_uml_varchar_field_from_str(line: str, res_params: tuple[str, int, bool, bool]):
    res = uml_field.create_uml_field(line)

    assert isinstance(res, uml_field.UMLVarcharField)
    
    name, size, is_pk, is_null = res_params
    assert res.name == name
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
    res = str(uml_field.create_uml_field(inp))
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
    res = uml_field.create_uml_field(line)

    assert isinstance(res, uml_field.UMLForeignKeyField)
    name, res_type, ref_table, ref_field, ref_operator, nullable = res_params
    
    assert res.name == name
    assert res.type == res_type
    assert res.ref_table == ref_table
    assert res.ref_field == ref_field
    assert res.ref_operator == ref_operator
    assert res.nullable == nullable


@pytest.mark.parametrize(
    argnames=['line', 'res_params'],
    argvalues=[
        ('is_enabled boolean [null]', ('is_enabled', True)),
    ],
)
def test_create_array_uml_field_from_str(line: str, res_params: tuple[str, bool]):
    res = uml_field.create_uml_field(line)
    
    assert isinstance(res, uml_field.UMLBooleanField)

    res_name, res_nullable = res_params
    assert res.name == res_name
    assert res.nullable == res_nullable



@pytest.mark.parametrize(
    argnames=['line', 'res_params'],
    argvalues=[
        ('dependents array[varchar(512) [null]]', ('dependents', uml_field.UMLVarcharField, 512, True)),
        ('dependents array[varchar]', ('dependents', uml_field.UMLVarcharField, 256, False)),
    ],
)
def test_create_array_uml_field_from_str(line: str, res_params: tuple[str, str]):
    res = uml_field.create_uml_field(line)
    assert isinstance(res, uml_field.UMLArrayField)
    res_name, res_subfield_type, res_subfield_size, res_subfield_null = res_params
    
    assert res.name == res_name
    assert isinstance(res.subfield, res_subfield_type)
    assert res.subfield.size == res_subfield_size
    assert res.subfield.nullable == res_subfield_null
    

def test_create_json_uml_field_from_str():
    line = 'flags json [null]'
    
    res_name, res_nullable = 'flags', True
    res = uml_field.create_uml_field(line)
    assert isinstance(res, uml_field.UMLJsonField)
    
    assert res.name == res_name
    assert res.nullable == res_nullable
