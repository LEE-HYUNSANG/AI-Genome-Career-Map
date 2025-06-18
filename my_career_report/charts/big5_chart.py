# File: charts/big5_chart.py
import os
import matplotlib.pyplot as plt


def render_big5(data: dict, output_path: str, cfg: dict) -> None:
    """Render BIG-5 bar chart and save to ``output_path``."""
    labels = ["E", "A", "C", "N", "O"]
    scores = [data["big5"][k] for k in labels]
    dpi = cfg['charts'].get('dpi', 300)
    figsize = cfg['charts'].get('figsize', [6,4])
    plt.figure(figsize=figsize, dpi=dpi)
    plt.bar(labels, scores, color='skyblue')
    plt.ylim(0, 100)
    plt.title('BIG-5 Scores')
    plt.xlabel('Trait')
    plt.ylabel('Score')
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=dpi)
    plt.close()
