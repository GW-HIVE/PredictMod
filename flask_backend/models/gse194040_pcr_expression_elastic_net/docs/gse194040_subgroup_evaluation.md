# GSE194040 Locked Test Subgroup Evaluation

This analysis describes frozen-model performance within prespecified clinical and treatment metadata groups on the existing 198-patient locked test set. It uses the versioned locked predictions and does not load, retrain, recalibrate, or tune the model.

## Reproduce

```powershell
python scripts\analyze_gse194040_subgroups.py
```

The script reads:

- `results/evaluation/gse194040_locked_test_evaluation_v2_20260719/gse194040_locked_test_predictions_v2.csv`
- `results/tables/gse194040_train_test_split.csv`
- `data_processed/gse194040_ml_ready_pcr_expression.csv`
- `results/tables/gse194040_final_test_metrics.csv`

Before subgroup estimation, sample membership and outcomes must agree across the locked predictions, saved split, and processed data. The six overall discrimination and classification metrics must also reproduce the canonical metrics within `1e-12`.

## Reporting Rules

- HR/HER2 groups are the four combinations of the saved binary `HR` and `HER2` fields.
- MP groups are reported as the saved `MP=0` and `MP=1` encodings.
- Treatment arms are estimated only when n≥10 with at least three pCR and three non-pCR patients.
- Any estimated subgroup with n<30 is explicitly marked `exploratory_small_sample`.
- Groups that do not meet the reporting rule retain sample and outcome counts, but performance estimates are left blank.
- ROC AUC, sensitivity, and specificity 95% confidence intervals use 2,000 paired patient-level nonparametric percentile bootstrap replicates with base seed `20260719`. A deterministic group-specific seed derived from that base seed makes every group reproducible and order-independent.

## Results

| Family | Subgroup | n | pCR | ROC AUC (95% CI) | Sensitivity (95% CI) | Specificity (95% CI) | Status |
|---|---|---:|---:|---:|---:|---:|---|
| HR/HER2 | HR-/HER2- | 66 | 28 | 0.696 (0.563–0.820) | 0.750 (0.576–0.913) | 0.605 (0.444–0.758) | Reported |
| HR/HER2 | HR-/HER2+ | 15 | 6 | 0.519 (0.178–0.852) | 0.833 (0.500–1.000) | 0.111 (0.000–0.364) | Exploratory |
| HR/HER2 | HR+/HER2- | 74 | 13 | 0.812 (0.659–0.938) | 0.385 (0.125–0.667) | 0.918 (0.845–0.983) | Reported |
| HR/HER2 | HR+/HER2+ | 43 | 17 | 0.855 (0.723–0.960) | 0.882 (0.714–1.000) | 0.692 (0.517–0.862) | Reported |
| MP status | MP=0 | 119 | 25 | 0.818 (0.712–0.915) | 0.680 (0.484–0.864) | 0.830 (0.747–0.903) | Reported |
| MP status | MP=1 | 79 | 39 | 0.658 (0.531–0.774) | 0.744 (0.605–0.875) | 0.500 (0.343–0.659) | Reported |
| Treatment | Paclitaxel | 40 | 8 | 0.750 (0.513–0.928) | 0.750 (0.400–1.000) | 0.750 (0.586–0.893) | Reported |
| Treatment | Paclitaxel + ABT 888 + Carboplatin | 15 | 5 | 0.700 (0.385–0.940) | 0.800 (0.333–1.000) | 0.600 (0.273–0.900) | Exploratory |
| Treatment | Paclitaxel + AMG 386 | 15 | 6 | 0.907 (0.727–1.000) | 0.500 (0.000–1.000) | 1.000 (1.000–1.000) | Exploratory |
| Treatment | Paclitaxel + Ganetespib | 11 | 3 | 0.667 (0.000–1.000) | 0.667 (0.000–1.000) | 0.875 (0.600–1.000) | Exploratory |
| Treatment | Paclitaxel + Ganitumab | 18 | 4 | 0.875 (0.667–1.000) | 0.750 (0.000–1.000) | 0.786 (0.545–1.000) | Exploratory |
| Treatment | Paclitaxel + MK-2206 | 15 | 4 | 0.773 (0.429–1.000) | 0.500 (0.000–1.000) | 0.909 (0.700–1.000) | Exploratory |
| Treatment | Paclitaxel + Neratinib | 31 | 12 | 0.693 (0.504–0.863) | 0.667 (0.385–0.917) | 0.526 (0.300–0.750) | Reported |
| Treatment | Paclitaxel + Pembrolizumab | 15 | 6 | 0.907 (0.700–1.000) | 0.667 (0.250–1.000) | 0.889 (0.625–1.000) | Exploratory |
| Treatment | T-DM1 + Pertuzumab | 12 | 7 | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | 1.000 (1.000–1.000) | Exploratory |

Treatment arms not estimated were Paclitaxel + AMG 386 + Trastuzumab (n=5, pCR=1), Paclitaxel + MK-2206 + Trastuzumab (n=5, pCR=1), Paclitaxel + Pertuzumab + Trastuzumab (n=9, pCR=4), and Paclitaxel + Trastuzumab (n=7, pCR=3).

## Interpretation Limits

These are internal descriptive subgroup estimates from one locked test split. Many intervals are wide, and apparent differences between subgroups can reflect sampling variation. The analysis does not test interactions, estimate treatment effects, establish treatment-arm superiority, or provide external validation. Perfect estimates in very small groups are especially unstable and remain explicitly exploratory.

## Versioned Outputs

- `results/evaluation/gse194040_locked_test_subgroups_v1_20260719/gse194040_locked_test_subgroup_metrics_v1.csv`
- `results/evaluation/gse194040_locked_test_subgroups_v1_20260719/gse194040_locked_test_subgroup_summary_v1.md`
- `results/evaluation/gse194040_locked_test_subgroups_v1_20260719/gse194040_locked_test_subgroup_session_v1.json`
