# File: charts/other_charts.py
"""High-visibility bar chart helpers for my_career_report."""

import os
from typing import Dict, List

import matplotlib.pyplot as plt


def _prep_dir(path: str) -> None:
    """Ensure the output directory exists."""
    os.makedirs(os.path.dirname(path), exist_ok=True)


def render_interest(data: Dict, output_path: str, cfg: Dict) -> None:
    """Render RIASEC interest scores as a bar chart."""
    interest = data.get("interest", data)
    labels = ["R", "I", "A", "S", "E", "C"]
    scores = [interest[label] for label in labels]

    dpi = cfg["charts"].get("dpi", 300)
    figsize = tuple(cfg["charts"].get("figsize", [6, 4]))

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    bars = ax.bar(labels, scores, edgecolor="black", alpha=0.8)
    ax.set_ylim(0, 100)
    ax.set_title("직무 관심사(RIASEC) 점수", fontsize=14, fontweight="bold")
    ax.set_xlabel("RIASEC 유형", fontsize=12)
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
    _prep_dir(output_path)
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def render_values(data: Dict, output_path: str, cfg: Dict) -> None:
    """Render job values as a bar chart."""
    values = data.get("values", data)
    labels = ["A", "I", "Rec", "Rel", "S", "W"]
    scores = [values[label] for label in labels]

    dpi = cfg["charts"].get("dpi", 300)
    figsize = tuple(cfg["charts"].get("figsize", [6, 4]))

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    bars = ax.bar(labels, scores, edgecolor="black", alpha=0.8)
    ax.set_ylim(0, 100)
    ax.set_title("직업 가치관 점수", fontsize=14, fontweight="bold")
    ax.set_xlabel("가치관 유형", fontsize=12)
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
    _prep_dir(output_path)
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def render_ai(data: Dict, output_path: str, cfg: Dict) -> None:
    """Render AI literacy scores as a bar chart."""
    ai_data = data.get("ai", data)
    labels = ["EU", "TS", "CE", "AO", "SE", "CB", "ER"]
    scores = [ai_data[label] for label in labels]

    dpi = cfg["charts"].get("dpi", 300)
    figsize = tuple(cfg["charts"].get("figsize", [6, 4]))

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    bars = ax.bar(labels, scores, edgecolor="black", alpha=0.8)
    ax.set_ylim(0, 100)
    ax.set_title("AI 활용능력 점수", fontsize=14, fontweight="bold")
    ax.set_xlabel("역량 영역", fontsize=12)
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
    _prep_dir(output_path)
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def render_tech(data: List[Dict], output_path: str, cfg: Dict) -> None:
    """Render technology competency scores as a bar chart."""
    tech = data
    if isinstance(data, dict):
        tech = data.get("tech", [])

    labels = [item["name"] for item in tech]
    scores = [item["score"] for item in tech]

    dpi = cfg["charts"].get("dpi", 300)
    figsize = tuple(cfg["charts"].get("figsize", [6, 4]))

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    bars = ax.bar(labels, scores, edgecolor="black", alpha=0.8)
    ax.set_ylim(0, 100)
    ax.set_title("AI/기술 핵심 역량 점수", fontsize=14, fontweight="bold")
    ax.set_xlabel("핵심 역량", fontsize=12)
    ax.set_ylabel("점수 (Index)", fontsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10)
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f"{height:.1f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    plt.tight_layout()
    _prep_dir(output_path)
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def render_soft(data: List[Dict], output_path: str, cfg: Dict) -> None:
    """Render soft skill scores as a bar chart."""
    soft = data
    if isinstance(data, dict):
        soft = data.get("soft", [])

    labels = [item["name"] for item in soft]
    scores = [item["score"] for item in soft]

    dpi = cfg["charts"].get("dpi", 300)
    figsize = tuple(cfg["charts"].get("figsize", [6, 4]))

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    bars = ax.bar(labels, scores, edgecolor="black", alpha=0.8)
    ax.set_ylim(0, 100)
    ax.set_title("비즈니스·소프트 스킬 점수", fontsize=14, fontweight="bold")
    ax.set_xlabel("스킬 항목", fontsize=12)
    ax.set_ylabel("점수 (Index)", fontsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10)
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f"{height:.1f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    plt.tight_layout()
    _prep_dir(output_path)
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
