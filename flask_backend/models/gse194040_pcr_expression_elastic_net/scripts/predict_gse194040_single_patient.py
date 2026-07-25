"""Predict pCR for one GSE194040-style patient row.

Input CSV requirements:
- Exactly one row.
- Contains the same expr_* gene-expression columns used during model training.
- Contains unique column names and numeric, finite gene-expression values.
- Has no more than 20% missing required gene-expression values.
- May contain extra metadata columns; they are ignored except identifiers are
  copied to the output when present.

The class values returned by ``predict_proba`` are exposed as uncalibrated
model scores. They are not clinical probabilities or calibrated risk estimates.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import joblib
import numpy as np
import pandas as pd


DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "gse194040_best_model.joblib"
ID_COLUMNS = ["sample_id", "patient_id"]
SUPPORTED_INPUT_SUFFIXES = {".csv"}
MAX_MISSING_FRACTION = 0.20


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run single-patient pCR prediction using the trained GSE194040 model."
    )
    parser.add_argument("input_csv", type=Path, help="Input CSV containing one patient row.")
    parser.add_argument("output_csv", type=Path, help="Output CSV for prediction results.")
    parser.add_argument(
        "--model",
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help=f"Saved sklearn model path. Default: {DEFAULT_MODEL_PATH}",
    )
    return parser.parse_args()


def get_expected_features(model: object) -> list[str]:
    if hasattr(model, "feature_names_in_"):
        return [str(feature) for feature in model.feature_names_in_]
    raise AttributeError(
        "The loaded model does not expose feature_names_in_; cannot safely align input columns."
    )


def get_class_score(model: object, aligned: pd.DataFrame, class_label: int) -> float:
    if not hasattr(model, "predict_proba"):
        raise AttributeError("The loaded model does not support predict_proba.")
    raw_scores = model.predict_proba(aligned)[0]
    classes = list(getattr(model, "classes_", []))
    if class_label not in classes:
        raise ValueError(f"Class {class_label} was not found in model classes: {classes}")
    return float(raw_scores[classes.index(class_label)])


def validate_csv_header(input_path: Path) -> None:
    suffix = input_path.suffix.lower()
    if suffix not in SUPPORTED_INPUT_SUFFIXES:
        supported = ", ".join(sorted(SUPPORTED_INPUT_SUFFIXES))
        displayed_suffix = suffix or "<none>"
        raise ValueError(
            f"Unsupported input format '{displayed_suffix}'. Supported format: {supported}."
        )

    try:
        with input_path.open(newline="", encoding="utf-8-sig") as handle:
            header = next(csv.reader(handle, strict=True), None)
    except (UnicodeError, csv.Error) as exc:
        raise ValueError(f"Unsupported or malformed CSV input: {exc}") from exc

    if not header:
        raise ValueError("Unsupported or empty input: expected a CSV header row.")

    duplicate_columns = [
        name for name, count in Counter(header).items() if count > 1
    ]
    if duplicate_columns:
        preview = ", ".join(repr(name) for name in duplicate_columns[:25])
        more = (
            ""
            if len(duplicate_columns) <= 25
            else f" ... and {len(duplicate_columns) - 25} more"
        )
        raise ValueError(f"Input CSV contains duplicate columns: {preview}{more}")


def read_patient_csv(input_path: Path) -> pd.DataFrame:
    validate_csv_header(input_path)
    try:
        return pd.read_csv(input_path)
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeError) as exc:
        raise ValueError(f"Unsupported or malformed CSV input: {exc}") from exc


def validate_patient_input(
    input_df: pd.DataFrame,
    expected_features: list[str],
) -> pd.DataFrame:
    if len(input_df) != 1:
        raise ValueError(
            f"Expected exactly one patient/sample row, but found {len(input_df)} rows."
        )

    missing_features = [
        feature for feature in expected_features if feature not in input_df.columns
    ]
    if missing_features:
        preview = ", ".join(missing_features[:25])
        more = (
            ""
            if len(missing_features) <= 25
            else f" ... and {len(missing_features) - 25} more"
        )
        raise ValueError(
            "Input CSV is missing required gene-expression columns: "
            f"{preview}{more}"
        )

    raw_features = input_df.loc[:, expected_features]
    aligned = raw_features.apply(pd.to_numeric, errors="coerce")

    nonnumeric_mask = raw_features.notna() & aligned.isna()
    if nonnumeric_mask.any(axis=None):
        invalid_features = [
            feature for feature in expected_features if nonnumeric_mask.at[0, feature]
        ]
        preview = ", ".join(invalid_features[:25])
        more = (
            ""
            if len(invalid_features) <= 25
            else f" ... and {len(invalid_features) - 25} more"
        )
        raise ValueError(
            "Input CSV contains nonnumeric gene-expression values in: "
            f"{preview}{more}"
        )

    infinite_mask = np.isinf(aligned.to_numpy(dtype=float))
    if infinite_mask.any():
        invalid_features = [
            expected_features[index]
            for index in np.flatnonzero(infinite_mask[0])[:25]
        ]
        preview = ", ".join(invalid_features)
        total = int(infinite_mask.sum())
        more = "" if total <= 25 else f" ... and {total - 25} more"
        raise ValueError(
            "Input CSV contains infinite gene-expression values in: "
            f"{preview}{more}"
        )

    missing_count = int(aligned.isna().sum(axis=1).iloc[0])
    feature_count = len(expected_features)
    if missing_count == feature_count:
        raise ValueError("All required gene-expression values are missing.")

    missing_fraction = missing_count / feature_count
    if missing_fraction > MAX_MISSING_FRACTION:
        raise ValueError(
            "Input CSV has excessive missing gene-expression values: "
            f"{missing_count} of {feature_count} ({missing_fraction:.1%}); "
            f"maximum allowed is {MAX_MISSING_FRACTION:.0%}."
        )

    return aligned


def run_prediction() -> None:
    args = parse_args()

    input_df = read_patient_csv(args.input_csv)
    if len(input_df) != 1:
        raise ValueError(
            f"Expected exactly one patient/sample row, but found {len(input_df)} rows."
        )

    model = joblib.load(args.model)
    expected_features = get_expected_features(model)
    aligned = validate_patient_input(input_df, expected_features)
    predicted_class = int(model.predict(aligned)[0])
    pcr_score = get_class_score(model, aligned, 1)
    non_pcr_score = get_class_score(model, aligned, 0)

    output = {
        "predicted_pCR_class": predicted_class,
        "predicted_pCR_score": pcr_score,
        "predicted_non_pCR_score": non_pcr_score,
    }
    for col in ID_COLUMNS:
        if col in input_df.columns:
            output[col] = input_df.loc[input_df.index[0], col]

    ordered_cols = [
        *[col for col in ID_COLUMNS if col in output],
        "predicted_pCR_class",
        "predicted_pCR_score",
        "predicted_non_pCR_score",
    ]
    result = pd.DataFrame([{col: output[col] for col in ordered_cols}])
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output_csv, index=False)
    print(f"Wrote prediction to {args.output_csv}")


if __name__ == "__main__":
    try:
        run_prediction()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from None
