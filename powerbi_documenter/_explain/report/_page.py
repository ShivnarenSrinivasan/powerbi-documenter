import pathlib
import json
from . import _visual, _model


def load(dir_: pathlib.Path) -> _model.Page:
    _config = dir_.joinpath('page.json')
    config = json.loads(_config.read_text())
    id_, name = _parse(config)
    visuals = [
        visual
        for v_dir in dir_.joinpath('visuals').iterdir()
        if (visual := _load_visual(v_dir)) is not None
    ]
    page = _model.Page(id_, name, [], visuals)
    return page


def _load_visual(dir_: pathlib.Path) -> _model.Visual | None:
    data = json.loads(dir_.joinpath('visual.json').read_text())
    try:
        visual = _visual.parse.json_to_visual(data)
    except _model.UnsupportedVisual:
        visual = None
    return visual


def _parse(json_: dict[str, str]) -> tuple[str, str]:
    return json_['name'], json_['displayName']
