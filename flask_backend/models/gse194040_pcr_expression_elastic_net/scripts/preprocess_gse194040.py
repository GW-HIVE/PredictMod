"""Prepare GSE194040 I-SPY2 pretreatment expression data for ML.

The GEO supplementary expression matrix is already normalized, log2 transformed,
gene-level collapsed, and platform/batch adjusted by the data submitters. This
script therefore focuses on orientation, clinical label parsing, merge, and
descriptive QC. Statistical feature filtering is deferred to training pipelines.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import os
import platform
import re
import sys
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


GEO_BASE = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194040"
EXPRESSION_FILE = (
    "GSE194040_ISPY2ResID_AgilentGeneExp_990_FrshFrzn_meanCol_geneLevel_n988.txt.gz"
)
SERIES_FILES = [
    "GSE194040-GPL20078_series_matrix.txt.gz",
    "GSE194040-GPL30493_series_matrix.txt.gz",
]
CLINICAL_COLUMNS = ["HR", "HER2", "MP", "pCR", "treatment_arm"]
ID_COLUMNS = ["sample_id", "patient_id", "gsm", "platform"]


def portable_project_path(path: Path, project_root: Path) -> str:
    """Return a POSIX path relative to the package root."""
    try:
        relative = os.path.relpath(path.resolve(), project_root.resolve())
    except ValueError:
        return path.name
    return Path(relative).as_posix()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an ML-ready pCR prediction table from GSE194040."
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project root containing the GSE194040 folder.",
    )
    parser.add_argument(
        "--max-missing-rate",
        type=float,
        default=0.20,
        help="Missingness threshold recorded for downstream training pipelines.",
    )
    parser.add_argument(
        "--near-zero-variance-threshold",
        type=float,
        default=1e-8,
        help="Variance threshold recorded for downstream training pipelines.",
    )
    parser.add_argument(
        "--download-missing",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Download required GEO files from NCBI HTTPS if they are absent locally.",
    )
    return parser.parse_args()


def ensure_input_files(raw_dir: Path, download_missing: bool) -> dict[str, Path]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    expected = {
        "expression": raw_dir / EXPRESSION_FILE,
        "GPL20078_series_matrix": raw_dir / SERIES_FILES[0],
        "GPL30493_series_matrix": raw_dir / SERIES_FILES[1],
    }
    urls = {
        expected["expression"]: f"{GEO_BASE}/suppl/{EXPRESSION_FILE}",
        expected["GPL20078_series_matrix"]: f"{GEO_BASE}/matrix/{SERIES_FILES[0]}",
        expected["GPL30493_series_matrix"]: f"{GEO_BASE}/matrix/{SERIES_FILES[1]}",
    }

    missing = [path for path in expected.values() if not path.exists()]
    if missing and not download_missing:
        missing_list = "\n".join(str(path) for path in missing)
        raise FileNotFoundError(f"Missing required input files:\n{missing_list}")

    for path in missing:
        print(f"Downloading {path.name} ...")
        urllib.request.urlretrieve(urls[path], path)

    return expected


def parse_quoted_tab_line(line: str) -> list[str]:
    return [value.strip().strip('"') for value in next(csv.reader([line], delimiter="\t"))]


def clean_key(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def normalize_patient_id(value: str) -> str:
    value = str(value).strip().replace("ISPY2_", "")
    return re.sub(r"-GPL\d+$", "", value)


def infer_platform(path: Path) -> str:
    match = re.search(r"GPL\d+", path.name)
    return match.group(0) if match else ""


def parse_series_matrix(path: Path) -> pd.DataFrame:
    sample_titles: list[str] | None = None
    gsm_ids: list[str] | None = None
    characteristic_rows: list[list[str]] = []

    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            if raw_line.startswith("!series_matrix_table_begin"):
                break
            line = raw_line.rstrip("\n")
            if line.startswith("!Sample_title"):
                sample_titles = parse_quoted_tab_line(line)[1:]
            elif line.startswith("!Sample_geo_accession"):
                gsm_ids = parse_quoted_tab_line(line)[1:]
            elif line.startswith("!Sample_characteristics_ch1"):
                characteristic_rows.append(parse_quoted_tab_line(line)[1:])

    if sample_titles is None or gsm_ids is None:
        raise ValueError(f"Could not parse sample titles/accessions from {path}")

    if len(sample_titles) != len(gsm_ids):
        raise ValueError(f"Sample title/accession length mismatch in {path}")

    records: list[dict[str, str]] = []
    for idx, title in enumerate(sample_titles):
        patient_id = normalize_patient_id(title)
        record: dict[str, str] = {
            "sample_id": title,
            "patient_id": patient_id,
            "gsm": gsm_ids[idx],
            "platform": infer_platform(path),
        }
        for row in characteristic_rows:
            if idx >= len(row) or ":" not in row[idx]:
                continue
            key, value = row[idx].split(":", 1)
            record[clean_key(key)] = value.strip()
        records.append(record)

    meta = pd.DataFrame.from_records(records)
    rename = {
        "hr": "HR",
        "her2": "HER2",
        "mp": "MP",
        "pcr": "pCR",
        "arm": "treatment_arm",
        "adjustment_method": "adjustment_method",
    }
    meta = meta.rename(columns=rename)
    for col in ["HR", "HER2", "MP", "pCR"]:
        if col in meta.columns:
            meta[col] = pd.to_numeric(meta[col], errors="coerce").astype("Int64")
    return meta


def make_unique(values: Iterable[str]) -> list[str]:
    counts: Counter[str] = Counter()
    unique_values: list[str] = []
    for value in values:
        counts[value] += 1
        if counts[value] == 1:
            unique_values.append(value)
        else:
            unique_values.append(f"{value}__dup{counts[value]}")
    return unique_values


def sanitize_feature_name(gene_symbol: str, used: set[str]) -> str:
    base = re.sub(r"[^A-Za-z0-9_.-]+", "_", gene_symbol.strip())
    base = base.strip("_") or "unknown_gene"
    candidate = f"expr_{base}"
    suffix = 2
    while candidate in used:
        candidate = f"expr_{base}__{suffix}"
        suffix += 1
    used.add(candidate)
    return candidate


def read_expression_matrix(path: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, object]]:
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
        sample_ids = handle.readline().rstrip("\n").split("\t")

    internal_sample_cols = make_unique(sample_ids)
    raw = pd.read_csv(
        path,
        sep="\t",
        compression="gzip",
        skiprows=1,
        header=None,
        names=["gene_symbol", *internal_sample_cols],
        na_values=["", "NA", "NaN", "nan", "NULL", "null"],
        low_memory=False,
    )

    duplicate_genes = raw["gene_symbol"].duplicated().sum()
    used_features: set[str] = set()
    feature_names = [sanitize_feature_name(str(gene), used_features) for gene in raw["gene_symbol"]]
    feature_manifest = pd.DataFrame(
        {
            "feature_name": feature_names,
            "gene_symbol": raw["gene_symbol"].astype(str),
        }
    )

    values = raw.drop(columns=["gene_symbol"]).apply(pd.to_numeric, errors="coerce")
    values.index = feature_names
    expression_by_sample = values.T
    expression_by_sample.index.name = "expression_column_id"
    expression_by_sample = expression_by_sample.reset_index()

    sample_map = pd.DataFrame(
        {
            "expression_column_id": internal_sample_cols,
            "patient_id": [normalize_patient_id(sample_id) for sample_id in sample_ids],
            "expression_sample_id": [f"ISPY2_{sample_id}" for sample_id in sample_ids],
        }
    )
    expression_by_sample = sample_map.merge(expression_by_sample, on="expression_column_id")

    feature_cols = feature_manifest["feature_name"].tolist()
    expression_by_patient = (
        expression_by_sample.groupby("patient_id", sort=False)[feature_cols]
        .mean(numeric_only=True)
        .reset_index()
    )
    expression_by_patient.insert(0, "sample_id", "ISPY2_" + expression_by_patient["patient_id"])

    stats = {
        "expression_orientation": "genes_rows_samples_columns",
        "expression_gene_rows_raw": int(raw.shape[0]),
        "expression_sample_columns_raw": int(len(sample_ids)),
        "expression_unique_patients": int(expression_by_patient["patient_id"].nunique()),
        "expression_duplicate_sample_ids": int(len(sample_ids) - len(set(sample_ids))),
        "expression_duplicate_patient_ids": int(
            len(sample_map) - sample_map["patient_id"].nunique()
        ),
        "expression_duplicate_gene_symbols": int(duplicate_genes),
        "expression_min_row_fields_expected": int(len(sample_ids) + 1),
    }
    return expression_by_patient, feature_manifest, stats


def collapse_metadata_to_patient(metadata: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    duplicate_rows = metadata[metadata["patient_id"].duplicated(keep=False)].copy()
    duplicate_reports: list[dict[str, object]] = []

    def collapse_group(group: pd.DataFrame) -> pd.Series:
        out: dict[str, object] = {"patient_id": group.name}
        for col in metadata.columns:
            if col == "patient_id":
                continue
            values = [value for value in group[col].dropna().astype(str).tolist() if value != ""]
            unique_values = list(dict.fromkeys(values))
            if len(unique_values) > 1:
                duplicate_reports.append(
                    {
                        "patient_id": group.name,
                        "field": col,
                        "values": "; ".join(unique_values),
                    }
                )
            if col == "sample_id":
                out[col] = f"ISPY2_{group.name}"
            elif col in {"gsm", "platform"}:
                out[col] = "; ".join(unique_values) if unique_values else pd.NA
            else:
                out[col] = unique_values[0] if unique_values else pd.NA
        out["sample_id"] = f"ISPY2_{group.name}"
        return pd.Series(out)

    collapsed = metadata.groupby("patient_id", sort=False).apply(
        collapse_group, include_groups=False
    )
    collapsed = collapsed.reset_index(drop=True)
    duplicate_report = pd.DataFrame(duplicate_reports)
    if duplicate_report.empty:
        duplicate_report = pd.DataFrame(columns=["patient_id", "field", "values"])
    duplicate_report.insert(0, "issue", "duplicate_patient_metadata_conflict")

    if not duplicate_rows.empty:
        duplicate_rows.insert(0, "issue", "duplicate_patient_metadata_row")
        duplicate_rows = duplicate_rows.astype(str)
        duplicate_report = pd.concat([duplicate_rows, duplicate_report], ignore_index=True)

    for col in ["HR", "HER2", "MP", "pCR"]:
        if col in collapsed.columns:
            collapsed[col] = pd.to_numeric(collapsed[col], errors="coerce").astype("Int64")
    return collapsed, duplicate_report


def value_counts_table(df: pd.DataFrame, column: str) -> pd.DataFrame:
    counts = (
        df[column]
        .astype("string")
        .fillna("<missing>")
        .value_counts(dropna=False)
        .rename_axis(column)
        .reset_index(name="n")
    )
    counts["fraction"] = counts["n"] / counts["n"].sum()
    return counts


def write_data_dictionary(path: Path, n_features: int) -> None:
    rows = [
        {
            "column": "sample_id",
            "type": "string",
            "description": "ISPY2 sample identifier in the form ISPY2_<patient_id>.",
        },
        {
            "column": "patient_id",
            "type": "string",
            "description": "Numeric I-SPY2 patient/sample identifier used to merge GEO metadata and expression.",
        },
        {
            "column": "pCR",
            "type": "integer target",
            "description": "Pathological complete response label; 1 = complete response, 0 = no complete response.",
        },
        {
            "column": "HR",
            "type": "integer metadata",
            "description": "Hormone receptor status; 1 = positive, 0 = negative.",
        },
        {
            "column": "HER2",
            "type": "integer metadata",
            "description": "HER2 status; 1 = positive, 0 = negative.",
        },
        {
            "column": "MP",
            "type": "integer metadata",
            "description": "MammaPrint risk; 0 = high risk 1 (MP1), 1 = ultra/high risk 2 (MP2).",
        },
        {
            "column": "treatment_arm",
            "type": "string metadata",
            "description": "Neoadjuvant I-SPY2 treatment arm from GEO sample characteristics.",
        },
        {
            "column": "gsm",
            "type": "string metadata",
            "description": "GEO sample accession from the series matrix.",
        },
        {
            "column": "platform",
            "type": "string metadata",
            "description": "Agilent platform series matrix source, GPL20078 or GPL30493.",
        },
        {
            "column": "expr_*",
            "type": f"{n_features} numeric gene-expression features",
            "description": "Pretreatment normalized log2 Agilent gene-expression values; see gse194040_gene_feature_manifest.csv for feature-to-gene mapping.",
        },
    ]
    pd.DataFrame(rows).to_csv(path, index=False)


def main() -> None:
    args = parse_args()
    root = args.project_root
    input_dir = root / "GSE194040"
    data_raw = root / "data_raw"
    data_processed = root / "data_processed"
    tables_dir = root / "results" / "tables"
    logs_dir = root / "logs"

    for directory in [data_raw, data_processed, tables_dir, logs_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    paths = ensure_input_files(input_dir, args.download_missing)

    metadata_parts = [
        parse_series_matrix(paths["GPL20078_series_matrix"]),
        parse_series_matrix(paths["GPL30493_series_matrix"]),
    ]
    metadata_raw = pd.concat(metadata_parts, ignore_index=True, sort=False)
    metadata_raw.to_csv(data_raw / "gse194040_metadata_from_series_matrix.csv", index=False)

    metadata, duplicate_report = collapse_metadata_to_patient(metadata_raw)
    metadata.to_csv(data_processed / "gse194040_metadata_clean.csv", index=False)

    expression, feature_manifest, expression_stats = read_expression_matrix(paths["expression"])
    feature_manifest.to_csv(data_processed / "gse194040_gene_feature_manifest.csv", index=False)
    expression.to_csv(data_processed / "gse194040_expression_transposed_by_patient.csv", index=False)

    feature_cols = feature_manifest["feature_name"].tolist()
    merged = metadata.merge(
        expression.drop(columns=["sample_id"]),
        on="patient_id",
        how="inner",
        validate="one_to_one",
    )
    if "sample_id" not in merged.columns:
        merged.insert(0, "sample_id", "ISPY2_" + merged["patient_id"].astype(str))

    exclusions: list[dict[str, object]] = []
    metadata_only = sorted(set(metadata["patient_id"]) - set(expression["patient_id"]))
    expression_only = sorted(set(expression["patient_id"]) - set(metadata["patient_id"]))
    for patient_id in metadata_only:
        exclusions.append({"patient_id": patient_id, "reason": "metadata_without_expression"})
    for patient_id in expression_only:
        exclusions.append({"patient_id": patient_id, "reason": "expression_without_metadata"})

    missing_pcr_mask = merged["pCR"].isna()
    for patient_id in merged.loc[missing_pcr_mask, "patient_id"]:
        exclusions.append({"patient_id": patient_id, "reason": "missing_pCR"})
    merged = merged.loc[~missing_pcr_mask].copy()

    all_expression_missing_mask = merged[feature_cols].isna().all(axis=1)
    feature_missing = merged[feature_cols].isna().mean()
    all_variances = merged[feature_cols].var(axis=0, skipna=True, ddof=0)
    full_cohort_missingness_flags = feature_missing > args.max_missing_rate
    full_cohort_variance_flags = (
        all_variances <= args.near_zero_variance_threshold
    )

    # Retain every gene and patient here. Statistical missingness and variance
    # filters are learned only from training data inside each model/CV pipeline.
    final_feature_cols = feature_cols
    final_columns = [
        "sample_id",
        "patient_id",
        "pCR",
        "HR",
        "HER2",
        "MP",
        "treatment_arm",
        "gsm",
        "platform",
        *final_feature_cols,
    ]
    for col in final_columns:
        if col not in merged.columns:
            merged[col] = pd.NA
    final = merged[final_columns].copy()

    final.to_csv(data_processed / "gse194040_ml_ready_pcr_expression.csv", index=False)

    removed_features = pd.DataFrame(columns=["feature_name", "reason"])
    removed_features.to_csv(data_processed / "gse194040_removed_gene_features.csv", index=False)

    feature_qc = feature_manifest.copy()
    feature_qc["missing_rate"] = feature_qc["feature_name"].map(feature_missing)
    feature_qc["variance"] = feature_qc["feature_name"].map(all_variances)
    feature_qc["full_cohort_missingness_above_pipeline_threshold"] = (
        feature_qc["feature_name"].map(full_cohort_missingness_flags).fillna(False)
    )
    feature_qc["full_cohort_variance_at_or_below_pipeline_threshold"] = (
        feature_qc["feature_name"].map(full_cohort_variance_flags).fillna(False)
    )
    feature_qc["retained"] = True
    feature_qc["removal_reason"] = ""
    feature_qc.to_csv(tables_dir / "gse194040_gene_feature_qc.csv", index=False)

    exclusions_df = pd.DataFrame(exclusions)
    if exclusions_df.empty:
        exclusions_df = pd.DataFrame(columns=["patient_id", "reason"])
    duplicate_report.to_csv(data_processed / "gse194040_duplicate_samples_or_patients.csv", index=False)
    exclusions_df.to_csv(data_processed / "gse194040_exclusions.csv", index=False)

    for col in ["pCR", "HR", "HER2", "MP", "treatment_arm"]:
        value_counts_table(final, col).to_csv(
            tables_dir / f"gse194040_{col.lower()}_distribution.csv", index=False
        )

    qc_rows = [
        {"metric": "expression_orientation", "value": expression_stats["expression_orientation"]},
        {"metric": "expression_gene_rows_raw", "value": expression_stats["expression_gene_rows_raw"]},
        {"metric": "expression_sample_columns_raw", "value": expression_stats["expression_sample_columns_raw"]},
        {"metric": "expression_unique_patients_after_duplicate_aggregation", "value": expression_stats["expression_unique_patients"]},
        {"metric": "metadata_rows_raw", "value": len(metadata_raw)},
        {"metric": "metadata_unique_patients", "value": metadata["patient_id"].nunique()},
        {"metric": "merged_patients_before_label_expression_drops", "value": len(metadata.merge(expression, on="patient_id", how="inner"))},
        {"metric": "final_patients", "value": len(final)},
        {"metric": "initial_gene_features", "value": len(feature_cols)},
        {"metric": "removed_gene_features_before_split", "value": 0},
        {"metric": "full_cohort_genes_above_pipeline_missingness_threshold", "value": int(full_cohort_missingness_flags.sum())},
        {"metric": "full_cohort_genes_at_or_below_pipeline_variance_threshold", "value": int(full_cohort_variance_flags.sum())},
        {"metric": "final_gene_features", "value": len(final_feature_cols)},
        {"metric": "max_missing_rate_threshold", "value": args.max_missing_rate},
        {"metric": "near_zero_variance_threshold", "value": args.near_zero_variance_threshold},
        {"metric": "remaining_missing_expression_values", "value": int(final[final_feature_cols].isna().sum().sum())},
        {"metric": "patients_with_all_expression_missing_retained_for_pipeline", "value": int(all_expression_missing_mask.sum())},
        {"metric": "duplicate_expression_sample_ids", "value": expression_stats["expression_duplicate_sample_ids"]},
        {"metric": "duplicate_expression_patient_ids_after_normalization", "value": expression_stats["expression_duplicate_patient_ids"]},
        {"metric": "duplicate_gene_symbols_raw", "value": expression_stats["expression_duplicate_gene_symbols"]},
        {"metric": "metadata_duplicate_patient_rows", "value": int(metadata_raw["patient_id"].duplicated(keep=False).sum())},
    ]
    qc_summary = pd.DataFrame(qc_rows)
    qc_summary.to_csv(tables_dir / "gse194040_qc_summary.csv", index=False)

    write_data_dictionary(
        data_processed / "gse194040_data_dictionary.csv", len(final_feature_cols)
    )

    summary_lines = [
        "# GSE194040 preprocessing summary",
        "",
        f"Run timestamp: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Input files",
        f"- Expression: `{portable_project_path(paths['expression'], root)}`",
        f"- Series matrix: `{portable_project_path(paths['GPL20078_series_matrix'], root)}`",
        f"- Series matrix: `{portable_project_path(paths['GPL30493_series_matrix'], root)}`",
        "",
        "## Structure confirmed",
        "- The expression file has genes as rows and ISPY2 numeric sample/patient IDs as columns.",
        "- The matrix was transposed and duplicate patient/sample IDs were aggregated by the mean expression value to enforce one row per patient.",
        "- Clinical labels were parsed from GEO `Sample_characteristics_ch1` fields and merged by numeric ISPY2 patient ID.",
        "",
        "## Final dataset",
        f"- Rows/patients: {len(final)}",
        f"- Gene-expression features retained before splitting: {len(final_feature_cols)} of {len(feature_cols)}",
        "- Genes removed before splitting for missingness or variance: 0",
        f"- Full-cohort genes above the downstream missingness threshold ({args.max_missing_rate:.2%}), descriptive only: {int(full_cohort_missingness_flags.sum())}",
        f"- Full-cohort genes at or below the downstream variance threshold ({args.near_zero_variance_threshold:g}), descriptive only: {int(full_cohort_variance_flags.sum())}",
        f"- Remaining missing expression values: {int(final[final_feature_cols].isna().sum().sum())}",
        "",
        "## Leakage note",
        "- No statistical gene filtering is applied before the train/test split.",
        "- Missingness filtering, imputation, variance filtering, scaling, supervised feature selection, PCA, and model fitting are fit inside each training fold by the training script.",
        "",
        "## Main outputs",
        "- `data_processed/gse194040_ml_ready_pcr_expression.csv`",
        "- `data_processed/gse194040_data_dictionary.csv`",
        "- `data_processed/gse194040_gene_feature_manifest.csv`",
        "- `results/tables/gse194040_qc_summary.csv`",
        "- `results/tables/gse194040_gene_feature_qc.csv`",
    ]
    (data_processed / "gse194040_preprocessing_summary.md").write_text(
        "\n".join(summary_lines) + "\n", encoding="utf-8"
    )

    session_info = {
        "python": sys.version,
        "platform": platform.platform(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "argv": sys.argv,
    }
    (logs_dir / "gse194040_session_info.json").write_text(
        json.dumps(session_info, indent=2), encoding="utf-8"
    )

    print("Wrote final ML-ready dataset:")
    print(data_processed / "gse194040_ml_ready_pcr_expression.csv")
    print(qc_summary.to_string(index=False))


if __name__ == "__main__":
    main()
