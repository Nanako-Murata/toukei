import numpy as np
import statsmodels.api as sm
from scipy import stats
from app.schemas.models import GroupData
from app.exceptions import CalculationError


def run_regression(groups: list[GroupData]) -> dict:
    if len(groups) < 2:
        raise CalculationError("単回帰分析には2つの変数(X, Y)が必要です。")

    x = np.array(groups[0].values)
    y = np.array(groups[1].values)

    if len(x) != len(y):
        raise CalculationError("単回帰分析では、XとYのデータ数が一致している必要があります。")

    if len(x) < 3:
        raise CalculationError("単回帰分析には3つ以上のデータペアが必要です。")

    reg = stats.linregress(x, y)

    return {
        "slope": float(reg.slope),
        "intercept": float(reg.intercept),
        "rSquared": float(reg.rvalue ** 2),
        "pValue": float(reg.pvalue),
        "standardError": float(reg.stderr),
        "xLabel": groups[0].name,
        "yLabel": groups[1].name,
    }


def run_multiple_regression(groups: list[GroupData], options: dict) -> dict:
    if len(groups) < 3:
        raise CalculationError("重回帰分析には3つ以上の変数(説明変数2つ以上＋目的変数1つ)が必要です。")

    y_index = options.get("yColumnIndex") if options else None
    if y_index is None:
        raise CalculationError("目的変数(Y)となる列を指定してください。")

    if y_index < 0 or y_index >= len(groups):
        raise CalculationError("指定されたY列のインデックスが範囲外です。")

    lengths = [len(g.values) for g in groups]
    if len(set(lengths)) != 1:
        raise CalculationError("重回帰分析では、すべての変数のデータ数が一致している必要があります。")

    if lengths[0] < len(groups) + 1:
        raise CalculationError("データ数が変数の数に対して不足しています(サンプル数を増やしてください)。")

    y = np.array(groups[y_index].values)
    x_groups = [g for i, g in enumerate(groups) if i != y_index]
    x_names = [g.name if g.name else f"X{i+1}" for i, g in enumerate(x_groups)]

    X = np.column_stack([g.values for g in x_groups])
    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit()

    coefficients = {}
    for i, name in enumerate(x_names):
        coefficients[name] = {
            "coefficient": float(model.params[i + 1]),
            "pValue": float(model.pvalues[i + 1]),
        }

    return {
        "intercept": float(model.params[0]),
        "interceptPValue": float(model.pvalues[0]),
        "coefficients": coefficients,
        "rSquared": float(model.rsquared),
        "adjustedRSquared": float(model.rsquared_adj),
        "fPValue": float(model.f_pvalue),
        "yLabel": groups[y_index].name,
        "predicted": model.predict(X).tolist(),
        "actual": y.tolist(),
    }