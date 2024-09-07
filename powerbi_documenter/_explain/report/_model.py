from __future__ import annotations
from collections.abc import Sequence
import dataclasses
import enum
import pathlib
import typing


class FileSystemNavigator:
    """Locates files in report director."""

    def __init__(self, root: pathlib.Path) -> None:
        self._root = root

    def definition(self) -> pathlib.Path:
        return self._root.joinpath('definition.pbir')

    def pages(self) -> pathlib.Path: ...


@dataclasses.dataclass
class Report:
    title: str
    pages: Sequence[Page]
    active_page: Page


@dataclasses.dataclass
class Page:
    id: str = dataclasses.field(repr=False)
    name: str
    filters: Sequence[_Filter] = dataclasses.field(repr=False)
    visuals: Sequence[Visual] = dataclasses.field(repr=False)


@dataclasses.dataclass
class _Filter:
    id: str


@dataclasses.dataclass
class Visual:
    id: str
    name: str
    type: VisualType
    query: Query


class VisualType(enum.StrEnum):
    SLICER = enum.auto()
    ADVANCED_SLICER = enum.auto()
    CARD = enum.auto()
    MATRIX = enum.auto()
    TABLE = enum.auto()
    MAP = enum.auto()
    LINE_CHART = enum.auto()
    DONUT_CHART = enum.auto()


class InvalidReportFormat(ValueError):
    """Raised when report is not pbir."""


class UnsupportedVisual(TypeError):
    """Raised when undefined visual is parsed."""


@dataclasses.dataclass
class Query:
    state: QueryState


@dataclasses.dataclass
class QueryState:
    rows: Rows
    values: Values


Rows = Sequence['Projection']
Values = Sequence['Projection']


@dataclasses.dataclass
class Projection:
    field: Field
    display_name: str


@dataclasses.dataclass
class Field:
    type: FieldType
    entity: Entity
    entity_field: str


class FieldType(enum.StrEnum):
    COLUMN = enum.auto()
    MEASURE = enum.auto()
    AGGREGATION = enum.auto()


Entity = typing.NewType('Entity', str)


class Lineage(typing.NamedTuple):
    projection: Projection
    visual: Visual
    page: Page
    report: Report
