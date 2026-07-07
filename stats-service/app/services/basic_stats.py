import numpy as np
from app.schemas.models import GroupData
from app.exceptions import CalculationError


def run_basic_stats(groups: list[GroupData]) -> dict:
    result = {}

    for group in groups:
        if len(group.values) == 0:
            continue  # データが空の群はスキップ(エラーにしない)

        values = np.array(group.values)
        result[group.name] = {
            "mean": float(np.mean(values)),
            "median": float(np.median(values)),
            "sd": float(np.std(values, ddof=1)) if len(values) > 1 else 0.0,
            "variance": float(np.var(values, ddof=1)) if len(values) > 1 else 0.0,
            "min": float(np.min(values)),
            "max": float(np.max(values)),
            "n": len(values),
        }

    if len(result) == 0:
        raise CalculationError("値を入力してください。")

    return result