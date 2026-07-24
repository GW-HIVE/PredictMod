"""Create descriptive cohort, QC, and normalization plots for GSE194040.

The expression matrix used here is already submitter-normalized, log2
transformed, gene-level collapsed, and platform/batch adjusted. The
normalization figure therefore summarizes the post-normalization expression
distributions rather than a raw-versus-normalized comparison.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]


LABELS = {
    "pCR": {0: "non-pCR", 1: "pCR"},
    "HR": {0: "HR-", 1: "HR+"},
    "HER2": {0: "HER2-", 1: "HER2+"},
    "MP": {0: "MP1 high risk", 1: "MP2 ultra/high risk"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot descriptive GSE194040 cohort, QC, and normalization summaries."
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=PROJECT_ROOT / "data_processed" / "gse194040_ml_ready_pcr_expression.csv",
        help="ML-ready GSE194040 CSV.",
    )
    parser.add_argument(
        "--gene-qc",
        type=Path,
        default=PROJECT_ROOT / "results" / "tables" / "gse194040_gene_feature_qc.csv",
        help="Gene-level QC CSV produced during preprocessing.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "figures",
        help="Directory for output figures.",
    )
    parser.add_argument(
        "--tables-dir",
        type=Path,
        default=PROJECT_ROOT / "results" / "tables",
        help="Directory for output summary tables.",
    )
    parser.add_argument(
        "--expression-sample-size",
        type=int,
        default=250_000,
        help="Maximum expression values sampled per platform for density plots.",
    )
    parser.add_argument("--random-state", type=int, default=20260720)
    return parser.parse_args()


def add_bar_labels(ax: plt.Axes, counts: pd.Series, total: int) -> None:
    for idx, value in enumerate(counts.to_numpy()):
        percent = 100 * value / total
        ax.text(
            value,
            idx,
            f" {value:,} ({percent:.1f}%)",
            va="center",
            ha="left",
            fontsize=8,
        )


def count_series(series: pd.Series, label_map: dict[int, str] | None = None) -> pd.Series:
    counts = series.value_counts(dropna=False).sort_index()
    if label_map:
        counts.index = [label_map.get(int(value), str(value)) for value in counts.index]
    return counts


def plot_count_panel(ax: plt.Axes, counts: pd.Series, title: str, total: int) -> None:
    y = np.arange(len(counts))
    ax.barh(y, counts.to_numpy(), color="#4c78a8")
    ax.set_yticks(y, labels=counts.index)
    ax.invert_yaxis()
    ax.set_title(title)
    ax.set_xlabel("Patients")
    ax.set_xlim(0, max(counts.max() * 1.22, 1))
    add_bar_labels(ax, counts, total)
    ax.grid(axis="x", alpha=0.25)


def write_categorical_summary(data: pd.DataFrame, tables_dir: Path) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    total = len(data)
    for column in ["pCR", "HR", "HER2", "MP", "platform", "treatment_arm"]:
        labels = LABELS.get(column)
        counts = count_series(data[column], labels)
        for category, n in counts.items():
            rows.append(
                {
                    "variable": column,
                    "category": category,
                    "n": int(n),
                    "fraction": float(n / total),
                }
            )
    summary = pd.DataFrame(rows)
    summary.to_csv(tables_dir / "gse194040_cohort_descriptor_summary.csv", index=False)
    return summary


def plot_cohort_distributions(data: pd.DataFrame, output_dir: Path) -> None:
    total = len(data)
    fig, axes = plt.subplots(3, 2, figsize=(12, 13))
    panels = [
        ("pCR", "pCR outcome"),
        ("HR", "Hormone receptor status"),
        ("HER2", "HER2 status"),
        ("MP", "MammaPrint status"),
        ("platform", "Agilent platform"),
        ("treatment_arm", "Treatment arm"),
    ]
    for ax, (column, title) in zip(axes.ravel(), panels):
        labels = LABELS.get(column)
        counts = count_series(data[column], labels)
        if column == "treatment_arm":
            counts = counts.sort_values(ascending=True)
        plot_count_panel(ax, counts, title, total)
    fig.suptitle("GSE194040 ML-ready cohort descriptors", y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(output_dir / "gse194040_cohort_distributions.png", dpi=200)
    plt.close(fig)


def plot_cohort_distribution_range(data: pd.DataFrame, output_dir: Path) -> None:
    total = len(data)
    rows: list[dict[str, object]] = []
    panels = [
        ("pCR", "pCR outcome"),
        ("HR", "Hormone receptor"),
        ("HER2", "HER2"),
        ("MP", "MammaPrint"),
        ("platform", "Platform"),
        ("treatment_arm", "Treatment arm"),
    ]
    for column, group in panels:
        labels = LABELS.get(column)
        counts = count_series(data[column], labels)
        if column == "treatment_arm":
            counts = counts.sort_values(ascending=False)
        for category, n in counts.items():
            rows.append(
                {
                    "group": group,
                    "category": str(category),
                    "n": int(n),
                    "percent": 100 * int(n) / total,
                }
            )

    plot_rows: list[dict[str, object]] = []
    y_positions: list[float] = []
    current_y = 0.0
    previous_group = None
    for row in rows:
        if previous_group is not None and row["group"] != previous_group:
            current_y += 0.7
        plot_rows.append(row)
        y_positions.append(current_y)
        current_y += 1.0
        previous_group = row["group"]

    group_colors = {
        "pCR outcome": "#4c78a8",
        "Hormone receptor": "#72b7b2",
        "HER2": "#f58518",
        "MammaPrint": "#54a24b",
        "Platform": "#b279a2",
        "Treatment arm": "#9d755d",
    }
    colors = [group_colors[str(row["group"])] for row in plot_rows]
    labels = [f"{row['group']}: {row['category']}" for row in plot_rows]
    percents = np.array([float(row["percent"]) for row in plot_rows])
    counts = [int(row["n"]) for row in plot_rows]

    fig_height = max(8, 0.36 * len(plot_rows) + 1.8)
    fig, ax = plt.subplots(figsize=(12, fig_height))
    ax.barh(y_positions, percents, color=colors)
    ax.set_yticks(y_positions, labels=labels)
    ax.invert_yaxis()
    ax.set_xlabel("Share of ML-ready cohort (%)")
    ax.set_title("GSE194040 cohort distribution range")
    ax.set_xlim(0, max(percents.max() * 1.22, 5))
    ax.grid(axis="x", alpha=0.25)

    for y, pct, n in zip(y_positions, percents, counts):
        ax.text(pct, y, f" {n:,} ({pct:.1f}%)", va="center", ha="left", fontsize=8)

    fig.tight_layout()
    fig.savefig(output_dir / "gse194040_cohort_distribution_range.png", dpi=200)
    plt.close(fig)


def plot_qc_distributions(
    data: pd.DataFrame, gene_qc: pd.DataFrame, output_dir: Path, tables_dir: Path
) -> None:
    expr_cols = [column for column in data.columns if column.startswith("expr_")]
    sample_missing_rate = data[expr_cols].isna().mean(axis=1)
    sample_missing_count = data[expr_cols].isna().sum(axis=1)

    qc_summary = pd.DataFrame(
        [
            {
                "metric": "gene_missing_rate",
                "min": gene_qc["missing_rate"].min(),
                "median": gene_qc["missing_rate"].median(),
                "mean": gene_qc["missing_rate"].mean(),
                "p95": gene_qc["missing_rate"].quantile(0.95),
                "max": gene_qc["missing_rate"].max(),
            },
            {
                "metric": "gene_variance",
                "min": gene_qc["variance"].min(),
                "median": gene_qc["variance"].median(),
                "mean": gene_qc["variance"].mean(),
                "p95": gene_qc["variance"].quantile(0.95),
                "max": gene_qc["variance"].max(),
            },
            {
                "metric": "sample_missing_rate",
                "min": sample_missing_rate.min(),
                "median": sample_missing_rate.median(),
                "mean": sample_missing_rate.mean(),
                "p95": sample_missing_rate.quantile(0.95),
                "max": sample_missing_rate.max(),
            },
            {
                "metric": "sample_missing_count",
                "min": sample_missing_count.min(),
                "median": sample_missing_count.median(),
                "mean": sample_missing_count.mean(),
                "p95": sample_missing_count.quantile(0.95),
                "max": sample_missing_count.max(),
            },
        ]
    )
    qc_summary.to_csv(tables_dir / "gse194040_qc_distribution_summary.csv", index=False)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.6))
    axes[0].hist(gene_qc["missing_rate"] * 100, bins=40, color="#4c78a8")
    axes[0].axvline(20, color="#e45756", linestyle="--", linewidth=1)
    axes[0].set_title("Gene missingness")
    axes[0].set_xlabel("Missing values per gene (%)")
    axes[0].set_ylabel("Genes")

    axes[1].hist(gene_qc["variance"], bins=50, color="#72b7b2")
    axes[1].axvline(1e-8, color="#e45756", linestyle="--", linewidth=1)
    axes[1].set_xscale("log")
    axes[1].set_title("Gene variance")
    axes[1].set_xlabel("Variance, log scale")
    axes[1].set_ylabel("Genes")

    axes[2].hist(sample_missing_count, bins=40, color="#54a24b")
    axes[2].set_title("Sample missingness")
    axes[2].set_xlabel("Missing gene values per patient")
    axes[2].set_ylabel("Patients")

    fig.suptitle("GSE194040 expression QC distributions", y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(output_dir / "gse194040_qc_distributions.png", dpi=200)
    plt.close(fig)


def sample_expression_values(
    values: pd.DataFrame, sample_size: int, rng: np.random.Generator
) -> np.ndarray:
    flattened = values.to_numpy(dtype=float, copy=False).ravel()
    flattened = flattened[~np.isnan(flattened)]
    if len(flattened) <= sample_size:
        return flattened
    indices = rng.choice(len(flattened), size=sample_size, replace=False)
    return flattened[indices]


def plot_normalization_summary(
    data: pd.DataFrame, output_dir: Path, tables_dir: Path, sample_size: int, random_state: int
) -> None:
    expr_cols = [column for column in data.columns if column.startswith("expr_")]
    expr = data[expr_cols]
    platforms = data["platform"].astype(str)
    rng = np.random.default_rng(random_state)

    sample_stats = pd.DataFrame(
        {
            "sample_id": data["sample_id"],
            "platform": platforms,
            "expression_median": expr.median(axis=1, skipna=True),
            "expression_iqr": expr.quantile(0.75, axis=1) - expr.quantile(0.25, axis=1),
            "expression_mean": expr.mean(axis=1, skipna=True),
        }
    )
    sample_stats.to_csv(tables_dir / "gse194040_post_normalization_sample_summary.csv", index=False)

    platform_order = sorted(platforms.unique())
    plotted_platform_order = [
        platform for platform in platform_order if int((platforms == platform).sum()) >= 10
    ]
    if not plotted_platform_order:
        plotted_platform_order = platform_order
    medians = [
        sample_stats.loc[sample_stats["platform"] == platform, "expression_median"].to_numpy()
        for platform in plotted_platform_order
    ]
    iqrs = [
        sample_stats.loc[sample_stats["platform"] == platform, "expression_iqr"].to_numpy()
        for platform in plotted_platform_order
    ]
    sampled_values = {
        platform: sample_expression_values(
            expr.loc[platforms == platform], sample_size=sample_size, rng=rng
        )
        for platform in plotted_platform_order
    }

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.8))
    axes[0].boxplot(medians, tick_labels=plotted_platform_order, showfliers=False)
    axes[0].set_title("Per-sample median")
    axes[0].set_ylabel("Normalized log2 expression")

    axes[1].boxplot(iqrs, tick_labels=plotted_platform_order, showfliers=False)
    axes[1].set_title("Per-sample IQR")
    axes[1].set_ylabel("Normalized log2 expression IQR")

    for platform, values in sampled_values.items():
        axes[2].hist(values, bins=80, alpha=0.45, density=True, label=platform)
    axes[2].set_title("Sampled expression values")
    axes[2].set_xlabel("Normalized log2 expression")
    axes[2].set_ylabel("Density")
    axes[2].legend(frameon=False)

    fig.suptitle("GSE194040 post-normalization expression distributions", y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(output_dir / "gse194040_post_normalization_expression_distributions.png", dpi=200)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.tables_dir.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(args.data)
    gene_qc = pd.read_csv(args.gene_qc)

    write_categorical_summary(data, args.tables_dir)
    plot_cohort_distributions(data, args.output_dir)
    plot_cohort_distribution_range(data, args.output_dir)
    plot_qc_distributions(data, gene_qc, args.output_dir, args.tables_dir)
    plot_normalization_summary(
        data,
        args.output_dir,
        args.tables_dir,
        sample_size=args.expression_sample_size,
        random_state=args.random_state,
    )

    print(f"Wrote figures to {args.output_dir}")
    print(f"Wrote summary tables to {args.tables_dir}")


if __name__ == "__main__":
    main()
