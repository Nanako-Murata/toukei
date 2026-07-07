from scipy import stats
from app.schemas.models import GroupData
from app.exceptions import CalculationError


def run_chisquare(groups: list[GroupData]) -> dict:
    if len(groups) < 2:
        raise CalculationError("カイ二乗検定には2つ以上の列(カテゴリ)が必要です。")

    lengths = [len(g.values) for g in groups]
    if len(set(lengths)) != 1:
        raise CalculationError("カイ二乗検定では、すべての列の行数が一致している必要があります。")

    if lengths[0] < 2:
        raise CalculationError("カイ二乗検定には2行以上のデータが必要です。")

    for g in groups:
        for v in g.values:
            if v < 0:
                raise CalculationError("件数(度数)は0以上の値を入力してください。")
            if v != int(v):
                raise CalculationError("件数(度数)は整数で入力してください(例: 2.5のような小数は不可)。")

    contingency_table = [g.values for g in groups]
    contingency_table = list(map(list, zip(*contingency_table)))

    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)

    low_expected_count = sum(1 for row in expected for val in row if val < 5)
    total_cells = expected.size
    warning = None
    if low_expected_count > 0:
        warning = (
            f"期待度数が5未満のセルが{low_expected_count}個(全{total_cells}個中)あります。"
            "この場合カイ二乗検定の近似精度が低下するため、結果の解釈には注意してください。"
        )

    fisher_result = None
    is_2x2 = len(contingency_table) == 2 and len(contingency_table[0]) == 2
    if is_2x2:
        odds_ratio, fisher_p = stats.fisher_exact(contingency_table)
        fisher_result = {
            "oddsRatio": float(odds_ratio),
            "pValue": float(fisher_p),
        }

    return {
        "statistic": float(chi2),
        "pValue": float(p_value),
        "degreesOfFreedom": int(dof),
        "observed": contingency_table,
        "expected": expected.tolist(),
        "warning": warning,
        "fisher": fisher_result,
    }