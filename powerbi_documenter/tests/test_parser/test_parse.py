from powerbi_documenter._parser._parse import (
    extract_field_name,
    body_fields,
    extract_body_field,
)


class TestBodyFields:
    def test_default(self) -> None:
        text = [
            'formatString: #,##0.00',
            'displayFolder: [ Measures ]',
        ]
        expected = {'formatString': '#,##0.00', 'displayFolder': '[ Measures ]'}
        assert body_fields(text) == expected

class TestExtractFieldName:
    def test_measure(self) -> None:
        text = 'measure Asset = Sum(Asset)'
        expected = 'Asset'
        assert extract_field_name(text, 'measure') == expected

    def test_column(self) -> None:
        text = 'column Asset'
        expected = 'Asset'
        assert extract_field_name(text, 'column') == expected

    def test_calculated_column(self) -> None:
        text = 'column Value = 1'
        expected = 'Value'
        assert extract_field_name(text, 'column') == expected
