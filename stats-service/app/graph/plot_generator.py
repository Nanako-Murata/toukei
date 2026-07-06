import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from app.schemas.models import GroupData


def _fig_to_base64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def generate_boxplot(groups: list[GroupData]) -> str:
    fig, ax = plt.subplots()
    values_list = [group.values for group in groups]
    labels = [f"#{i + 1}" for i in range(len(groups))]

    ax.boxplot(values_list, tick_labels=labels)
    ax.set_xlabel("Group")
    ax.set_ylabel("Value")
    ax.set_ylim(bottom=0)
    fig.tight_layout()

    return _fig_to_base64(fig)


def generate_scatterplot(groups: list[GroupData]) -> str:
    fig, ax = plt.subplots()

    for i, group in enumerate(groups):
        x = np.random.normal(loc=i + 1, scale=0.05, size=len(group.values))
        ax.scatter(x, group.values, alpha=0.7)

    labels = [f"#{i + 1}" for i in range(len(groups))]
    ax.set_xticks(range(1, len(groups) + 1))
    ax.set_xticklabels(labels)
    ax.set_xlabel("Group")
    ax.set_ylabel("Value")
    ax.set_ylim(bottom=0)
    fig.tight_layout()

    return _fig_to_base64(fig)