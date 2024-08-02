from __future__ import annotations
import enum
from dataclasses import dataclass


@dataclass
class Table:
    name: str
    lineage: str
    measures: list[Measure]
    columns: list[Column]
    query: Query


@dataclass
class Measure:
    name: str
    code: str
    documentation: str
    format: str
    folder: str | None
    lineage: str
    isHidden: bool


@dataclass
class Column:
    name: str
    code: str | None
    documentation: str
    source_name: str
    data_type: str
    lineage: str
    summarize_by: str
    isHidden: bool


@dataclass
class Query:
    mode: QueryMode
    code: str


class QueryMode(enum.StrEnum):
    DIRECT = enum.auto()
    IMPORT = enum.auto()


DOC_SYMBOL = '///'
QUERY_WRAPPER = '```'
