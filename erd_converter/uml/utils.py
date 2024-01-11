import re

DATA_TYPE_PATTERN = re.compile(r'\b\w+\s+(\w+(?:\(\d+\))?(?:\[\w+.*?\])?)\b')


def get_data_type(line: str) -> str:
    if 'ref' in line:
        return 'fk'

    match = DATA_TYPE_PATTERN.search(line)
    if not match:
        raise ValueError(f'Incorrect field {line}')
    return match.group(1)


def get_nullable(options: list[str]) -> bool:
    if 'null' in options:
        return True
    if 'not null' in options:
        return False
    return False
