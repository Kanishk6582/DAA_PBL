from pathlib import Path

import matplotlib.pyplot as plt


def build_comparison_figure(rows: list[dict[str, float]]):
    budgets = [row["budget"] for row in rows]
    dp_scores = [row["dp"] for row in rows]
    greedy_scores = [row["greedy"] for row in rows]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(budgets, dp_scores, marker="o", linewidth=2, label="Dynamic Programming")
    ax.plot(budgets, greedy_scores, marker="s", linewidth=2, label="Greedy")
    ax.set_title("Satisfaction vs Available Time")
    ax.set_xlabel("Available Time (minutes)")
    ax.set_ylabel("Adjusted Satisfaction")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()
    fig.tight_layout()
    return fig


def save_comparison_plot(rows: list[dict[str, float]], output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig = build_comparison_figure(rows)
    fig.savefig(output)
    plt.close(fig)
    return output
