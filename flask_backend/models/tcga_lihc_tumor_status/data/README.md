# Data

## Main modeling dataset

`tcga_lihc_tumor_status_ml_ready_top500_genes.csv.gz`

Model-ready TCGA-LIHC dataset. Each row is a matched primary tumor RNA-seq sample with clinical variables, selected expression features, and a binary tumor-status outcome.

## Review dataset

`training_data_review_100_genes.csv`

Smaller review file with fewer gene columns for easier manual inspection.

## Example single-patient input

`example_single_patient_input.csv`

One-row example input for `scripts/single_patient_predict.py`.

## Outcome coding

- `0` = Tumor Free
- `1` = With Tumor

Missing or unknown tumor-status labels were excluded.
