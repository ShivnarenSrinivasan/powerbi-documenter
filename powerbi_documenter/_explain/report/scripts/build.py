import pathlib
import pandas as pd
from powerbi_documenter._explain.report import _report, _model

p = pathlib.Path(
    # r'C:\Users\wb570819\shiv\repos\wfafo-hotspot-dashboard\out\Reports\Asset.Report'
    r'C:\Users\wb570819\shiv\repos\wfafo-hotspot-dashboard\out\Reports\Hotspot Dashboard.Report'
)


def main(root: pathlib.Path) -> None:
    dirs = [dir_ for dir_ in root.iterdir() if dir_.name.endswith('.Report')]
    out = pd.concat([_build_report(dir_) for dir_ in dirs])
    renamed = _make_columns_accountant_readable(out)
    renamed.to_excel('Mapping.xlsx', index=False)


def _make_columns_accountant_readable(out: pd.DataFrame) -> pd.DataFrame:
    # accountants don't seem to like underscores 🙃
    return out.rename(
        columns={col: col.replace('_', ' ').title() for col in out.columns}
    )


def _build_report(p: pathlib.Path) -> pd.DataFrame:
    try:
        _report.validate_format(p)
    except _model.InvalidReportFormat as e:
        print(e)
        return pd.DataFrame()
    report = _report.load(p)
    lineage = _report.create_lineage(report)
    out = [_report.flatten_lineage(l) for l in lineage]
    df = pd.DataFrame.from_records(out)
    return df


if __name__ == '__main__':
    root = pathlib.Path(
        r'C:\Users\wb570819\shiv\repos\wfafo-hotspot-dashboard\out\Reports'
    )
    main(root)
