"""Evaluate the frozen GSE194040 model on its held-out test set.

This script is diagnostic only. It loads the already selected model and saved
train/test membership, calculates calibration statistics from the held-out test
predictions, and writes new versioned calibration and performance outputs. It
never refits, recalibrates, tunes, or overwrites the trained model or the
original performance results.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import joblib
import matplotlib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


matplotlib.use("Agg")
import matplotlib.pyplot as plt


DEFAULT_DATA_PATH = (
    PROJECT_ROOT / "data_processed" / "gse194040_ml_ready_pcr_expression.csv"
)
DEFAULT_SPLIT_PATH = (
    PROJECT_ROOT / "results" / "tables" / "gse194040_train_test_split.csv"
)
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "gse194040_best_model.joblib"
DEFAULT_ORIGINAL_METRICS_PATH = (
    PROJECT_ROOT / "results" / "tables" / "gse194040_final_test_metrics.csv"
)
DEFAULT_OUTPUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "evaluation"
    / "gse194040_locked_test_evaluation_v2_20260719"
)
CALIBRATION_METRICS_FILENAME = "gse194040_heldout_calibration_metrics_v2.csv"
CURVE_FILENAME = "gse194040_heldout_calibration_curve_v2.csv"
RATES_FILENAME = "gse194040_observed_vs_predicted_pcr_rates_v2.csv"
PLOT_FILENAME = "gse194040_heldout_calibration_plot_v2.png"
PREDICTIONS_FILENAME = "gse194040_locked_test_predictions_v2.csv"
POINT_METRICS_FILENAME = "gse194040_locked_test_point_metrics_v2.csv"
BOOTSTRAP_CI_FILENAME = "gse194040_locked_test_bootstrap_95ci_v2.csv"
SUMMARY_FILENAME = "gse194040_locked_test_evaluation_summary_v2.md"
SESSION_FILENAME = "gse194040_locked_test_evaluation_session_v2.json"
DEFAULT_BOOTSTRAP_ITERATIONS = 2_000
DEFAULT_RANDOM_SEED = 20_260_719
BOOTSTRAP_METRICS = (
    "roc_auc",
    "accuracy",
    "sensitivity",
    "specificity",
    "precision",
    "f1",
)


def portable_package_path(path: Path) -> str:
    """Return a POSIX path relative to the package root."""
    try:
        relative = os.path.relpath(path.resolve(), PROJECT_ROOT.resolve())
    except ValueError:
        return path.name
    return Path(relative).as_posix()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Calculate performance confidence intervals and diagnostic calibration "
            "statistics for the frozen selected GSE194040 model on the saved "
            "held-out test split."
        )
    )
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA_PATH)
    parser.add_argument("--split", type=Path, default=DEFAULT_SPLIT_PATH)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL_PATH)
    parser.add_argument(
        "--original-metrics",
        type=Path,
        default=DEFAULT_ORIGINAL_METRICS_PATH,
        help="Canonical metrics used only to verify locked predictions.",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--n-bins",
        type=int,
        default=10,
        help="Number of equal-frequency bins for calibration curve data.",
    )
    parser.add_argument(
        "--bootstrap-iterations",
        type=int,
        default=DEFAULT_BOOTSTRAP_ITERATIONS,
        help="Number of paired patient-level bootstrap replicates.",
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=DEFAULT_RANDOM_SEED,
        help="Seed for NumPy's bootstrap random-number generator.",
    )
    return parser.parse_args()


def get_expected_features(model: object) -> list[str]:
    if not hasattr(model, "feature_names_in_"):
        raise AttributeError(
            "The loaded model does not expose feature_names_in_; cannot align test data."
        )
    return [str(feature) for feature in model.feature_names_in_]


def get_pcr_scores(model: object, features: pd.DataFrame) -> np.ndarray:
    if not hasattr(model, "predict_proba"):
        raise AttributeError("The loaded model does not support predict_proba.")
    classes = list(getattr(model, "classes_", []))
    if 1 not in classes:
        raise ValueError(f"Class 1 was not found in model classes: {classes}")
    return np.asarray(model.predict_proba(features)[:, classes.index(1)], dtype=float)


def select_heldout_rows(
    data: pd.DataFrame,
    split: pd.DataFrame,
    expected_features: list[str],
) -> pd.DataFrame:
    required_split_columns = {"sample_id", "pCR", "split"}
    missing_split_columns = required_split_columns.difference(split.columns)
    if missing_split_columns:
        raise ValueError(
            "Split table is missing required columns: "
            + ", ".join(sorted(missing_split_columns))
        )

    test_membership = split.loc[
        split["split"].eq("test"), ["sample_id", "pCR"]
    ].rename(columns={"pCR": "split_pCR"})
    if test_membership.empty:
        raise ValueError("Split table does not contain any held-out test rows.")
    if test_membership["sample_id"].duplicated().any():
        raise ValueError("Split table contains duplicate held-out sample_id values.")
    if data["sample_id"].duplicated().any():
        raise ValueError("ML-ready dataset contains duplicate sample_id values.")

    selected = test_membership.merge(
        data.loc[:, ["sample_id", "pCR", *expected_features]],
        on="sample_id",
        how="left",
        validate="one_to_one",
    )
    missing_rows = selected["pCR"].isna()
    if missing_rows.any():
        missing_ids = ", ".join(selected.loc[missing_rows, "sample_id"].head(25))
        raise ValueError(f"Held-out sample IDs were not found in the dataset: {missing_ids}")

    label_mismatch = selected["split_pCR"].astype(int) != selected["pCR"].astype(int)
    if label_mismatch.any():
        mismatched_ids = ", ".join(
            selected.loc[label_mismatch, "sample_id"].head(25)
        )
        raise ValueError(
            "Held-out pCR labels disagree between split and dataset for: "
            f"{mismatched_ids}"
        )
    return selected


def calibration_intercept_slope(
    y_true: np.ndarray,
    predicted_scores: np.ndarray,
) -> tuple[float, float]:
    clipped = np.clip(np.asarray(predicted_scores, dtype=float), 1e-15, 1 - 1e-15)
    logits = np.log(clipped / (1 - clipped)).reshape(-1, 1)
    diagnostic_model = LogisticRegression(
        C=np.inf,
        solver="lbfgs",
        max_iter=10_000,
    )
    diagnostic_model.fit(logits, np.asarray(y_true, dtype=int))
    return (
        float(diagnostic_model.intercept_[0]),
        float(diagnostic_model.coef_[0, 0]),
    )


def build_calibration_curve_data(
    y_true: np.ndarray,
    predicted_scores: np.ndarray,
    n_bins: int,
) -> pd.DataFrame:
    if n_bins < 2:
        raise ValueError("n_bins must be at least 2.")
    frame = pd.DataFrame(
        {
            "observed_pCR": np.asarray(y_true, dtype=int),
            "predicted_pCR_score": np.asarray(predicted_scores, dtype=float),
        }
    )
    frame["bin"] = pd.qcut(
        frame["predicted_pCR_score"],
        q=min(n_bins, len(frame)),
        labels=False,
        duplicates="drop",
    )
    curve = (
        frame.groupby("bin", observed=True)
        .agg(
            n=("observed_pCR", "size"),
            observed_pCR_count=("observed_pCR", "sum"),
            minimum_predicted_pCR_score=("predicted_pCR_score", "min"),
            maximum_predicted_pCR_score=("predicted_pCR_score", "max"),
            mean_predicted_pCR_score=("predicted_pCR_score", "mean"),
            observed_pCR_rate=("observed_pCR", "mean"),
        )
        .reset_index()
    )
    curve["bin"] = curve["bin"].astype(int) + 1
    return curve


def build_observed_vs_predicted_rates(
    y_true: np.ndarray,
    predicted_scores: np.ndarray,
    curve: pd.DataFrame,
) -> pd.DataFrame:
    overall = pd.DataFrame(
        [
            {
                "scope": "overall_heldout_test",
                "bin": pd.NA,
                "n": len(y_true),
                "observed_pCR_count": int(np.asarray(y_true, dtype=int).sum()),
                "mean_predicted_pCR_score": float(np.mean(predicted_scores)),
                "observed_pCR_rate": float(np.mean(y_true)),
            }
        ]
    )
    by_bin = curve.loc[
        :,
        [
            "bin",
            "n",
            "observed_pCR_count",
            "mean_predicted_pCR_score",
            "observed_pCR_rate",
        ],
    ].copy()
    by_bin.insert(0, "scope", "equal_frequency_bin")
    rates = pd.concat([overall, by_bin], ignore_index=True)
    rates["observed_minus_predicted"] = (
        rates["observed_pCR_rate"] - rates["mean_predicted_pCR_score"]
    )
    return rates


def calculate_point_metrics(
    y_true: np.ndarray,
    predicted_classes: np.ndarray,
    predicted_scores: np.ndarray,
) -> dict[str, float]:
    y_true = np.asarray(y_true, dtype=int)
    predicted_classes = np.asarray(predicted_classes, dtype=int)
    predicted_scores = np.asarray(predicted_scores, dtype=float)
    if not (len(y_true) == len(predicted_classes) == len(predicted_scores)):
        raise ValueError("Observed labels, classes, and scores must have equal lengths.")
    if len(np.unique(y_true)) != 2:
        raise ValueError("ROC AUC requires both outcome classes.")

    tn, fp, fn, tp = confusion_matrix(
        y_true, predicted_classes, labels=[0, 1]
    ).ravel()
    return {
        "roc_auc": float(roc_auc_score(y_true, predicted_scores)),
        "pr_auc_average_precision": float(
            average_precision_score(y_true, predicted_scores)
        ),
        "accuracy": float(accuracy_score(y_true, predicted_classes)),
        "sensitivity": float(recall_score(y_true, predicted_classes)),
        "specificity": float(tn / (tn + fp)),
        "precision": float(
            precision_score(y_true, predicted_classes, zero_division=0)
        ),
        "f1": float(f1_score(y_true, predicted_classes, zero_division=0)),
    }


def verify_locked_point_metrics(
    point_metrics: dict[str, float],
    original_metrics_path: Path,
    tolerance: float = 1e-12,
) -> None:
    original = pd.read_csv(original_metrics_path)
    if len(original) != 1:
        raise ValueError("Canonical test metrics must contain exactly one row.")
    for metric in BOOTSTRAP_METRICS:
        if metric not in original.columns:
            raise ValueError(f"Canonical test metrics are missing column: {metric}")
        expected = float(original.loc[0, metric])
        actual = point_metrics[metric]
        if not np.isclose(actual, expected, rtol=0.0, atol=tolerance):
            raise ValueError(
                f"Locked prediction verification failed for {metric}: "
                f"recomputed={actual:.17g}, canonical={expected:.17g}."
            )


def bootstrap_confidence_intervals(
    y_true: np.ndarray,
    predicted_classes: np.ndarray,
    predicted_scores: np.ndarray,
    point_metrics: dict[str, float],
    iterations: int,
    random_seed: int,
) -> pd.DataFrame:
    if iterations < 1:
        raise ValueError("bootstrap_iterations must be at least 1.")
    y_true = np.asarray(y_true, dtype=int)
    predicted_classes = np.asarray(predicted_classes, dtype=int)
    predicted_scores = np.asarray(predicted_scores, dtype=float)
    if not (len(y_true) == len(predicted_classes) == len(predicted_scores)):
        raise ValueError("Observed labels, classes, and scores must have equal lengths.")

    rng = np.random.default_rng(random_seed)
    estimates: dict[str, list[float]] = {
        metric: [] for metric in BOOTSTRAP_METRICS
    }
    for _ in range(iterations):
        indices = rng.integers(0, len(y_true), size=len(y_true))
        observed = y_true[indices]
        classes = predicted_classes[indices]
        scores = predicted_scores[indices]

        estimates["accuracy"].append(float(accuracy_score(observed, classes)))
        estimates["sensitivity"].append(
            float(recall_score(observed, classes, zero_division=0))
        )
        confusion = confusion_matrix(observed, classes, labels=[0, 1]).ravel()
        tn, fp = int(confusion[0]), int(confusion[1])
        if tn + fp:
            estimates["specificity"].append(float(tn / (tn + fp)))
        estimates["precision"].append(
            float(precision_score(observed, classes, zero_division=0))
        )
        estimates["f1"].append(
            float(f1_score(observed, classes, zero_division=0))
        )
        if len(np.unique(observed)) == 2:
            estimates["roc_auc"].append(float(roc_auc_score(observed, scores)))

    rows = []
    for metric in BOOTSTRAP_METRICS:
        values = np.asarray(estimates[metric], dtype=float)
        if values.size == 0:
            raise ValueError(f"No valid bootstrap replicates for {metric}.")
        lower, upper = np.percentile(values, [2.5, 97.5])
        rows.append(
            {
                "metric": metric,
                "point_estimate": point_metrics[metric],
                "ci_lower_95": float(lower),
                "ci_upper_95": float(upper),
                "bootstrap_iterations": iterations,
                "valid_replicates": int(values.size),
                "random_seed": random_seed,
                "method": "paired patient-level nonparametric percentile bootstrap",
            }
        )
    return pd.DataFrame(rows)


def save_calibration_plot(
    curve: pd.DataFrame,
    predicted_scores: np.ndarray,
    brier_score: float,
    intercept: float,
    slope: float,
    output_path: Path,
) -> None:
    fig, (ax_curve, ax_hist) = plt.subplots(
        2,
        1,
        figsize=(7.2, 7.2),
        gridspec_kw={"height_ratios": [3, 1]},
        constrained_layout=True,
    )
    ax_curve.plot([0, 1], [0, 1], linestyle="--", color="#5A6573", label="Ideal")
    ax_curve.plot(
        curve["mean_predicted_pCR_score"],
        curve["observed_pCR_rate"],
        marker="o",
        linewidth=2,
        color="#2F6BFF",
        label="Held-out test bins",
    )
    ax_curve.set_xlim(0, 1)
    ax_curve.set_ylim(0, 1)
    ax_curve.set_xlabel("Mean predicted pCR model score (uncalibrated)")
    ax_curve.set_ylabel("Observed pCR rate")
    ax_curve.set_title("GSE194040 held-out calibration diagnostic")
    ax_curve.grid(alpha=0.25)
    ax_curve.legend(loc="upper left")
    ax_curve.text(
        0.98,
        0.03,
        f"Brier = {brier_score:.3f}\nIntercept = {intercept:.3f}\nSlope = {slope:.3f}",
        transform=ax_curve.transAxes,
        horizontalalignment="right",
        verticalalignment="bottom",
        fontsize=10,
        bbox={"facecolor": "white", "edgecolor": "#C8CDD4", "alpha": 0.9},
    )

    ax_hist.hist(predicted_scores, bins=10, range=(0, 1), color="#63BCE3", edgecolor="white")
    ax_hist.set_xlim(0, 1)
    ax_hist.set_xlabel("Predicted pCR model score (uncalibrated)")
    ax_hist.set_ylabel("Patients")
    ax_hist.grid(axis="y", alpha=0.2)
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def ensure_new_output_directory(output_dir: Path) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(
            f"Refusing to overwrite non-empty evaluation output directory: {output_dir}. "
            "Choose a new versioned --output-dir."
        )
    output_dir.mkdir(parents=True, exist_ok=True)


def main() -> None:
    args = parse_args()
    ensure_new_output_directory(args.output_dir)

    model = joblib.load(args.model)
    expected_features = get_expected_features(model)
    data = pd.read_csv(args.data, usecols=["sample_id", "pCR", *expected_features])
    split = pd.read_csv(args.split)
    heldout = select_heldout_rows(data, split, expected_features)

    features = heldout.loc[:, expected_features]
    y_true = heldout["pCR"].astype(int).to_numpy()
    predicted_scores = get_pcr_scores(model, features)
    predicted_classes = np.asarray(model.predict(features), dtype=int)

    point_metrics = calculate_point_metrics(
        y_true, predicted_classes, predicted_scores
    )
    verify_locked_point_metrics(point_metrics, args.original_metrics)
    bootstrap_cis = bootstrap_confidence_intervals(
        y_true,
        predicted_classes,
        predicted_scores,
        point_metrics,
        args.bootstrap_iterations,
        args.random_seed,
    )

    brier = float(brier_score_loss(y_true, predicted_scores))
    intercept, slope = calibration_intercept_slope(y_true, predicted_scores)
    curve = build_calibration_curve_data(y_true, predicted_scores, args.n_bins)
    rates = build_observed_vs_predicted_rates(y_true, predicted_scores, curve)

    calibration_metrics = pd.DataFrame(
        [
            {
                "model": "elastic_net_logistic",
                "evaluation_split": "heldout_test",
                "n": len(y_true),
                "observed_pCR_count": int(y_true.sum()),
                "observed_pCR_rate": float(y_true.mean()),
                "mean_predicted_pCR_score": float(predicted_scores.mean()),
                "brier_score": brier,
                "calibration_intercept": intercept,
                "calibration_slope": slope,
                "calibration_bins": len(curve),
            }
        ]
    )

    predictions = pd.DataFrame(
        {
            "sample_id": heldout["sample_id"],
            "observed_pCR": y_true,
            "predicted_pCR_class": predicted_classes,
            "predicted_pCR_score": predicted_scores,
        }
    )
    point_metrics_table = pd.DataFrame(
        [
            {
                "model": "elastic_net_logistic",
                "evaluation_split": "locked_heldout_test",
                "n": len(y_true),
                "observed_pCR_count": int(y_true.sum()),
                "observed_non_pCR_count": int(len(y_true) - y_true.sum()),
                **point_metrics,
                "classification_source": "frozen_model_predict",
                "canonical_metrics_verified": True,
            }
        ]
    )

    calibration_metrics.to_csv(
        args.output_dir / CALIBRATION_METRICS_FILENAME, index=False
    )
    curve.to_csv(args.output_dir / CURVE_FILENAME, index=False)
    rates.to_csv(args.output_dir / RATES_FILENAME, index=False)
    predictions.to_csv(args.output_dir / PREDICTIONS_FILENAME, index=False)
    point_metrics_table.to_csv(args.output_dir / POINT_METRICS_FILENAME, index=False)
    bootstrap_cis.to_csv(args.output_dir / BOOTSTRAP_CI_FILENAME, index=False)
    save_calibration_plot(
        curve,
        predicted_scores,
        brier,
        intercept,
        slope,
        args.output_dir / PLOT_FILENAME,
    )

    summary = [
        "# GSE194040 locked held-out evaluation (v2)",
        "",
        f"Run timestamp: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Frozen evaluation design",
        "",
        f"- Saved model: `{portable_package_path(args.model)}`",
        f"- Saved split: `{portable_package_path(args.split)}`",
        f"- Held-out patients: {len(y_true)} ({int(y_true.sum())} pCR; {len(y_true) - int(y_true.sum())} non-pCR).",
        "- The original selected model was loaded without refitting or parameter changes.",
        "- Test outcomes were used only to estimate post-hoc evaluation diagnostics and uncertainty.",
        "- No calibration mapping was saved or applied to model outputs.",
        "- Frozen class predictions and model scores were calculated once, then resampled as paired patient-level records.",
        f"- Bootstrap: {args.bootstrap_iterations} percentile replicates with NumPy seed {args.random_seed}.",
        "- Recomputed AUC and classification metrics matched the canonical metrics CSV before output was written.",
        "",
        "## Discrimination and classification",
        "",
        f"- ROC AUC: {point_metrics['roc_auc']:.6f}",
        f"- PR-AUC (average precision): {point_metrics['pr_auc_average_precision']:.6f}",
        f"- Accuracy: {point_metrics['accuracy']:.6f}",
        f"- Sensitivity: {point_metrics['sensitivity']:.6f}",
        f"- Specificity: {point_metrics['specificity']:.6f}",
        f"- Precision: {point_metrics['precision']:.6f}",
        f"- F1: {point_metrics['f1']:.6f}",
        "",
        "## Calibration diagnostics",
        "",
        f"- Brier score: {brier:.6f}",
        f"- Calibration intercept: {intercept:.6f}",
        f"- Calibration slope: {slope:.6f}",
        f"- Mean predicted pCR model score: {predicted_scores.mean():.6f}",
        f"- Observed held-out pCR rate: {y_true.mean():.6f}",
        f"- Observed minus predicted rate: {y_true.mean() - predicted_scores.mean():.6f}",
        "",
        "The classifier outputs remain uncalibrated model scores. These diagnostics do not convert them into clinical probabilities or establish external validity.",
        "",
        "## Outputs",
        "",
        f"- `{POINT_METRICS_FILENAME}`",
        f"- `{BOOTSTRAP_CI_FILENAME}`",
        f"- `{PREDICTIONS_FILENAME}`",
        f"- `{CALIBRATION_METRICS_FILENAME}`",
        f"- `{CURVE_FILENAME}`",
        f"- `{RATES_FILENAME}`",
        f"- `{PLOT_FILENAME}`",
        f"- `{SESSION_FILENAME}`",
    ]
    (args.output_dir / SUMMARY_FILENAME).write_text(
        "\n".join(summary) + "\n", encoding="utf-8"
    )

    session = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "python": sys.version,
        "platform": platform.platform(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "model_path": portable_package_path(args.model),
        "data_path": portable_package_path(args.data),
        "split_path": portable_package_path(args.split),
        "original_metrics_path": portable_package_path(args.original_metrics),
        "output_dir": portable_package_path(args.output_dir),
        "n_bins_requested": args.n_bins,
        "n_bins_created": len(curve),
        "bootstrap_iterations": args.bootstrap_iterations,
        "bootstrap_random_seed": args.random_seed,
        "bootstrap_method": "paired patient-level nonparametric percentile bootstrap",
        "pr_auc_definition": "average precision",
        "canonical_metrics_verified": True,
        "diagnostic_only_no_model_refit": True,
    }
    (args.output_dir / SESSION_FILENAME).write_text(
        json.dumps(session, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote locked held-out evaluation to {args.output_dir}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from None
