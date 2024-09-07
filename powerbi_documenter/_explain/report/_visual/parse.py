from collections.abc import Callable
from powerbi_documenter._explain.report import _model


def json_to_visual(json: dict) -> _model.Visual:
    id_ = json['name']
    if 'visual' not in json:
        raise _model.UnsupportedVisual('scaffold visual')
    type_ = _get_type(json['visual']['visualType'])
    if 'visualContainerObjects' not in json['visual']:
        name = ''
    else:
        name = _get_visual_name(json['visual']['visualContainerObjects'])
    query = _get_query(json['visual']['query'], type_)
    return _model.Visual(id_, name, type_, query)


def _get_visual_name(visual_container_objects: dict) -> str:
    # a known issue is when the title is hidden, but there is text there--it may not match
    # with the frontend
    name = visual_container_objects['title'][0]['properties']['text']['expr'][
        'Literal'
    ]['Value']
    return name.replace("'", '')


def _get_type(type_: str) -> _model.VisualType:
    if type_ not in _VISUAL_TYPE_LOOKUP:
        raise _model.UnsupportedVisual(f'{type_} not supported')
    return _VISUAL_TYPE_LOOKUP[type_]


_VISUAL_TYPE_LOOKUP = {
    'slicer': _model.VisualType.SLICER,
    'tableEx': _model.VisualType.TABLE,
    'card': _model.VisualType.CARD,
    'advancedSlicerVisual': _model.VisualType.ADVANCED_SLICER,
    'pivotTable': _model.VisualType.MATRIX,
    'map': _model.VisualType.MAP,
    'lineChart': _model.VisualType.LINE_CHART,
    'donutChart': _model.VisualType.DONUT_CHART,
}

_VISUAL_COLUMN_LOOKUP = {
    _model.VisualType.MAP: ('Category', 'Size'),
    _model.VisualType.LINE_CHART: ('Category', 'Y'),
    _model.VisualType.DONUT_CHART: ('Category', 'Y'),
}
def _visual_field_names(visual_: _model.VisualType) -> tuple[str, str]:
    return _VISUAL_COLUMN_LOOKUP.get(visual_, ('Rows', 'Values'))

def _get_query(query: dict, visual_: _model.VisualType) -> _model.Query:
    x, y = _visual_field_names(visual_)
    state = query['queryState']

    values = _get_values(state[y]['projections'])
    rows = _get_rows(state.get(x))

    query_state = _model.QueryState(rows, values)
    return _model.Query(query_state)


def _get_rows(rows: list[dict] | None) -> _model.Rows:
    if rows is None:
        return []
    return [_get_projection(obj) for obj in rows['projections']]


def _get_values(values: list[dict] | None) -> _model.Values:
    return [_get_projection(obj) for obj in values]


def _get_projection(obj: dict) -> _model.Projection:
    field = _get_field(obj['field'])
    name = str(obj.get('displayName') or field.entity_field)
    return _model.Projection(field, name)


def _get_field(field: dict) -> _model.Field:
    key = str(list(field.keys())[0])
    if key not in _FIELD_LOOKUP:
        breakpoint()
    type_ = _FIELD_LOOKUP[key]
    body = field[key]
    entity, entity_field = _entity_extractor(type_)(body)
    # if 'Property' not in body:
    #     breakpoint()
    # entity_field = body['Property']
    return _model.Field(type_, entity, entity_field)


_FIELD_LOOKUP = {
    'Measure': _model.FieldType.MEASURE,
    'Column': _model.FieldType.COLUMN,
    'Aggregation': _model.FieldType.AGGREGATION,
}

_Entity = tuple[_model.Entity, str]

def _entity_extractor(field: _model.FieldType) -> Callable[[dict], _Entity]:
    lookup = {_model.FieldType.AGGREGATION: _agg_entity}
    return lookup.get(field, _default_entity)


def _agg_entity(d: dict) -> _Entity:
    return _default_entity(d['Expression']['Column'])

def _default_entity(d: dict) -> _Entity:
    return _model.Entity(d['Expression']['SourceRef']['Entity']), d['Property']
