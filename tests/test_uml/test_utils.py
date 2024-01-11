import pytest

from erd_converter.uml import utils as u


@pytest.mark.parametrize(
    argnames=['example', 'expected_data_type'],
    argvalues=[
        ('dependents array[varchar(512)] [not null]', 'array'),
        ('is_enabled boolean [null]', 'boolean'),
        ('user_id int [null, ref: > user.id]', 'fk'),
        ('description varchar(125) [null]', 'varchar'),
        ('name varchar', 'varchar'),
        ('count int [not null]', 'int'),
    ],
)
def test_extract_data_type(example: str, expected_data_type: str):
    result = u.get_data_type(example)
    assert result == expected_data_type
