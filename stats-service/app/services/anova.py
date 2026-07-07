from scipy import stats
from app.schemas.models import GroupData
from app.exceptions import CalculationError


def run_anova(groups: list[GroupData]) -> dict:
    if len(groups) < 3:
        raise CalculationError("ANOVA(分散分析)には3つ以上の群が必要です。")

    for g in groups:
        if len(g.values) < 2:
            raise CalculationError(f"群「{g.name}」のデータが不足しています(2つ以上必要です)。")

    values_list = [g.values for g in groups]
    f_statistic, p_value = stats.f_oneway(*values_list)

    summary = {}
    for g in groups:
        summary[g.name] = {
            "mean": float(sum(g.values) / len(g.values)),
            "n": len(g.values),
        }

    return {
        "statistic": float(f_statistic),
        "pValue": float(p_value),
        "summary": summary,
    }