# Package Manifest

The submission package contains 120 files. The full processed training CSV,
downloaded GEO archives, Git LFS rules, generated Python and pytest caches,
volunteership reporting, symposium material, and package-audit documentation
are intentionally excluded.

## Top-level inventory

| Path | File count | Contents |
|---|---:|---|
| `bco/` | 1 | IEEE 2791 BioCompute Object |
| `data_processed/` | 7 | Data dictionaries, manifests, and preprocessing records |
| `docs/` | 7 | Technical model and analysis documentation |
| `examples/` | 1 | Single-patient example input |
| `logs/` | 2 | Preprocessing and model-training session information |
| `models/` | 7 | Frozen model pipelines and selected-model metadata |
| `results/` | 60 | Tables, figures, evaluations, and validation records |
| `schemas/` | 9 | Vendored IEEE 2791 v1.4 schemas |
| `scripts/` | 9 | Preprocessing, training, evaluation, validation, and prediction code |
| `tests/` | 6 | Automated test modules |
| Package-root files | 11 | README, manifest, citation, licensing, dependency, Docker, and pytest configuration |

## Required completion-criteria files

| Requirement | Included path |
|---|---|
| Historical training-dataset provenance | `data_processed/gse194040_preprocessing_summary.md` and `results/reproducibility/gse194040_reproducibility_manifest_v1_20260719.json` |
| Model training | `scripts/train_gse194040_models.py` |
| Single-patient prediction | `scripts/predict_gse194040_single_patient.py` |
| Example patient input | `examples/gse194040_single_patient_input_example.csv` |
| Example prediction output | `results/tables/gse194040_single_patient_prediction_example_v2_uncalibrated_score.csv` |
| Frozen selected model | `models/gse194040_best_model.joblib` |
| BioCompute Object | `bco/gse194040_pcr_pipeline_bco_v1.json` |

## Reproducibility and deployment

- Citation metadata: `CITATION.cff`
- Licence scope and unresolved terms: `LICENSES.md`
- Third-party inventory: `THIRD_PARTY_NOTICES.md`
- Exact Python packages: `requirements-lock.txt`
- Direct dependencies: `requirements.txt`
- Conda environment: `environment.yml`
- Docker build: `Dockerfile`
- Docker exclusions: `.dockerignore`
- Large-data policy: processed training data and downloaded GEO archives are recreated with `scripts/preprocess_gse194040.py`; no package Git LFS rules remain
- Automated tests: `tests/`
- IEEE 2791 v1.4 schemas: `schemas/ieee-2791-v1.4/`
- BCO validation: `scripts/validate_gse194040_bco.py`

## Outputs

- Canonical model summary: `results/gse194040_model_training_summary.md`
- Tables: `results/tables/`
- Figures: `results/figures/`
- Locked evaluation and confidence intervals: `results/evaluation/`
- Calibration diagnostics: `results/calibration/`
- Reproducibility manifest: `results/reproducibility/`
- Test and BCO validation records: `results/validation/`

## Included technical documentation

- `docs/gse194040_bco_pipeline_documentation.md`
- `docs/gse194040_calibration_analysis.md`
- `docs/gse194040_clinical_model_comparison.md`
- `docs/gse194040_preprocessing_leakage_audit.md`
- `docs/gse194040_reproducibility.md`
- `docs/gse194040_single_patient_prediction_usage.md`
- `docs/gse194040_subgroup_evaluation.md`

## Intentional exclusions

- `.pytest_cache/`
- `scripts/__pycache__/`
- `tests/__pycache__/`
- `docs/gse194040_volunteership_report.md`
- `docs/gse194040_symposium_slide_outline.md`
- `docs/gse194040_final_project_verification.md`
- `docs/gse194040_package_audit.md`
- `data_processed/gse194040_ml_ready_pcr_expression.csv`
- `GSE194040/`
- `.gitattributes`

## Scope

This package contains the canonical pooled full-cohort model. The separate
Paclitaxel-only analysis is not a replacement production model and is excluded
pending a project-lead decision on whether it should be a documented
supplement.
