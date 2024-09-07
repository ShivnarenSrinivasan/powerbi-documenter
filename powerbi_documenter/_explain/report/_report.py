from collections.abc import Sequence
import itertools as it
import pathlib
import json
from . import _page, _model


def load(dir_: pathlib.Path) -> _model.Report:
    definition = dir_.joinpath('definition')
    _pages = definition.joinpath('pages')
    pages = [_page.load(d) for d in _pages.iterdir() if not d.is_file()]
    name = dir_.name.replace('.Report', '')
    active_pagename = json.loads(_pages.joinpath('pages.json').read_text())[
        'activePageName'
    ]
    active_page = [p for p in pages if p.id == active_pagename][0]
    report = _model.Report(name, pages, active_page)
    return report


def create_lineage(report: _model.Report) -> Sequence[_model.Lineage]:
    _lineage = []
    for page in report.pages:
        for visual in page.visuals:
            for proj in it.chain(visual.query.state.rows, visual.query.state.values):
                # data = (proj, visual.name, visual.type, page.name, report.title)
                data = _model.Lineage(proj, visual, page, report)
                _lineage.append(data)
    return _lineage


def flatten_lineage(lineage: _model.Lineage) -> dict[str, str]:
    return {
        'field_display_name_report': lineage.projection.display_name,
        'field_powerbi': lineage.projection.field.entity_field,
        'table_powerbi': lineage.projection.field.entity,
        'visual_name': lineage.visual.name,
        'visual_type': lineage.visual.type,
        'page': lineage.page.name,
        'report': lineage.report.title,
    }


def validate_format(report_root: pathlib.Path) -> None:
    if not report_root.joinpath('definition').exists():
        raise _model.InvalidReportFormat(f'invalid report: {report_root.name}')
