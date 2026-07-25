# GSE194040 locked test subgroup evaluation (v1)

Run timestamp: 2026-07-19T21:46:26

## Design

- Uses only the existing versioned locked-test predictions; the trained model is not loaded or refit.
- Bootstrap: 2000 paired patient-level percentile replicates with base seed 20260719.
- Treatment arms require n >= 10 and at least 3 patients in each outcome class.
- Any estimated subgroup with n < 30 is marked exploratory.
- ROC AUC, sensitivity, and specificity confidence intervals are internal descriptive estimates, not external validation.

## Estimated subgroups

| Family | Subgroup | n | pCR | ROC AUC (95% CI) | Sensitivity (95% CI) | Specificity (95% CI) | Status |
|---|---|---:|---:|---:|---:|---:|---|
| HR_HER2 | HR-/HER2- | 66 | 28 | 0.696 (0.563-0.820) | 0.750 (0.576-0.913) | 0.605 (0.444-0.758) | reported |
| HR_HER2 | HR-/HER2+ | 15 | 6 | 0.519 (0.178-0.852) | 0.833 (0.500-1.000) | 0.111 (0.000-0.364) | exploratory_small_sample |
| HR_HER2 | HR+/HER2- | 74 | 13 | 0.812 (0.659-0.938) | 0.385 (0.125-0.667) | 0.918 (0.845-0.983) | reported |
| HR_HER2 | HR+/HER2+ | 43 | 17 | 0.855 (0.723-0.960) | 0.882 (0.714-1.000) | 0.692 (0.517-0.862) | reported |
| MP_status | MP=0 | 119 | 25 | 0.818 (0.712-0.915) | 0.680 (0.484-0.864) | 0.830 (0.747-0.903) | reported |
| MP_status | MP=1 | 79 | 39 | 0.658 (0.531-0.774) | 0.744 (0.605-0.875) | 0.500 (0.343-0.659) | reported |
| treatment_arm | Paclitaxel | 40 | 8 | 0.750 (0.513-0.928) | 0.750 (0.400-1.000) | 0.750 (0.586-0.893) | reported |
| treatment_arm | Paclitaxel + ABT 888 + Carboplatin | 15 | 5 | 0.700 (0.385-0.940) | 0.800 (0.333-1.000) | 0.600 (0.273-0.900) | exploratory_small_sample |
| treatment_arm | Paclitaxel + AMG 386 | 15 | 6 | 0.907 (0.727-1.000) | 0.500 (0.000-1.000) | 1.000 (1.000-1.000) | exploratory_small_sample |
| treatment_arm | Paclitaxel + Ganetespib | 11 | 3 | 0.667 (0.000-1.000) | 0.667 (0.000-1.000) | 0.875 (0.600-1.000) | exploratory_small_sample |
| treatment_arm | Paclitaxel + Ganitumab | 18 | 4 | 0.875 (0.667-1.000) | 0.750 (0.000-1.000) | 0.786 (0.545-1.000) | exploratory_small_sample |
| treatment_arm | Paclitaxel + MK-2206 | 15 | 4 | 0.773 (0.429-1.000) | 0.500 (0.000-1.000) | 0.909 (0.700-1.000) | exploratory_small_sample |
| treatment_arm | Paclitaxel + Neratinib | 31 | 12 | 0.693 (0.504-0.863) | 0.667 (0.385-0.917) | 0.526 (0.300-0.750) | reported |
| treatment_arm | Paclitaxel + Pembrolizumab | 15 | 6 | 0.907 (0.700-1.000) | 0.667 (0.250-1.000) | 0.889 (0.625-1.000) | exploratory_small_sample |
| treatment_arm | T-DM1 + Pertuzumab | 12 | 7 | 1.000 (1.000-1.000) | 1.000 (1.000-1.000) | 1.000 (1.000-1.000) | exploratory_small_sample |

## Treatment arms not estimated

- Paclitaxel + AMG 386 + Trastuzumab: n=5, pCR=1; insufficient under the prespecified reporting rule.
- Paclitaxel + MK-2206 + Trastuzumab: n=5, pCR=1; insufficient under the prespecified reporting rule.
- Paclitaxel + Pertuzumab + Trastuzumab: n=9, pCR=4; insufficient under the prespecified reporting rule.
- Paclitaxel + Trastuzumab: n=7, pCR=3; insufficient under the prespecified reporting rule.

The subgroup analysis is descriptive and underpowered for interaction or treatment-effect inference. It must not be interpreted as evidence that treatment performance differs between arms or biomarker groups.
