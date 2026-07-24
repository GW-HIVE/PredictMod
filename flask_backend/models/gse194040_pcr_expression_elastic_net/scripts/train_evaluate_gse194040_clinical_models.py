"""Train clinical comparison models without using the locked test set for tuning.

The clinical-only and clinical-plus-expression pipelines are selected by
cross-validation on the saved training membership. The locked test membership
is scored once after selection. Existing expression-model predictions are read
from their protected versioned output and are never replaced.
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
import joblib
import matplotlib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
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
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


matplotlib.use("Agg")
import matplotlib.pyplot as plt


DEFAULT_DATA_PATH = (
    PROJECT_ROOT / "data_processed" / "gse194040_ml_ready_pcr_expression.csv"
)
DEFAULT_SPLIT_PATH = (
    PROJECT_ROOT / "results" / "tables" / "gse194040_train_test_split.csv"
)
DEFAULT_EXPRESSION_PREDICTIONS_PATH = (
    PROJECT_ROOT
    / "results"
    / "evaluation"
    / "gse194040_locked_test_evaluation_v2_20260719"
    / "gse194040_locked_test_predictions_v2.csv"
)
DEFAULT_ORIGINAL_METRICS_PATH = (
    PROJECT_ROOT / "results" / "tables" / "gse194040_final_test_metrics.csv"
)
DEFAULT_OUTPUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "evaluation"
    / "gse194040_clinical_expression_comparison_v1_20260719"
)
CLINICAL_MODEL_FILENAME = "gse194040_clinical_baseline_model_v1.joblib"
COMBINED_MODEL_FILENAME = "gse194040_clinical_plus_expression_model_v1.joblib"
PREDICTIONS_FILENAME = "gse194040_model_comparison_locked_test_predictions_v1.csv"
METRICS_FILENAME = "gse194040_model_comparison_locked_test_metrics_v1.csv"
CI_FILENAME = "gse194040_model_comparison_bootstrap_95ci_v1.csv"
PAIRWISE_FILENAME = "gse194040_model_comparison_pairwise_differences_v1.csv"
CV_RESULTS_FILENAME = "gse194040_clinical_models_training_cv_results_v1.csv"
CURVE_FILENAME = "gse194040_model_comparison_calibration_curve_v1.csv"
PLOT_FILENAME = "gse194040_model_comparison_calibration_plot_v1.png"
SUMMARY_FILENAME = "gse194040_clinical_expression_comparison_summary_v1.md"
SESSION_FILENAME = "gse194040_clinical_expression_comparison_session_v1.json"

CLINICAL_BINARY_COLUMNS = ["HR", "HER2", "MP"]
TREATMENT_COLUMN = "treatment_arm"
MODEL_ORDER = [
    "clinical_baseline",
    "expression_model_existing",
    "clinical_plus_expression",
]
BOOTSTRAP_METRICS = [
    "roc_auc",
    "pr_auc_average_precision",
    "brier_score",
    "calibration_intercept",
    "calibration_slope",
]
DEFAULT_CV_FOLDS = 3
DEFAULT_RANDOM_SEED = 42
DEFAULT_BOOTSTRAP_SEED = 20_260_719
DEFAULT_BOOTSTRAP_ITERATIONS = 2_000


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
            "Train clinical-only and clinical-plus-expression models using saved "
            "training membership, then evaluate the locked test set once."
        )
    )
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA_PATH)
    parser.add_argument("--split", type=Path, default=DEFAULT_SPLIT_PATH)
    parser.add_argument(
        "--expression-predictions",
        type=Path,
        default=DEFAULT_EXPRESSION_PREDICTIONS_PATH,
    )
    parser.add_argument(
        "--original-metrics", type=Path, default=DEFAULT_ORIGINAL_METRICS_PATH
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--cv-folds", type=int, default=DEFAULT_CV_FOLDS)
    parser.add_argument("--random-seed", type=int, default=DEFAULT_RANDOM_SEED)
    parser.add_argument(
        "--bootstrap-seed", type=int, default=DEFAULT_BOOTSTRAP_SEED
    )
    parser.add_argument(
        "--bootstrap-iterations", type=int, default=DEFAULT_BOOTSTRAP_ITERATIONS
    )
    parser.add_argument("--n-jobs", type=int, default=1)
    parser.add_argument("--max-iter", type=int, default=1_500)
    return parser.parse_args()


def validate_n_jobs(n_jobs: int) -> int:
    if n_jobs == 0 or n_jobs < -1:
        raise ValueError("n_jobs must be -1 or a positive integer.")
    return n_jobs


def logistic_convergence_status(estimator: Pipeline) -> dict[str, object]:
    classifier = estimator.named_steps["classifier"]
    iterations = np.asarray(classifier.n_iter_, dtype=int).ravel()
    observed_max = int(iterations.max())
    configured_max = int(classifier.max_iter)
    return {
        "classifier_class": type(classifier).__name__,
        "n_iter": iterations.tolist(),
        "observed_max_iter": observed_max,
        "configured_max_iter": configured_max,
        "status": (
            "converged_before_max_iter"
            if observed_max < configured_max
            else "reached_max_iter_review_warning"
        ),
    }


def ensure_new_output_directory(output_dir: Path) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(
            f"Refusing to overwrite non-empty comparison output directory: {output_dir}. "
            "Choose a new versioned --output-dir."
        )
    output_dir.mkdir(parents=True, exist_ok=True)


def load_saved_split_data(
    data_path: Path, split_path: Path
) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    data = pd.read_csv(data_path)
    expression_columns = [column for column in data.columns if column.startswith("expr_")]
    required_data_columns = {
        "sample_id",
        "pCR",
        *CLINICAL_BINARY_COLUMNS,
        TREATMENT_COLUMN,
    }
    missing = required_data_columns.difference(data.columns)
    if missing:
        raise ValueError("ML-ready data are missing columns: " + ", ".join(sorted(missing)))
    if not expression_columns:
        raise ValueError("ML-ready data do not contain expression features.")
    if data["sample_id"].duplicated().any():
        raise ValueError("ML-ready data contain duplicate sample_id values.")

    split = pd.read_csv(split_path)
    required_split_columns = {"sample_id", "pCR", "split"}
    missing = required_split_columns.difference(split.columns)
    if missing:
        raise ValueError("Saved split is missing columns: " + ", ".join(sorted(missing)))
    if split["sample_id"].duplicated().any():
        raise ValueError("Saved split contains duplicate sample_id values.")
    if not split["split"].isin(["train", "test"]).all():
        raise ValueError("Saved split contains unsupported membership labels.")

    selected_columns = [
        "sample_id",
        "pCR",
        *CLINICAL_BINARY_COLUMNS,
        TREATMENT_COLUMN,
        *expression_columns,
    ]
    indexed = data.loc[:, selected_columns].set_index("sample_id", drop=False)
    train_membership = split.loc[split["split"].eq("train"), ["sample_id", "pCR"]]
    test_membership = split.loc[split["split"].eq("test"), ["sample_id", "pCR"]]
    missing_ids = set(split["sample_id"]).difference(indexed.index)
    if missing_ids:
        raise ValueError("Saved split sample IDs are missing from ML-ready data.")
    train = indexed.loc[train_membership["sample_id"]].reset_index(drop=True)
    test = indexed.loc[test_membership["sample_id"]].reset_index(drop=True)
    if not train["pCR"].astype(int).reset_index(drop=True).eq(
        train_membership["pCR"].astype(int).reset_index(drop=True)
    ).all():
        raise ValueError("Training outcomes disagree between split and ML-ready data.")
    if not test["pCR"].astype(int).reset_index(drop=True).eq(
        test_membership["pCR"].astype(int).reset_index(drop=True)
    ).all():
        raise ValueError("Test outcomes disagree between split and ML-ready data.")
    clinical_columns = [*CLINICAL_BINARY_COLUMNS, TREATMENT_COLUMN]
    if train[clinical_columns].isna().any().any() or test[clinical_columns].isna().any().any():
        raise ValueError("Clinical comparison variables contain missing values.")
    unseen_treatments = set(test[TREATMENT_COLUMN]).difference(train[TREATMENT_COLUMN])
    if unseen_treatments:
        raise ValueError(
            "Locked test contains treatment categories absent from training: "
            + ", ".join(sorted(map(str, unseen_treatments)))
        )
    return train, test, expression_columns


def build_model_specs(
    expression_columns: list[str], random_seed: int, max_iter: int
) -> dict[str, tuple[Pipeline, dict[str, list[object]]]]:
    binary_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("scaler", StandardScaler()),
        ]
    )
    treatment_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "one_hot",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )
    clinical_preprocessor = ColumnTransformer(
        [
            ("binary", binary_pipeline, CLINICAL_BINARY_COLUMNS),
            ("treatment", treatment_pipeline, [TREATMENT_COLUMN]),
        ],
        sparse_threshold=0.0,
    )
    clinical_model = Pipeline(
        [
            ("preprocessor", clinical_preprocessor),
            (
                "classifier",
                LogisticRegression(
                    solver="liblinear",
                    class_weight="balanced",
                    max_iter=2_000,
                    random_state=random_seed,
                ),
            ),
        ]
    )

    expression_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    combined_preprocessor = ColumnTransformer(
        [
            ("expression", expression_pipeline, expression_columns),
            ("binary", binary_pipeline, CLINICAL_BINARY_COLUMNS),
            ("treatment", treatment_pipeline, [TREATMENT_COLUMN]),
        ],
        sparse_threshold=0.0,
    )
    combined_model = Pipeline(
        [
            ("preprocessor", combined_preprocessor),
            (
                "classifier",
                LogisticRegression(
                    penalty="elasticnet",
                    solver="saga",
                    class_weight="balanced",
                    max_iter=max_iter,
                    tol=1e-3,
                    random_state=random_seed,
                ),
            ),
        ]
    )
    return {
        "clinical_baseline": (
            clinical_model,
            {
                "classifier__penalty": ["l1", "l2"],
                "classifier__C": [0.01, 0.1, 1.0, 10.0],
            },
        ),
        "clinical_plus_expression": (
            combined_model,
            {
                "classifier__C": [0.03, 0.1],
                "classifier__l1_ratio": [0.2, 0.8],
            },
        ),
    }


def collect_cv_results(model_name: str, grid: GridSearchCV) -> pd.DataFrame:
    results = pd.DataFrame(grid.cv_results_)
    output = pd.DataFrame(
        {
            "model": model_name,
            "params": results["params"].map(lambda value: json.dumps(value, sort_keys=True)),
            "mean_cv_roc_auc": results["mean_test_roc_auc"],
            "std_cv_roc_auc": results["std_test_roc_auc"],
            "rank_cv_roc_auc": results["rank_test_roc_auc"],
            "mean_cv_pr_auc_average_precision": results["mean_test_average_precision"],
            "std_cv_pr_auc_average_precision": results["std_test_average_precision"],
        }
    )
    output["selected"] = output["rank_cv_roc_auc"].eq(1)
    return output


def train_models(
    train: pd.DataFrame,
    expression_columns: list[str],
    cv_folds: int,
    random_seed: int,
    max_iter: int,
    n_jobs: int,
) -> tuple[dict[str, GridSearchCV], pd.DataFrame]:
    validate_n_jobs(n_jobs)
    if cv_folds < 2:
        raise ValueError("cv_folds must be at least 2.")
    y_train = train["pCR"].astype(int).to_numpy()
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_seed)
    scoring = {"roc_auc": "roc_auc", "average_precision": "average_precision"}
    grids: dict[str, GridSearchCV] = {}
    cv_tables = []
    for model_name, (pipeline, parameter_grid) in build_model_specs(
        expression_columns, random_seed, max_iter
    ).items():
        print(f"Training {model_name} on saved training membership...", flush=True)
        grid = GridSearchCV(
            pipeline,
            parameter_grid,
            scoring=scoring,
            refit="roc_auc",
            cv=cv,
            n_jobs=n_jobs,
            return_train_score=False,
            error_score="raise",
            verbose=1,
        )
        grid.fit(train, y_train)
        grids[model_name] = grid
        cv_tables.append(collect_cv_results(model_name, grid))
        print(
            f"Selected {model_name}: {grid.best_params_}; "
            f"training CV AUC={grid.best_score_:.6f}",
            flush=True,
        )
    return grids, pd.concat(cv_tables, ignore_index=True)


def verify_expression_predictions(
    predictions_path: Path,
    test: pd.DataFrame,
    original_metrics_path: Path,
    tolerance: float = 1e-12,
) -> pd.DataFrame:
    predictions = pd.read_csv(predictions_path)
    required = {
        "sample_id",
        "observed_pCR",
        "predicted_pCR_class",
        "predicted_pCR_score",
    }
    missing = required.difference(predictions.columns)
    if missing:
        raise ValueError(
            "Existing expression predictions are missing columns: "
            + ", ".join(sorted(missing))
        )
    if predictions["sample_id"].duplicated().any():
        raise ValueError("Existing expression predictions contain duplicate sample IDs.")
    if set(predictions["sample_id"]) != set(test["sample_id"]):
        raise ValueError("Existing expression predictions do not match locked test membership.")
    aligned = test.loc[:, ["sample_id", "pCR"]].merge(
        predictions, on="sample_id", validate="one_to_one"
    )
    if not aligned["pCR"].astype(int).eq(aligned["observed_pCR"].astype(int)).all():
        raise ValueError("Expression prediction outcomes disagree with locked test labels.")

    observed = aligned["observed_pCR"].astype(int).to_numpy()
    classes = aligned["predicted_pCR_class"].astype(int).to_numpy()
    scores = aligned["predicted_pCR_score"].astype(float).to_numpy()
    tn, fp, fn, tp = confusion_matrix(observed, classes, labels=[0, 1]).ravel()
    recomputed = {
        "roc_auc": float(roc_auc_score(observed, scores)),
        "accuracy": float(accuracy_score(observed, classes)),
        "sensitivity": float(recall_score(observed, classes)),
        "specificity": float(tn / (tn + fp)),
        "precision": float(precision_score(observed, classes, zero_division=0)),
        "f1": float(f1_score(observed, classes, zero_division=0)),
    }
    canonical = pd.read_csv(original_metrics_path)
    if len(canonical) != 1:
        raise ValueError("Canonical expression metrics must contain exactly one row.")
    for metric, actual in recomputed.items():
        expected = float(canonical.loc[0, metric])
        if not np.isclose(actual, expected, rtol=0.0, atol=tolerance):
            raise ValueError(
                f"Existing expression prediction verification failed for {metric}: "
                f"recomputed={actual:.17g}, canonical={expected:.17g}."
            )
    return aligned


def calibration_intercept_slope(
    observed: np.ndarray, predicted_scores: np.ndarray
) -> tuple[float, float]:
    clipped = np.clip(np.asarray(predicted_scores, dtype=float), 1e-15, 1 - 1e-15)
    logits = np.log(clipped / (1 - clipped)).reshape(-1, 1)
    diagnostic_model = LogisticRegression(C=np.inf, solver="lbfgs", max_iter=10_000)
    diagnostic_model.fit(logits, np.asarray(observed, dtype=int))
    return float(diagnostic_model.intercept_[0]), float(diagnostic_model.coef_[0, 0])


def evaluate_scores(
    observed: np.ndarray, predicted_scores: np.ndarray
) -> dict[str, float]:
    observed = np.asarray(observed, dtype=int)
    predicted_scores = np.asarray(predicted_scores, dtype=float)
    intercept, slope = calibration_intercept_slope(observed, predicted_scores)
    return {
        "roc_auc": float(roc_auc_score(observed, predicted_scores)),
        "pr_auc_average_precision": float(
            average_precision_score(observed, predicted_scores)
        ),
        "brier_score": float(brier_score_loss(observed, predicted_scores)),
        "calibration_intercept": intercept,
        "calibration_slope": slope,
        "observed_pCR_rate": float(observed.mean()),
        "mean_predicted_pCR_score": float(predicted_scores.mean()),
        "observed_minus_predicted_rate": float(
            observed.mean() - predicted_scores.mean()
        ),
    }


def derived_seed(base_seed: int, label: str) -> int:
    digest = hashlib.sha256(f"{base_seed}|{label}".encode("utf-8")).digest()
    return int.from_bytes(digest[:4], byteorder="little", signed=False)


def bootstrap_model_confidence_intervals(
    observed: np.ndarray,
    predicted_scores: np.ndarray,
    point_metrics: dict[str, float],
    iterations: int,
    random_seed: int,
) -> pd.DataFrame:
    if iterations < 1:
        raise ValueError("bootstrap_iterations must be at least 1.")
    observed = np.asarray(observed, dtype=int)
    predicted_scores = np.asarray(predicted_scores, dtype=float)
    rng = np.random.default_rng(random_seed)
    estimates: dict[str, list[float]] = {metric: [] for metric in BOOTSTRAP_METRICS}
    for _ in range(iterations):
        indices = rng.integers(0, len(observed), size=len(observed))
        sampled_observed = observed[indices]
        sampled_scores = predicted_scores[indices]
        estimates["brier_score"].append(
            float(brier_score_loss(sampled_observed, sampled_scores))
        )
        if len(np.unique(sampled_observed)) != 2:
            continue
        estimates["roc_auc"].append(
            float(roc_auc_score(sampled_observed, sampled_scores))
        )
        estimates["pr_auc_average_precision"].append(
            float(average_precision_score(sampled_observed, sampled_scores))
        )
        intercept, slope = calibration_intercept_slope(
            sampled_observed, sampled_scores
        )
        estimates["calibration_intercept"].append(intercept)
        estimates["calibration_slope"].append(slope)

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
                "valid_replicates": int(values.size),
                "bootstrap_iterations": iterations,
                "bootstrap_random_seed": random_seed,
                "method": "paired patient-level nonparametric percentile bootstrap",
            }
        )
    return pd.DataFrame(rows)


def bootstrap_pairwise_differences(
    observed: np.ndarray,
    score_by_model: dict[str, np.ndarray],
    iterations: int,
    base_seed: int,
) -> pd.DataFrame:
    pairs = [
        ("clinical_baseline", "expression_model_existing"),
        ("clinical_plus_expression", "expression_model_existing"),
        ("clinical_plus_expression", "clinical_baseline"),
    ]
    rows = []
    observed = np.asarray(observed, dtype=int)
    for model_a, model_b in pairs:
        seed = derived_seed(base_seed, f"{model_a}_minus_{model_b}")
        rng = np.random.default_rng(seed)
        distributions = {"roc_auc": [], "pr_auc_average_precision": []}
        for _ in range(iterations):
            indices = rng.integers(0, len(observed), size=len(observed))
            y_sample = observed[indices]
            if len(np.unique(y_sample)) != 2:
                continue
            score_a = score_by_model[model_a][indices]
            score_b = score_by_model[model_b][indices]
            distributions["roc_auc"].append(
                roc_auc_score(y_sample, score_a) - roc_auc_score(y_sample, score_b)
            )
            distributions["pr_auc_average_precision"].append(
                average_precision_score(y_sample, score_a)
                - average_precision_score(y_sample, score_b)
            )
        for metric, values in distributions.items():
            values_array = np.asarray(values, dtype=float)
            if metric == "roc_auc":
                point_a = roc_auc_score(observed, score_by_model[model_a])
                point_b = roc_auc_score(observed, score_by_model[model_b])
            else:
                point_a = average_precision_score(observed, score_by_model[model_a])
                point_b = average_precision_score(observed, score_by_model[model_b])
            lower, upper = np.percentile(values_array, [2.5, 97.5])
            rows.append(
                {
                    "model_a": model_a,
                    "model_b": model_b,
                    "metric": metric,
                    "difference_a_minus_b": float(point_a - point_b),
                    "ci_lower_95": float(lower),
                    "ci_upper_95": float(upper),
                    "valid_replicates": int(values_array.size),
                    "bootstrap_iterations": iterations,
                    "bootstrap_random_seed": seed,
                    "method": "paired patient-level nonparametric percentile bootstrap",
                }
            )
    return pd.DataFrame(rows)


def calibration_curve_data(
    model_name: str,
    observed: np.ndarray,
    predicted_scores: np.ndarray,
    n_bins: int = 10,
) -> pd.DataFrame:
    frame = pd.DataFrame(
        {
            "observed_pCR": np.asarray(observed, dtype=int),
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
            pCR_count=("observed_pCR", "sum"),
            mean_predicted_pCR_score=("predicted_pCR_score", "mean"),
            observed_pCR_rate=("observed_pCR", "mean"),
        )
        .reset_index()
    )
    curve.insert(0, "model", model_name)
    curve["bin"] = curve["bin"].astype(int) + 1
    return curve


def save_calibration_plot(curves: pd.DataFrame, output_path: Path) -> None:
    colors = {
        "clinical_baseline": "#E67E22",
        "expression_model_existing": "#2F6BFF",
        "clinical_plus_expression": "#2AA876",
    }
    labels = {
        "clinical_baseline": "Clinical baseline",
        "expression_model_existing": "Expression model (existing)",
        "clinical_plus_expression": "Clinical + expression",
    }
    fig, ax = plt.subplots(figsize=(7.2, 6.2), constrained_layout=True)
    ax.plot([0, 1], [0, 1], linestyle="--", color="#5A6573", label="Ideal")
    for model_name in MODEL_ORDER:
        curve = curves.loc[curves["model"].eq(model_name)]
        ax.plot(
            curve["mean_predicted_pCR_score"],
            curve["observed_pCR_rate"],
            marker="o",
            linewidth=2,
            color=colors[model_name],
            label=labels[model_name],
        )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Mean predicted pCR model score (uncalibrated)")
    ax.set_ylabel("Observed pCR rate")
    ax.set_title("GSE194040 locked-test calibration comparison")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper left")
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def write_summary(
    output_dir: Path,
    metrics: pd.DataFrame,
    confidence_intervals: pd.DataFrame,
    pairwise: pd.DataFrame,
    best_params: dict[str, dict[str, object]],
    cv_scores: dict[str, float],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# GSE194040 clinical and expression model comparison (v1)",
        "",
        f"Run timestamp: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Design",
        "",
        "- Clinical baseline and clinical-plus-expression models were tuned and fit using saved training membership only.",
        "- The locked test set was scored once after both specifications and hyperparameter grids were finalized.",
        "- The existing frozen expression-model prediction file was reused without modifying the model or canonical results.",
        "- Calibration intercept and slope are test-set diagnostics only; no calibration mapping was saved or applied.",
        f"- Confidence intervals use {args.bootstrap_iterations} paired patient-level percentile replicates with base seed {args.bootstrap_seed}.",
        "",
        "## Selected training-CV models",
        "",
        f"- Clinical baseline: `{json.dumps(best_params['clinical_baseline'], sort_keys=True)}`; mean training CV AUC {cv_scores['clinical_baseline']:.6f}.",
        f"- Clinical plus expression: `{json.dumps(best_params['clinical_plus_expression'], sort_keys=True)}`; mean training CV AUC {cv_scores['clinical_plus_expression']:.6f}.",
        "",
        "## Locked-test results",
        "",
        "| Model | ROC AUC (95% CI) | PR-AUC (95% CI) | Brier (95% CI) | Calibration intercept (95% CI) | Calibration slope (95% CI) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for model_name in MODEL_ORDER:
        metric_row = metrics.loc[metrics["model"].eq(model_name)].iloc[0]
        ci = confidence_intervals.loc[confidence_intervals["model"].eq(model_name)].set_index("metric")
        cells = []
        for metric in BOOTSTRAP_METRICS:
            cells.append(
                f"{metric_row[metric]:.3f} ({ci.loc[metric, 'ci_lower_95']:.3f}-{ci.loc[metric, 'ci_upper_95']:.3f})"
            )
        lines.append(f"| {model_name} | " + " | ".join(cells) + " |")
    lines.extend(
        [
            "",
            "## Paired discrimination differences",
            "",
            "Positive values favor model A. Intervals containing zero do not demonstrate a difference on this locked test sample.",
            "",
            "| Model A | Model B | Metric | Difference (95% CI) |",
            "|---|---|---|---:|",
        ]
    )
    for row in pairwise.itertuples(index=False):
        lines.append(
            f"| {row.model_a} | {row.model_b} | {row.metric} | "
            f"{row.difference_a_minus_b:.3f} ({row.ci_lower_95:.3f}-{row.ci_upper_95:.3f}) |"
        )
    lines.extend(
        [
            "",
            "All outputs are internal single-split estimates. Model scores remain uncalibrated and must not be interpreted as clinical probabilities. The comparison is not external validation and does not establish clinical utility.",
        ]
    )
    (output_dir / SUMMARY_FILENAME).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    validate_n_jobs(args.n_jobs)
    ensure_new_output_directory(args.output_dir)
    train, test, expression_columns = load_saved_split_data(args.data, args.split)
    expression_predictions = verify_expression_predictions(
        args.expression_predictions, test, args.original_metrics
    )

    grids, cv_results = train_models(
        train,
        expression_columns,
        args.cv_folds,
        args.random_seed,
        args.max_iter,
        args.n_jobs,
    )
    joblib.dump(
        grids["clinical_baseline"].best_estimator_,
        args.output_dir / CLINICAL_MODEL_FILENAME,
    )
    joblib.dump(
        grids["clinical_plus_expression"].best_estimator_,
        args.output_dir / COMBINED_MODEL_FILENAME,
    )
    cv_results.to_csv(args.output_dir / CV_RESULTS_FILENAME, index=False)

    observed = test["pCR"].astype(int).to_numpy()
    expression_scores = expression_predictions["predicted_pCR_score"].astype(float).to_numpy()
    print("Scoring the locked test set once for each finalized new model...", flush=True)
    clinical_scores = grids["clinical_baseline"].best_estimator_.predict_proba(test)[:, 1]
    combined_scores = grids["clinical_plus_expression"].best_estimator_.predict_proba(test)[:, 1]
    score_by_model = {
        "clinical_baseline": np.asarray(clinical_scores, dtype=float),
        "expression_model_existing": np.asarray(expression_scores, dtype=float),
        "clinical_plus_expression": np.asarray(combined_scores, dtype=float),
    }

    predictions = pd.DataFrame(
        {
            "sample_id": test["sample_id"],
            "observed_pCR": observed,
            "clinical_baseline_pCR_score": clinical_scores,
            "expression_model_existing_pCR_score": expression_scores,
            "clinical_plus_expression_pCR_score": combined_scores,
        }
    )
    predictions.to_csv(args.output_dir / PREDICTIONS_FILENAME, index=False)

    metric_rows = []
    ci_tables = []
    curve_tables = []
    for model_name in MODEL_ORDER:
        point_metrics = evaluate_scores(observed, score_by_model[model_name])
        metric_rows.append(
            {
                "model": model_name,
                "n": len(observed),
                "pCR_count": int(observed.sum()),
                "model_source": (
                    "existing_locked_predictions"
                    if model_name == "expression_model_existing"
                    else "new_training_only_cv_pipeline"
                ),
                **point_metrics,
            }
        )
        ci = bootstrap_model_confidence_intervals(
            observed,
            score_by_model[model_name],
            point_metrics,
            args.bootstrap_iterations,
            derived_seed(args.bootstrap_seed, model_name),
        )
        ci.insert(0, "model", model_name)
        ci_tables.append(ci)
        curve_tables.append(
            calibration_curve_data(model_name, observed, score_by_model[model_name])
        )
    metrics = pd.DataFrame(metric_rows)
    confidence_intervals = pd.concat(ci_tables, ignore_index=True)
    curves = pd.concat(curve_tables, ignore_index=True)
    pairwise = bootstrap_pairwise_differences(
        observed, score_by_model, args.bootstrap_iterations, args.bootstrap_seed
    )
    metrics.to_csv(args.output_dir / METRICS_FILENAME, index=False)
    confidence_intervals.to_csv(args.output_dir / CI_FILENAME, index=False)
    pairwise.to_csv(args.output_dir / PAIRWISE_FILENAME, index=False)
    curves.to_csv(args.output_dir / CURVE_FILENAME, index=False)
    save_calibration_plot(curves, args.output_dir / PLOT_FILENAME)

    best_params = {name: grid.best_params_ for name, grid in grids.items()}
    cv_scores = {name: float(grid.best_score_) for name, grid in grids.items()}
    write_summary(
        args.output_dir,
        metrics,
        confidence_intervals,
        pairwise,
        best_params,
        cv_scores,
        args,
    )
    session = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "python": sys.version,
        "platform": platform.platform(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "sklearn": sys.modules["sklearn"].__version__,
        "data_path": portable_package_path(args.data),
        "split_path": portable_package_path(args.split),
        "expression_predictions_path": portable_package_path(
            args.expression_predictions
        ),
        "original_metrics_path": portable_package_path(args.original_metrics),
        "output_dir": portable_package_path(args.output_dir),
        "training_rows": len(train),
        "locked_test_rows": len(test),
        "expression_feature_count": len(expression_columns),
        "clinical_variables": [*CLINICAL_BINARY_COLUMNS, TREATMENT_COLUMN],
        "cv_folds": args.cv_folds,
        "training_random_seed": args.random_seed,
        "bootstrap_iterations": args.bootstrap_iterations,
        "bootstrap_base_seed": args.bootstrap_seed,
        "best_params": best_params,
        "best_cv_roc_auc": cv_scores,
        "model_convergence_status": {
            name: logistic_convergence_status(grid.best_estimator_)
            for name, grid in grids.items()
        },
        "locked_test_scored_once_after_selection": True,
        "test_data_used_for_training_or_tuning": False,
        "calibration_mapping_saved_or_applied": False,
        "existing_expression_results_replaced": False,
    }
    (args.output_dir / SESSION_FILENAME).write_text(
        json.dumps(session, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote clinical/expression comparison to {args.output_dir}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from None
