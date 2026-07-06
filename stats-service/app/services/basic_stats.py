import numpy as np
from app.schemas.models import GroupData


def run_basic_stats(groups: list[GroupData]) -> dict:
    result = {}
    for group in groups:
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
    return result