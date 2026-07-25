"""Train ML models for GSE194040 pCR prediction from pretreatment expression.

Leakage controls:
- The existing locked stratified train/test membership is loaded first.
- The test set is used once, after model selection.
- Missingness filtering, imputation, variance filtering, scaling, supervised
  feature selection, PCA, and model fitting all
  live inside sklearn Pipelines, so CV folds fit preprocessing on training-fold
  data only.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.base import BaseEstimator, TransformerMixin, clone
from sklearn.calibration import CalibratedClassifierCV
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, VarianceThreshold, f_classif
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    auc,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


METRIC_COLUMNS = [
    "roc_auc",
    "f1",
    "sensitivity",
    "specificity",
    "precision",
    "accuracy",
]
RANDOM_STATE = 42
DEFAULT_OUTPUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "evaluation"
    / "gse194040_leakage_corrected_training_v1_20260719"
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
        description="Train and compare GSE194040 pCR prediction models."
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=PROJECT_ROOT / "data_processed" / "gse194040_ml_ready_pcr_expression.csv",
        help="ML-ready CSV with pCR target and expr_* features.",
    )
    parser.add_argument(
        "--split",
        type=Path,
        default=PROJECT_ROOT / "results" / "tables" / "gse194040_train_test_split.csv",
        help="Saved locked train/test membership; read but never rewritten.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="New versioned output directory; non-empty directories are rejected.",
    )
    parser.add_argument("--cv-folds", type=int, default=3)
    parser.add_argument("--random-state", type=int, default=RANDOM_STATE)
    parser.add_argument(
        "--n-jobs",
        type=int,
        default=1,
        help="GridSearchCV parallel jobs. Keep low on memory-constrained machines.",
    )
    parser.add_argument(
        "--max-iter",
        type=int,
        default=1500,
        help="Maximum iterations for saga logistic regression models.",
    )
    parser.add_argument("--max-missing-rate", type=float, default=0.20)
    parser.add_argument("--variance-threshold", type=float, default=1e-8)
    return parser.parse_args()


def validate_n_jobs(n_jobs: int) -> int:
    """Validate sklearn job semantics while rejecting the invalid value zero."""
    if n_jobs == 0 or n_jobs < -1:
        raise ValueError("n_jobs must be -1 or a positive integer.")
    return n_jobs


class MissingnessFilter(BaseEstimator, TransformerMixin):
    """Drop features whose missing rate exceeds a threshold learned in fit()."""

    def __init__(self, max_missing_rate: float = 0.20) -> None:
        self.max_missing_rate = max_missing_rate

    def fit(self, X: Any, y: Any = None) -> "MissingnessFilter":
        if not 0 <= self.max_missing_rate <= 1:
            raise ValueError("max_missing_rate must be between 0 and 1.")
        values = np.asarray(X)
        if values.ndim != 2:
            raise ValueError("MissingnessFilter requires a two-dimensional matrix.")
        self.n_features_in_ = values.shape[1]
        if hasattr(X, "columns"):
            self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        self.missing_rates_ = np.asarray(pd.isna(values).mean(axis=0), dtype=float)
        self.support_ = self.missing_rates_ <= self.max_missing_rate
        if not self.support_.any():
            raise ValueError("MissingnessFilter removed every feature.")
        return self

    def transform(self, X: Any) -> Any:
        values = np.asarray(X)
        if values.ndim != 2 or values.shape[1] != self.n_features_in_:
            raise ValueError("Input feature count does not match MissingnessFilter fit data.")
        if hasattr(X, "iloc"):
            return X.iloc[:, self.support_]
        return values[:, self.support_]

    def get_support(self) -> np.ndarray:
        return self.support_.copy()

    def get_feature_names_out(self, input_features: Any = None) -> np.ndarray:
        if input_features is None:
            input_features = getattr(
                self,
                "feature_names_in_",
                np.asarray(
                    [f"x{i}" for i in range(self.n_features_in_)], dtype=object
                ),
            )
        features = np.asarray(input_features, dtype=object)
        return features[self.support_]


def expression_preprocessing_steps(
    max_missing_rate: float,
    variance_threshold: float,
    scale: bool,
) -> list[tuple[str, Any]]:
    steps: list[tuple[str, Any]] = [
        ("missingness", MissingnessFilter(max_missing_rate=max_missing_rate)),
        ("imputer", SimpleImputer(strategy="median")),
        ("variance", VarianceThreshold(threshold=variance_threshold)),
    ]
    if scale:
        steps.append(("scaler", StandardScaler()))
    return steps


def ensure_new_output_directory(output_dir: Path) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(
            f"Refusing to overwrite non-empty corrected training directory: {output_dir}. "
            "Choose a new versioned --output-dir."
        )
    output_dir.mkdir(parents=True, exist_ok=True)


def specificity_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    tn, fp, _fn, _tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    denom = tn + fp
    return float(tn / denom) if denom else 0.0


def scorer_dict() -> dict[str, Any]:
    from sklearn.metrics import make_scorer

    return {
        "roc_auc": "roc_auc",
        "f1": make_scorer(f1_score, zero_division=0),
        "sensitivity": make_scorer(recall_score, zero_division=0),
        "specificity": make_scorer(specificity_score),
        "precision": make_scorer(precision_score, zero_division=0),
        "accuracy": "accuracy",
    }


def get_positive_scores(estimator: Any, X: pd.DataFrame) -> np.ndarray:
    if hasattr(estimator, "predict_proba"):
        proba = estimator.predict_proba(X)
        return proba[:, 1]
    if hasattr(estimator, "decision_function"):
        scores = estimator.decision_function(X)
        return np.asarray(scores)
    return estimator.predict(X)


def build_model_specs(
    random_state: int,
    max_iter: int,
    max_missing_rate: float = 0.20,
    variance_threshold: float = 1e-8,
) -> dict[str, tuple[Pipeline, dict[str, list[Any]]]]:
    lasso = Pipeline(
        steps=expression_preprocessing_steps(
            max_missing_rate, variance_threshold, scale=True
        ) + [
            (
                "classifier",
                LogisticRegression(
                    penalty="l1",
                    solver="saga",
                    class_weight="balanced",
                    max_iter=max_iter,
                    tol=1e-3,
                    random_state=random_state,
                ),
            ),
        ]
    )

    elastic_net = Pipeline(
        steps=expression_preprocessing_steps(
            max_missing_rate, variance_threshold, scale=True
        ) + [
            (
                "classifier",
                LogisticRegression(
                    penalty="elasticnet",
                    solver="saga",
                    class_weight="balanced",
                    max_iter=max_iter,
                    tol=1e-3,
                    random_state=random_state,
                ),
            ),
        ]
    )

    random_forest = Pipeline(
        steps=expression_preprocessing_steps(
            max_missing_rate, variance_threshold, scale=False
        ) + [
            ("select", SelectKBest(score_func=f_classif, k=3000)),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=200,
                    class_weight="balanced_subsample",
                    random_state=random_state,
                    # GridSearchCV owns parallelism so nested all-core pools are avoided.
                    n_jobs=1,
                ),
            ),
        ]
    )

    svm_estimator = LinearSVCCompat(random_state=random_state)
    linear_svm = Pipeline(
        steps=expression_preprocessing_steps(
            max_missing_rate, variance_threshold, scale=True
        ) + [
            ("select", SelectKBest(score_func=f_classif, k=5000)),
            (
                "classifier",
                CalibratedClassifierCV(
                    estimator=svm_estimator,
                    method="sigmoid",
                    cv=3,
                ),
            ),
        ]
    )

    pca_logistic = Pipeline(
        steps=expression_preprocessing_steps(
            max_missing_rate, variance_threshold, scale=True
        ) + [
            (
                "pca",
                PCA(
                    svd_solver="randomized",
                    random_state=random_state,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    penalty="l2",
                    solver="lbfgs",
                    class_weight="balanced",
                    max_iter=2000,
                    random_state=random_state,
                ),
            ),
        ]
    )

    return {
        "lasso_logistic_l1": (
            lasso,
            {"classifier__C": [0.01, 0.03, 0.1]},
        ),
        "elastic_net_logistic": (
            elastic_net,
            {
                "classifier__C": [0.03, 0.1],
                "classifier__l1_ratio": [0.2, 0.8],
            },
        ),
        "random_forest": (
            random_forest,
            {
                "classifier__max_features": ["sqrt", 0.10],
                "classifier__min_samples_leaf": [1, 5],
            },
        ),
        "linear_svm_calibrated": (
            linear_svm,
            {"classifier__estimator__C": [0.01, 0.1, 1.0]},
        ),
        "pca_logistic": (
            pca_logistic,
            {
                "pca__n_components": [25, 50],
                "classifier__C": [0.1, 1.0],
            },
        ),
    }


def LinearSVCCompat(random_state: int) -> Any:
    from sklearn.svm import LinearSVC

    return LinearSVC(
        C=0.1,
        class_weight="balanced",
        dual="auto",
        max_iter=5000,
        random_state=random_state,
    )


def model_convergence_records(model_name: str, estimator: Any) -> list[dict[str, Any]]:
    """Report fitted iterative-estimator status without suppressing warnings."""
    classifier = (
        estimator.named_steps.get("classifier")
        if hasattr(estimator, "named_steps")
        else estimator
    )
    records: list[dict[str, Any]] = []
    seen: set[int] = set()

    def visit(candidate: Any, path: str) -> None:
        if candidate is None or id(candidate) in seen:
            return
        seen.add(id(candidate))
        if hasattr(candidate, "n_iter_") and hasattr(candidate, "max_iter"):
            iterations = np.asarray(candidate.n_iter_, dtype=int).ravel()
            max_iter = int(candidate.max_iter)
            observed_max = int(iterations.max()) if iterations.size else 0
            records.append(
                {
                    "model": model_name,
                    "estimator_path": path,
                    "estimator_class": type(candidate).__name__,
                    "status": (
                        "converged_before_max_iter"
                        if observed_max < max_iter
                        else "reached_max_iter_review_warning"
                    ),
                    "n_iter": iterations.tolist(),
                    "observed_max_iter": observed_max,
                    "configured_max_iter": max_iter,
                }
            )
        for index, calibrated in enumerate(
            getattr(candidate, "calibrated_classifiers_", [])
        ):
            visit(
                getattr(calibrated, "estimator", None),
                f"{path}.calibrated_classifiers_[{index}].estimator",
            )

    visit(classifier, "classifier")
    if not records:
        records.append(
            {
                "model": model_name,
                "estimator_path": "classifier",
                "estimator_class": type(classifier).__name__,
                "status": "not_applicable_non_iterative_estimator",
                "n_iter": None,
                "observed_max_iter": None,
                "configured_max_iter": getattr(classifier, "max_iter", None),
            }
        )
    return records


def summarize_best_grid(model_name: str, grid: GridSearchCV) -> dict[str, Any]:
    best_idx = int(grid.best_index_)
    row: dict[str, Any] = {
        "model": model_name,
        "best_params": json.dumps(grid.best_params_, sort_keys=True),
        "selection_refit_metric": grid.refit,
    }
    for metric in METRIC_COLUMNS:
        row[f"cv_mean_{metric}"] = float(grid.cv_results_[f"mean_test_{metric}"][best_idx])
        row[f"cv_std_{metric}"] = float(grid.cv_results_[f"std_test_{metric}"][best_idx])
    return row


def collect_full_grid_results(model_name: str, grid: GridSearchCV) -> pd.DataFrame:
    cols = ["params"]
    for metric in METRIC_COLUMNS:
        cols.extend([f"mean_test_{metric}", f"std_test_{metric}", f"rank_test_{metric}"])
    available = [col for col in cols if col in grid.cv_results_]
    df = pd.DataFrame({col: grid.cv_results_[col] for col in available})
    df.insert(0, "model", model_name)
    df["params"] = df["params"].apply(lambda value: json.dumps(value, sort_keys=True))
    return df


def choose_best_model(comparison: pd.DataFrame) -> str:
    ranked = comparison.sort_values(
        by=["cv_mean_roc_auc", "cv_mean_f1", "cv_mean_sensitivity"],
        ascending=[False, False, False],
        kind="mergesort",
    )
    return str(ranked.iloc[0]["model"])


def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray, y_score: np.ndarray) -> dict[str, float]:
    return {
        "roc_auc": float(roc_auc_score(y_true, y_score)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "sensitivity": float(recall_score(y_true, y_pred, zero_division=0)),
        "specificity": float(specificity_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
    }


def save_gene_coefficients(
    estimator: Pipeline,
    feature_cols: list[str],
    output_path: Path,
    model_name: str,
    threshold: float = 1e-8,
) -> int:
    classifier = estimator.named_steps["classifier"]
    transformed_feature_cols = estimator[:-1].get_feature_names_out(feature_cols)
    coef = np.asarray(classifier.coef_).ravel()
    if len(transformed_feature_cols) != len(coef):
        raise ValueError("Filtered feature names do not align with coefficients.")
    coef_df = pd.DataFrame(
        {
            "model": model_name,
            "feature_name": transformed_feature_cols,
            "gene_symbol": [
                str(col).replace("expr_", "", 1)
                for col in transformed_feature_cols
            ],
            "coefficient": coef,
            "abs_coefficient": np.abs(coef),
        }
    )
    selected = coef_df.loc[coef_df["abs_coefficient"] > threshold].copy()
    selected = selected.sort_values("abs_coefficient", ascending=False)
    selected.to_csv(output_path, index=False)
    return int(len(selected))


def plot_confusion(y_true: np.ndarray, y_pred: np.ndarray, title: str, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(5.5, 4.8))
    display = ConfusionMatrixDisplay.from_predictions(
        y_true,
        y_pred,
        labels=[0, 1],
        display_labels=["non-pCR", "pCR"],
        cmap="Blues",
        values_format="d",
        ax=ax,
    )
    display.ax_.set_title(title)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def plot_roc(y_true: np.ndarray, y_score: np.ndarray, title: str, output_path: Path) -> None:
    fpr, tpr, _thresholds = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)
    fig, ax = plt.subplots(figsize=(5.5, 4.8))
    ax.plot(fpr, tpr, color="#1f77b4", linewidth=2, label=f"AUC = {roc_auc:.3f}")
    ax.plot([0, 1], [0, 1], color="#777777", linewidth=1, linestyle="--")
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate / sensitivity")
    ax.set_title(title)
    ax.legend(loc="lower right")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def write_summary(
    path: Path,
    best_model_name: str,
    comparison: pd.DataFrame,
    test_metrics: pd.DataFrame,
    lasso_selected_n: int,
    elastic_selected_n: int,
    feature_count: int,
    train_n: int,
    test_n: int,
    max_missing_rate: float,
    variance_threshold: float,
    features_after_missingness: int,
    features_after_variance: int,
) -> None:
    best_cv = comparison.loc[comparison["model"] == best_model_name].iloc[0]
    test = test_metrics.iloc[0]
    lines = [
        "# GSE194040 pCR model training summary",
        "",
        f"Run timestamp: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Data and split",
        f"- Features: {feature_count} pretreatment `expr_*` gene-expression columns.",
        f"- Target: `pCR` (1 = pathological complete response, 0 = no pCR).",
        f"- Training rows: {train_n}; untouched test rows: {test_n}.",
        "- Metadata columns were excluded from features: `sample_id`, `patient_id`, `HR`, `HER2`, `MP`, `treatment_arm`, `gsm`, and `platform`.",
        "",
        "## Model selection",
        f"- Best model by cross-validated AUC, then F1, then sensitivity: `{best_model_name}`.",
        f"- Best-model CV AUC: {best_cv['cv_mean_roc_auc']:.3f} +/- {best_cv['cv_std_roc_auc']:.3f}.",
        f"- Best-model CV F1: {best_cv['cv_mean_f1']:.3f} +/- {best_cv['cv_std_f1']:.3f}.",
        f"- Best-model CV sensitivity: {best_cv['cv_mean_sensitivity']:.3f} +/- {best_cv['cv_std_sensitivity']:.3f}.",
        "",
        "## Untouched test performance",
        f"- AUC: {test['roc_auc']:.3f}",
        f"- F1: {test['f1']:.3f}",
        f"- Sensitivity/recall: {test['sensitivity']:.3f}",
        f"- Specificity: {test['specificity']:.3f}",
        f"- Precision: {test['precision']:.3f}",
        f"- Accuracy: {test['accuracy']:.3f}",
        "",
        "## Sparse logistic model-selected gene features",
        f"- LASSO non-zero genes: {lasso_selected_n}",
        f"- Elastic Net non-zero genes: {elastic_selected_n}",
        "",
        "## Leakage controls and limitations",
        f"- Missingness filtering (> {max_missing_rate:.2%}), median imputation, variance filtering (<= {variance_threshold:g}), scaling, supervised feature selection, PCA, and classifier fitting were all inside sklearn pipelines and therefore fit separately within each training fold.",
        f"- Final selected pipeline retained {features_after_missingness} features after its training-only missingness filter and {features_after_variance} after its training-only variance filter.",
        "- The final test set was evaluated once after choosing the model from training-set CV.",
        "- This is a single random split of a modest-size high-dimensional cohort; external validation and fold-specific biological stability checks are still needed before interpreting model-selected genes biologically.",
        "- Remaining sparse expression missingness is handled by median imputation inside each training fold or final training pipeline.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    validate_n_jobs(args.n_jobs)
    ensure_new_output_directory(args.output_dir)
    output_tables = args.output_dir / "tables"
    output_figures = args.output_dir / "figures"
    output_models = args.output_dir / "models"
    output_logs = args.output_dir / "logs"
    for directory in [output_tables, output_figures, output_models, output_logs]:
        directory.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.data)
    feature_cols = [col for col in df.columns if col.startswith("expr_")]
    metadata_cols = [
        col
        for col in df.columns
        if col not in feature_cols and col != "pCR"
    ]
    if df["sample_id"].duplicated().any():
        raise ValueError("ML-ready data contain duplicate sample_id values.")
    split_df = pd.read_csv(args.split)
    required_split_columns = {"sample_id", "pCR", "split"}
    missing_split_columns = required_split_columns.difference(split_df.columns)
    if missing_split_columns:
        raise ValueError(
            "Saved split is missing columns: "
            + ", ".join(sorted(missing_split_columns))
        )
    if split_df["sample_id"].duplicated().any():
        raise ValueError("Saved split contains duplicate sample_id values.")
    indexed = df.set_index("sample_id", drop=False)
    if set(split_df["sample_id"]) != set(indexed.index):
        raise ValueError("Saved split membership does not exactly match ML-ready data.")
    train_membership = split_df.loc[split_df["split"].eq("train")]
    test_membership = split_df.loc[split_df["split"].eq("test")]
    train_rows = indexed.loc[train_membership["sample_id"]]
    test_rows = indexed.loc[test_membership["sample_id"]]
    if not np.array_equal(
        train_rows["pCR"].astype(int).to_numpy(),
        train_membership["pCR"].astype(int).to_numpy(),
    ):
        raise ValueError("Training outcomes disagree between data and saved split.")
    if not np.array_equal(
        test_rows["pCR"].astype(int).to_numpy(),
        test_membership["pCR"].astype(int).to_numpy(),
    ):
        raise ValueError("Test outcomes disagree between data and saved split.")
    X_train = train_rows.loc[:, feature_cols]
    X_test = test_rows.loc[:, feature_cols]
    y_train = train_rows["pCR"].astype(int).to_numpy()
    y_test = test_rows["pCR"].astype(int).to_numpy()

    cv = StratifiedKFold(
        n_splits=args.cv_folds,
        shuffle=True,
        random_state=args.random_state,
    )
    specs = build_model_specs(
        args.random_state,
        args.max_iter,
        args.max_missing_rate,
        args.variance_threshold,
    )

    fitted_grids: dict[str, GridSearchCV] = {}
    comparison_rows: list[dict[str, Any]] = []
    full_grid_rows: list[pd.DataFrame] = []
    convergence_records: list[dict[str, Any]] = []
    scoring = scorer_dict()

    print(f"Loaded {len(df)} rows, {len(feature_cols)} expression features.", flush=True)
    print(f"Excluded metadata columns: {metadata_cols}", flush=True)
    print(f"Training rows: {len(X_train)}; test rows: {len(X_test)}", flush=True)

    for model_name, (pipeline, param_grid) in specs.items():
        print(f"\n=== Training {model_name} ===", flush=True)
        grid = GridSearchCV(
            estimator=pipeline,
            param_grid=param_grid,
            scoring=scoring,
            refit="roc_auc",
            cv=cv,
            n_jobs=args.n_jobs,
            verbose=2,
            return_train_score=False,
            error_score="raise",
        )
        grid.fit(X_train, y_train)
        fitted_grids[model_name] = grid
        comparison_rows.append(summarize_best_grid(model_name, grid))
        full_grid_rows.append(collect_full_grid_results(model_name, grid))
        convergence_records.extend(
            model_convergence_records(model_name, grid.best_estimator_)
        )
        joblib.dump(grid.best_estimator_, output_models / f"gse194040_{model_name}_best_pipeline.joblib")

    comparison = pd.DataFrame(comparison_rows)
    comparison = comparison.sort_values(
        by=["cv_mean_roc_auc", "cv_mean_f1", "cv_mean_sensitivity"],
        ascending=[False, False, False],
        kind="mergesort",
    )
    comparison.to_csv(output_tables / "gse194040_cv_model_comparison.csv", index=False)
    pd.concat(full_grid_rows, ignore_index=True).to_csv(
        output_tables / "gse194040_cv_grid_results.csv", index=False
    )
    convergence_path = output_logs / "gse194040_model_convergence_status.json"
    convergence_path.write_text(
        json.dumps(convergence_records, indent=2) + "\n", encoding="utf-8"
    )

    best_model_name = choose_best_model(comparison)
    best_estimator = fitted_grids[best_model_name].best_estimator_
    features_after_missingness = int(
        best_estimator.named_steps["missingness"].get_support().sum()
    )
    features_after_variance = int(
        best_estimator.named_steps["variance"].get_support().sum()
    )
    y_test_pred = best_estimator.predict(X_test)
    y_test_score = get_positive_scores(best_estimator, X_test)
    test_metrics = pd.DataFrame(
        [
            {
                "model": best_model_name,
                "best_params": json.dumps(fitted_grids[best_model_name].best_params_, sort_keys=True),
                **evaluate_predictions(y_test, y_test_pred, y_test_score),
            }
        ]
    )
    test_metrics.to_csv(output_tables / "gse194040_final_test_metrics.csv", index=False)

    joblib.dump(best_estimator, output_models / "gse194040_best_model.joblib")
    model_info = {
        "best_model": best_model_name,
        "best_params": fitted_grids[best_model_name].best_params_,
        "random_state": args.random_state,
        "split_path": portable_package_path(args.split),
        "cv_folds": args.cv_folds,
        "feature_count": len(feature_cols),
        "max_missing_rate": args.max_missing_rate,
        "variance_threshold": args.variance_threshold,
        "features_after_training_missingness_filter": features_after_missingness,
        "features_after_training_variance_filter": features_after_variance,
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "convergence_status": [
            row for row in convergence_records if row["model"] == best_model_name
        ],
    }
    (output_models / "gse194040_best_model_metadata.json").write_text(
        json.dumps(model_info, indent=2), encoding="utf-8"
    )

    lasso_selected_n = save_gene_coefficients(
        fitted_grids["lasso_logistic_l1"].best_estimator_,
        feature_cols,
        output_tables / "gse194040_lasso_selected_genes_coefficients.csv",
        "lasso_logistic_l1",
    )
    elastic_selected_n = save_gene_coefficients(
        fitted_grids["elastic_net_logistic"].best_estimator_,
        feature_cols,
        output_tables / "gse194040_elastic_net_selected_genes_coefficients.csv",
        "elastic_net_logistic",
    )

    plot_confusion(
        y_test,
        y_test_pred,
        f"{best_model_name} test confusion matrix",
        output_figures / "gse194040_final_confusion_matrix.png",
    )
    plot_roc(
        y_test,
        y_test_score,
        f"{best_model_name} test ROC curve",
        output_figures / "gse194040_final_roc_curve.png",
    )

    write_summary(
        args.output_dir / "gse194040_model_training_summary.md",
        best_model_name,
        comparison,
        test_metrics,
        lasso_selected_n,
        elastic_selected_n,
        len(feature_cols),
        len(X_train),
        len(X_test),
        args.max_missing_rate,
        args.variance_threshold,
        features_after_missingness,
        features_after_variance,
    )

    session_info = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "python": sys.version,
        "platform": platform.platform(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "sklearn": sklearn.__version__,
        "matplotlib": matplotlib.__version__,
        "joblib": joblib.__version__,
        "argv": sys.argv,
        "split_path": portable_package_path(args.split),
        "output_dir": portable_package_path(args.output_dir),
        "max_missing_rate": args.max_missing_rate,
        "variance_threshold": args.variance_threshold,
        "preprocessing_fit_inside_cv_pipelines": True,
        "canonical_outputs_overwritten": False,
        "convergence_warnings_globally_suppressed": False,
        "convergence_status_path": portable_package_path(convergence_path),
        "n_jobs": args.n_jobs,
        "parallelism_policy": "GridSearchCV uses n_jobs; nested estimators use one job",
    }
    (output_logs / "gse194040_model_training_session_info.json").write_text(
        json.dumps(session_info, indent=2), encoding="utf-8"
    )

    print("\n=== Best model ===")
    print(best_model_name)
    print("\n=== CV comparison ===")
    print(comparison.to_string(index=False))
    print("\n=== Final untouched test metrics ===")
    print(test_metrics.to_string(index=False))
    print(f"\nLASSO selected genes: {lasso_selected_n}")
    print(f"Elastic Net selected genes: {elastic_selected_n}")


if __name__ == "__main__":
    main()
