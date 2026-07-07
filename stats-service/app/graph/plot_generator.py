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


def generate_heatmap(corr_matrix: dict, labels: list[str]) -> str:
    n = len(labels)
    matrix = np.array([[corr_matrix[row][col] for col in labels] for row in labels])

    fig, ax = plt.subplots()
    im = ax.imshow(matrix, vmin=-1, vmax=1, cmap="coolwarm")

    display_labels = [f"#{i + 1}" for i in range(n)]
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(display_labels)
    ax.set_yticklabels(display_labels)

    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", color="black")

    fig.colorbar(im, ax=ax)
    fig.tight_layout()

    return _fig_to_base64(fig)


def generate_regression_plot(groups: list[GroupData], result: dict) -> str:
    x = np.array(groups[0].values)
    y = np.array(groups[1].values)

    fig, ax = plt.subplots()
    ax.scatter(x, y, alpha=0.7, label="Data")

    x_line = np.linspace(min(x), max(x), 100)
    y_line = result["slope"] * x_line + result["intercept"]
    ax.plot(x_line, y_line, color="red", label="Regression line")

    ax.set_xlabel("#1")
    ax.set_ylabel("#2")
    ax.set_ylim(bottom=0)
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    fig.tight_layout()

    return _fig_to_base64(fig)


def generate_prediction_plot(predicted: list, actual: list) -> str:
    fig, ax = plt.subplots()

    ax.scatter(actual, predicted, alpha=0.7)

    min_val = min(min(actual), min(predicted))
    max_val = max(max(actual), max(predicted))
    ax.plot([min_val, max_val], [min_val, max_val], color="red", linestyle="--", label="Perfect fit")

    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    ax.set_ylim(bottom=0)
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    fig.tight_layout()

    return _fig_to_base64(fig)