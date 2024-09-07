import argparse
import pathlib
import pypandoc
from powerbi_documenter import _llm, _explain


def main(root: pathlib.Path, outdir: pathlib.Path) -> None:
    files = [file for file in root.iterdir() if _should_process(file.name)]
    llm = _llm.get_model(2000, 'gpt-4-32k')

    for file in files:
        llm_call = _LOOKUP.get(file.name, _explain.table.explain)
        explanation = llm_call(file.read_text(), llm)
        outfile = outdir.joinpath(file.with_suffix('.md').name)
        outfile.write_text(explanation)
        pypandoc.convert_file(
            outfile.resolve().as_posix(),
            'docx',
            outputfile=outfile.with_suffix('.docx'),
        )


def _should_process(file: str) -> bool:
    return len(_EXCLUSIONS) == 0 or not any(entry in file for entry in _EXCLUSIONS)

    # entry = input(f'should process {file}? (Y/N), default=Y')
    # return entry.upper() == 'Y' or entry.strip() == ''


_LOOKUP = {'_MEASURES_ACCOUNTING.tmdl': _explain.measures.explain}

_EXCLUSIONS = ('DateTable', 'CountryDirector', 'AssetStat', 'AssetType')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--indir', type=pathlib.Path, metavar='', help='')
    parser.add_argument('--outdir', type=pathlib.Path, metavar='', help='')
    args = parser.parse_args()

    main(args.indir, args.outdir)
