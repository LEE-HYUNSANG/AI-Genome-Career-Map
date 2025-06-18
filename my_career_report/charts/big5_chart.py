# File: charts/big5_chart.py
"""Utilities for rendering the BIG-5 personality chart."""

import os
import matplotlib.pyplot as plt


def render_big5(data: dict, output_path: str, cfg: dict) -> None:
    """Render a BIG-5 bar chart and save it as a PNG.

    Parameters
    ----------
    data : dict
        Either a dictionary with BIG-5 scores ``{"E": .., "A": .., ...}`` or a
        parent dictionary containing the ``"big5"`` key.
    output_path : str
        File path where the chart image will be saved.
    cfg : dict
        Configuration dictionary loaded from ``config.yaml``. The keys
        ``cfg["charts"]["dpi"]`` and ``cfg["charts"]["figsize"]`` control figure
        size and resolution.
    """

    big5_data = data.get("big5", data)
    LABEL_MAP = {"E": "외향성", "A": "친화성", "C": "성실성", "N": "신경성", "O": "개방성"}
    codes = ["E", "A", "C", "N", "O"]
    labels = [LABEL_MAP[c] for c in codes]
    scores = [big5_data[c] for c in codes]

    dpi = cfg["charts"].get("dpi", 300)
    figsize = tuple(cfg["charts"].get("figsize", [6, 4]))

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    bars = ax.bar(labels, scores, edgecolor="black", alpha=0.8)
    ax.set_ylim(0, 100)
    ax.set_title("BIG-5 개인성향 점수", fontsize=14, fontweight="bold")
    ax.set_xlabel("성향 요인", fontsize=12)
    ax.set_ylabel("점수 (Index)", fontsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f"{height:.1f}",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
