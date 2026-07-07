import numpy as np
import pandas as pd
from scipy import stats
from app.schemas.models import GroupData
from app.exceptions import CalculationError


def run_correlation(groups: list[GroupData]) -> dict:
    if len(groups) < 2:
        raise CalculationError("相関分析には2つ以上の変数が必要です。")

    lengths = [len(g.values) for g in groups]
    if len(set(lengths)) != 1:
        raise CalculationError("相関分析では、すべての変数のデータ数が一致している必要があります。")

    if lengths[0] < 2:
        raise CalculationError("相関分析には各変数につき2つ以上のデータが必要です。")

    names = [g.name for g in groups]
    df = pd.DataFrame({g.name: g.values for g in groups})

    corr_matrix = df.corr(method="pearson")

    p_matrix = pd.DataFrame(
        np.ones((len(names), len(names))), index=names, columns=names
    )
    for i in range(len(names)):
        for j in range(len(names)):
            if i != j:
                _, p = stats.pearsonr(df[names[i]], df[names[j]])
                p_matrix.iloc[i, j] = p

    return {
        "labels": names,
        "correlation": corr_matrix.round(4).to_dict(),
        "pValue": p_matrix.round(4).to_dict(),
    }