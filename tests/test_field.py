from erd_converter.field import UMLField


def test_creating_uml_field_from_str():
    line = 'id int [pk]'
    res = UMLField.from_str(line)
    assert isinstance(res, UMLField)
    assert res.name == 'id'
    assert res.type == 'int'
    assert res.primary_key
    assert not res.nullable


def test_creating_uml_field_from_str_2():
    line = 'name varchar'
    res = UMLField.from_str(line)
    assert isinstance(res, UMLField)
    assert res.name == 'name'
    assert res.type == 'varchar'
    assert not res.primary_key
    assert not res.nullable
