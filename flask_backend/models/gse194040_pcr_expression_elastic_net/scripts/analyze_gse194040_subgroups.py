"""Evaluate prespecified subgroups using frozen GSE194040 test predictions.

The script reads the existing versioned locked-test predictions and saved test
membership. It never loads, fits, tunes, or modifies the trained model.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


DEFAULT_PREDICTIONS_PATH = (
    PROJECT_ROOT
    / "results"
    / "evaluation"
    / "gse194040_locked_test_evaluation_v2_20260719"
    / "gse194040_locked_test_predictions_v2.csv"
)
DEFAULT_DATA_PATH = (
    PROJECT_ROOT / "data_processed" / "gse194040_ml_ready_pcr_expression.csv"
)
DEFAULT_SPLIT_PATH = (
    PROJECT_ROOT / "results" / "tables" / "gse194040_train_test_split.csv"
)
DEFAULT_ORIGINAL_METRICS_PATH = (
    PROJECT_ROOT / "results" / "tables" / "gse194040_final_test_metrics.csv"
)
DEFAULT_OUTPUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "evaluation"
    / "gse194040_locked_test_subgroups_v1_20260719"
)
RESULTS_FILENAME = "gse194040_locked_test_subgroup_metrics_v1.csv"
SUMMARY_FILENAME = "gse194040_locked_test_subgroup_summary_v1.md"
SESSION_FILENAME = "gse194040_locked_test_subgroup_session_v1.json"
DEFAULT_BOOTSTRAP_ITERATIONS = 2_000
DEFAULT_RANDOM_SEED = 20_260_719
DEFAULT_MINIMUM_TREATMENT_N = 10
DEFAULT_MINIMUM_OUTCOME_COUNT = 3
DEFAULT_EXPLORATORY_N = 30


def portable_package_path(path: Path) -> str:
    """Return a POSIX path relative to the package root."""
    try:
        relative = os.path.relpath(path.resolve(), PROJECT_ROOT.resolve())
    except ValueError:
        return path.name
    return Path(relative).as_posix()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate subgroups from frozen GSE194040 test predictions."
    )
    parser.add_argument(
        "--predictions", type=Path, default=DEFAULT_PREDICTIONS_PATH
    )
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA_PATH)
    parser.add_argument("--split", type=Path, default=DEFAULT_SPLIT_PATH)
    parser.add_argument(
        "--original-metrics", type=Path, default=DEFAULT_ORIGINAL_METRICS_PATH
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--bootstrap-iterations", type=int, default=DEFAULT_BOOTSTRAP_ITERATIONS
    )
    parser.add_argument("--random-seed", type=int, default=DEFAULT_RANDOM_SEED)
    parser.add_argument(
        "--minimum-treatment-n", type=int, default=DEFAULT_MINIMUM_TREATMENT_N
    )
    parser.add_argument(
        "--minimum-outcome-count", type=int, default=DEFAULT_MINIMUM_OUTCOME_COUNT
    )
    parser.add_argument(
        "--exploratory-n", type=int, default=DEFAULT_EXPLORATORY_N
    )
    return parser.parse_args()


def ensure_new_output_directory(output_dir: Path) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(
            f"Refusing to overwrite non-empty subgroup output directory: {output_dir}. "
            "Choose a new versioned --output-dir."
        )
    output_dir.mkdir(parents=True, exist_ok=True)


def binary_metrics(
    observed: np.ndarray,
    predicted_classes: np.ndarray,
    predicted_scores: np.ndarray,
) -> dict[str, float]:
    observed = np.asarray(observed, dtype=int)
    predicted_classes = np.asarray(predicted_classes, dtype=int)
    predicted_scores = np.asarray(predicted_scores, dtype=float)
    tn, fp, fn, tp = confusion_matrix(
        observed, predicted_classes, labels=[0, 1]
    ).ravel()
    return {
        "roc_auc": (
            float(roc_auc_score(observed, predicted_scores))
            if len(np.unique(observed)) == 2
            else np.nan
        ),
        "sensitivity": float(tp / (tp + fn)) if tp + fn else np.nan,
        "specificity": float(tn / (tn + fp)) if tn + fp else np.nan,
    }


def verify_overall_metrics(
    locked: pd.DataFrame,
    original_metrics_path: Path,
    tolerance: float = 1e-12,
) -> None:
    observed = locked["observed_pCR"].astype(int).to_numpy()
    classes = locked["predicted_pCR_class"].astype(int).to_numpy()
    scores = locked["predicted_pCR_score"].astype(float).to_numpy()
    subgroup_metrics = binary_metrics(observed, classes, scores)
    tn, fp, fn, tp = confusion_matrix(observed, classes, labels=[0, 1]).ravel()
    recomputed = {
        "roc_auc": subgroup_metrics["roc_auc"],
        "accuracy": float(accuracy_score(observed, classes)),
        "sensitivity": subgroup_metrics["sensitivity"],
        "specificity": subgroup_metrics["specificity"],
        "precision": float(precision_score(observed, classes, zero_division=0)),
        "f1": float(f1_score(observed, classes, zero_division=0)),
    }
    original = pd.read_csv(original_metrics_path)
    if len(original) != 1:
        raise ValueError("Canonical test metrics must contain exactly one row.")
    for metric, actual in recomputed.items():
        expected = float(original.loc[0, metric])
        if not np.isclose(actual, expected, rtol=0.0, atol=tolerance):
            raise ValueError(
                f"Locked prediction verification failed for {metric}: "
                f"recomputed={actual:.17g}, canonical={expected:.17g}."
            )


def load_locked_subgroup_data(
    predictions_path: Path,
    data_path: Path,
    split_path: Path,
    original_metrics_path: Path,
) -> pd.DataFrame:
    predictions = pd.read_csv(predictions_path)
    required_prediction_columns = {
        "sample_id",
        "observed_pCR",
        "predicted_pCR_class",
        "predicted_pCR_score",
    }
    missing = required_prediction_columns.difference(predictions.columns)
    if missing:
        raise ValueError(
            "Locked predictions are missing columns: " + ", ".join(sorted(missing))
        )
    if predictions["sample_id"].duplicated().any():
        raise ValueError("Locked predictions contain duplicate sample_id values.")

    split = pd.read_csv(split_path)
    required_split_columns = {"sample_id", "pCR", "split"}
    missing = required_split_columns.difference(split.columns)
    if missing:
        raise ValueError("Saved split is missing columns: " + ", ".join(sorted(missing)))
    test_split = split.loc[
        split["split"].eq("test"), ["sample_id", "pCR"]
    ].rename(columns={"pCR": "split_pCR"})
    if test_split["sample_id"].duplicated().any():
        raise ValueError("Saved test split contains duplicate sample_id values.")
    if set(predictions["sample_id"]) != set(test_split["sample_id"]):
        raise ValueError("Locked predictions do not exactly match saved test membership.")

    metadata = pd.read_csv(
        data_path,
        usecols=["sample_id", "pCR", "HR", "HER2", "MP", "treatment_arm"],
    )
    if metadata["sample_id"].duplicated().any():
        raise ValueError("ML-ready data contain duplicate sample_id values.")
    locked = (
        test_split.merge(predictions, on="sample_id", validate="one_to_one")
        .merge(metadata, on="sample_id", validate="one_to_one")
    )
    if len(locked) != len(test_split):
        raise ValueError("One or more saved test samples lack subgroup metadata.")
    if not (
        locked["split_pCR"].astype(int).eq(locked["observed_pCR"].astype(int)).all()
        and locked["pCR"].astype(int).eq(locked["observed_pCR"].astype(int)).all()
    ):
        raise ValueError("Outcome labels disagree across split, predictions, and data.")
    if locked[["HR", "HER2", "MP", "treatment_arm"]].isna().any().any():
        raise ValueError("Locked test subgroup metadata contain missing values.")
    verify_overall_metrics(locked, original_metrics_path)
    return locked


def derived_group_seed(base_seed: int, family: str, subgroup: str) -> int:
    digest = hashlib.sha256(
        f"{base_seed}|{family}|{subgroup}".encode("utf-8")
    ).digest()
    return int.from_bytes(digest[:4], byteorder="little", signed=False)


def bootstrap_metric_intervals(
    observed: np.ndarray,
    predicted_classes: np.ndarray,
    predicted_scores: np.ndarray,
    iterations: int,
    random_seed: int,
) -> dict[str, float | int]:
    if iterations < 1:
        raise ValueError("bootstrap_iterations must be at least 1.")
    observed = np.asarray(observed, dtype=int)
    predicted_classes = np.asarray(predicted_classes, dtype=int)
    predicted_scores = np.asarray(predicted_scores, dtype=float)
    rng = np.random.default_rng(random_seed)
    estimates: dict[str, list[float]] = {
        "roc_auc": [],
        "sensitivity": [],
        "specificity": [],
    }
    for _ in range(iterations):
        indices = rng.integers(0, len(observed), size=len(observed))
        metrics = binary_metrics(
            observed[indices], predicted_classes[indices], predicted_scores[indices]
        )
        for metric, value in metrics.items():
            if np.isfinite(value):
                estimates[metric].append(value)

    result: dict[str, float | int] = {}
    for metric, values in estimates.items():
        if not values:
            raise ValueError(f"No valid bootstrap replicates for {metric}.")
        lower, upper = np.percentile(np.asarray(values), [2.5, 97.5])
        result[f"{metric}_ci_lower_95"] = float(lower)
        result[f"{metric}_ci_upper_95"] = float(upper)
        result[f"{metric}_valid_replicates"] = len(values)
    return result


def subgroup_definitions(locked: pd.DataFrame) -> list[tuple[str, str, pd.DataFrame]]:
    definitions: list[tuple[str, str, pd.DataFrame]] = []
    hr_her2_labels = {
        (0, 0): "HR-/HER2-",
        (0, 1): "HR-/HER2+",
        (1, 0): "HR+/HER2-",
        (1, 1): "HR+/HER2+",
    }
    for values, label in hr_her2_labels.items():
        subset = locked.loc[locked["HR"].eq(values[0]) & locked["HER2"].eq(values[1])]
        definitions.append(("HR_HER2", label, subset))
    for value in (0, 1):
        definitions.append(("MP_status", f"MP={value}", locked.loc[locked["MP"].eq(value)]))
    for arm in sorted(locked["treatment_arm"].astype(str).unique()):
        definitions.append(
            (
                "treatment_arm",
                arm,
                locked.loc[locked["treatment_arm"].astype(str).eq(arm)],
            )
        )
    return definitions


def build_subgroup_results(
    locked: pd.DataFrame,
    bootstrap_iterations: int,
    random_seed: int,
    minimum_treatment_n: int,
    minimum_outcome_count: int,
    exploratory_n: int,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for family, subgroup, subset in subgroup_definitions(locked):
        n = len(subset)
        pcr_count = int(subset["observed_pCR"].sum())
        non_pcr_count = n - pcr_count
        minimum_n = minimum_treatment_n if family == "treatment_arm" else 1
        sufficient = (
            n >= minimum_n
            and pcr_count >= minimum_outcome_count
            and non_pcr_count >= minimum_outcome_count
        )
        exploratory = n < exploratory_n
        if not sufficient:
            status = "not_estimated_insufficient_sample"
        elif exploratory:
            status = "exploratory_small_sample"
        else:
            status = "reported"

        row: dict[str, object] = {
            "subgroup_family": family,
            "subgroup": subgroup,
            "n": n,
            "pCR_count": pcr_count,
            "non_pCR_count": non_pcr_count,
            "sufficient_for_estimation": sufficient,
            "exploratory": exploratory,
            "analysis_status": status,
            "roc_auc": np.nan,
            "roc_auc_ci_lower_95": np.nan,
            "roc_auc_ci_upper_95": np.nan,
            "sensitivity": np.nan,
            "sensitivity_ci_lower_95": np.nan,
            "sensitivity_ci_upper_95": np.nan,
            "specificity": np.nan,
            "specificity_ci_lower_95": np.nan,
            "specificity_ci_upper_95": np.nan,
            "bootstrap_iterations": bootstrap_iterations,
            "bootstrap_base_random_seed": random_seed,
            "bootstrap_group_random_seed": np.nan,
            "roc_auc_valid_replicates": 0,
            "sensitivity_valid_replicates": 0,
            "specificity_valid_replicates": 0,
        }
        if sufficient:
            observed = subset["observed_pCR"].astype(int).to_numpy()
            classes = subset["predicted_pCR_class"].astype(int).to_numpy()
            scores = subset["predicted_pCR_score"].astype(float).to_numpy()
            metrics = binary_metrics(observed, classes, scores)
            group_seed = derived_group_seed(random_seed, family, subgroup)
            intervals = bootstrap_metric_intervals(
                observed, classes, scores, bootstrap_iterations, group_seed
            )
            row.update(metrics)
            row.update(intervals)
            row["bootstrap_group_random_seed"] = group_seed
        rows.append(row)
    return pd.DataFrame(rows)


def write_summary(results: pd.DataFrame, args: argparse.Namespace) -> None:
    estimated = results.loc[results["sufficient_for_estimation"]]
    omitted = results.loc[~results["sufficient_for_estimation"]]
    lines = [
        "# GSE194040 locked test subgroup evaluation (v1)",
        "",
        f"Run timestamp: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Design",
        "",
        "- Uses only the existing versioned locked-test predictions; the trained model is not loaded or refit.",
        f"- Bootstrap: {args.bootstrap_iterations} paired patient-level percentile replicates with base seed {args.random_seed}.",
        f"- Treatment arms require n >= {args.minimum_treatment_n} and at least {args.minimum_outcome_count} patients in each outcome class.",
        f"- Any estimated subgroup with n < {args.exploratory_n} is marked exploratory.",
        "- ROC AUC, sensitivity, and specificity confidence intervals are internal descriptive estimates, not external validation.",
        "",
        "## Estimated subgroups",
        "",
        "| Family | Subgroup | n | pCR | ROC AUC (95% CI) | Sensitivity (95% CI) | Specificity (95% CI) | Status |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in estimated.itertuples(index=False):
        lines.append(
            f"| {row.subgroup_family} | {row.subgroup} | {row.n} | {row.pCR_count} | "
            f"{row.roc_auc:.3f} ({row.roc_auc_ci_lower_95:.3f}-{row.roc_auc_ci_upper_95:.3f}) | "
            f"{row.sensitivity:.3f} ({row.sensitivity_ci_lower_95:.3f}-{row.sensitivity_ci_upper_95:.3f}) | "
            f"{row.specificity:.3f} ({row.specificity_ci_lower_95:.3f}-{row.specificity_ci_upper_95:.3f}) | "
            f"{row.analysis_status} |"
        )
    lines.extend(["", "## Treatment arms not estimated", ""])
    if omitted.empty:
        lines.append("None.")
    else:
        for row in omitted.itertuples(index=False):
            lines.append(
                f"- {row.subgroup}: n={row.n}, pCR={row.pCR_count}; insufficient under the prespecified reporting rule."
            )
    lines.extend(
        [
            "",
            "The subgroup analysis is descriptive and underpowered for interaction or treatment-effect inference. It must not be interpreted as evidence that treatment performance differs between arms or biomarker groups.",
        ]
    )
    (args.output_dir / SUMMARY_FILENAME).write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    args = parse_args()
    ensure_new_output_directory(args.output_dir)
    locked = load_locked_subgroup_data(
        args.predictions, args.data, args.split, args.original_metrics
    )
    results = build_subgroup_results(
        locked,
        args.bootstrap_iterations,
        args.random_seed,
        args.minimum_treatment_n,
        args.minimum_outcome_count,
        args.exploratory_n,
    )
    results.to_csv(args.output_dir / RESULTS_FILENAME, index=False)
    write_summary(results, args)
    session = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "python": sys.version,
        "platform": platform.platform(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "predictions_path": portable_package_path(args.predictions),
        "data_path": portable_package_path(args.data),
        "split_path": portable_package_path(args.split),
        "original_metrics_path": portable_package_path(args.original_metrics),
        "output_dir": portable_package_path(args.output_dir),
        "locked_test_patients": len(locked),
        "bootstrap_iterations": args.bootstrap_iterations,
        "bootstrap_base_random_seed": args.random_seed,
        "bootstrap_method": "paired patient-level nonparametric percentile bootstrap",
        "minimum_treatment_n": args.minimum_treatment_n,
        "minimum_outcome_count": args.minimum_outcome_count,
        "exploratory_n": args.exploratory_n,
        "model_loaded_or_refit": False,
        "canonical_overall_metrics_verified": True,
    }
    (args.output_dir / SESSION_FILENAME).write_text(
        json.dumps(session, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote locked test subgroup evaluation to {args.output_dir}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from None
