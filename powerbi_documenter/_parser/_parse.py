"""Common parsing utilities."""
from collections.abc import Iterable
import re
from typing import Literal as L


def body_fields(text: Iterable[str]) -> dict[str, str]:
    return dict(extract_body_field(line) for line in text)


def extract_body_field(row: str) -> tuple[str, str]:
    name, *rest = row.split()
    return name.replace(':', ''), ' '.join(rest)


def extract_field_name(field: str, field_type: L['measure', 'column']) -> str:
    mat = re.search(f"{field_type} ([^=.]+)?( =)?", field)
    assert mat is not None
    removed_quotes = mat.group(1).replace("'", '').strip()
    return removed_quotes
