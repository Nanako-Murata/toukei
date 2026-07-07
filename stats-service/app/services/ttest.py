from scipy import stats
from app.schemas.models import GroupData
from app.exceptions import CalculationError


def run_ttest(groups: list[GroupData], options: dict) -> dict:
    if len(groups) != 2:
        raise CalculationError("t検定には2つの群が必要です。")

    values1 = groups[0].values
    values2 = groups[1].values

    if len(values1) < 2 or len(values2) < 2:
        raise CalculationError("各群に2つ以上のデータが必要です。")

    paired = options.get("paired", False) if options else False

    if paired:
        if len(values1) != len(values2):
            raise CalculationError("対応ありt検定では、両群のデータ数が一致している必要があります。")
        test_result = stats.ttest_rel(values1, values2)
        df = len(values1) - 1
    else:
        test_result = stats.ttest_ind(values1, values2)
        df = len(values1) + len(values2) - 2

    return {
        "statistic": float(test_result.statistic),
        "pValue": float(test_result.pvalue),
        "degreesOfFreedom": df,
        "paired": paired,
        "summary": {
            groups[0].name: {
                "mean": float(sum(values1) / len(values1)),
                "n": len(values1),
            },
            groups[1].name: {
                "mean": float(sum(values2) / len(values2)),
                "n": len(values2),
            },
        },
    }