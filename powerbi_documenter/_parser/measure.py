from powerbi_documenter import _tmdl_model
from . import _parse


def parse(text: list[str]) -> _tmdl_model.Measure:
    i = 0
    while text[i].strip().startswith(_tmdl_model.DOC_SYMBOL):
        i += 1
    doc = text[:i]
    name = _parse.extract_field_name(text[i], 'measure')
    code_first_line = text[i].split('= ')[-1]
    i += 1
    start = i
    for line in text[start:]:
        if not line.startswith('\t\t\t'):
            break
        i += 1

    code = (
        (code_first_line + '\n'.join(m.strip() for m in text[start:i]))
        .replace(_tmdl_model.QUERY_WRAPPER, '')
        .strip()
    )
    body_fields = _parse.body_fields(text[i:])
    out = _tmdl_model.Measure(
        name,
        code,
        '\n'.join(d.strip().replace(_tmdl_model.DOC_SYMBOL, '') for d in doc),
        body_fields['formatString'],
        body_fields.get('displayFolder'),
        body_fields['lineageTag'],
        'isHidden' in body_fields,
    )
    return out
