import pathlib
from powerbi_documenter._tmdl_model import Measure
from powerbi_documenter._parser.measure import parse

_ROOT = pathlib.Path(__file__).parent


class TestParse:
    def test_single_measure(self) -> None:
        source = _ROOT.joinpath('single_measure-1.txt')
        with open(source) as fp:
            lines = fp.readlines()

        actual = parse(lines)
        expected = Measure(
            name='Asset Accumulated depreciation on investment support Amount',
            code="// note\nSUM(  'Asset Transaction'[Asset Accumulated depreciation on investment support Amt]\n)",
            documentation=' Asset Accumulated depreciation on investment support Amt Description',
            format='#,##0.00',
            folder='[ Measures ]',
            lineage='8eea1da0-6c3d-41a8-9329-875636188060',
            isHidden=False,
        )
        assert actual == expected
