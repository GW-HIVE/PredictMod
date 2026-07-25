# GSE194040 preprocessing summary

Run timestamp: 2026-07-19T15:11:24

## Environment provenance
- This existing processed dataset was produced in the environment recorded by `logs/gse194040_session_info.json`: CPython 3.12.13 on 64-bit Windows, pandas 3.0.1, and NumPy 2.3.5.
- It has not been regenerated under the current prediction/testing lock, which specifies pandas 2.2.2 and NumPy 2.5.1.

## Input files
- Expression: `GSE194040_ISPY2ResID_AgilentGeneExp_990_FrshFrzn_meanCol_geneLevel_n988.txt.gz`; SHA-1 `f84873f85a5ba8ca4a357a414e0b847532ed74d6`
- Series matrix: `GSE194040-GPL20078_series_matrix.txt.gz`; SHA-1 `6fdf48178aeb1a1394ae5718b1e13d026987ed86`
- Series matrix: `GSE194040-GPL30493_series_matrix.txt.gz`; SHA-1 `27a7ad81e2e7ffa42b9f9382928f43ff39312069`
- Source accession: `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE194040`

The downloaded archives are intentionally excluded from the submission and are
recreated by `scripts/preprocess_gse194040.py`.

## Structure confirmed
- The expression file has genes as rows and ISPY2 numeric sample/patient IDs as columns.
- The matrix was transposed and duplicate patient/sample IDs were aggregated by the mean expression value to enforce one row per patient.
- Clinical labels were parsed from GEO `Sample_characteristics_ch1` fields and merged by numeric ISPY2 patient ID.

## Final dataset
- Rows/patients: 987
- Columns: 19143
- Gene-expression features retained: 19134 of 19134
- Genes removed for missingness > 20.00%: 0
- Genes removed for near-zero variance <= 1e-08: 0
- Remaining missing expression values: 2831

## Leakage note
- Filtering here is outcome-independent QC only: missingness and near-zero variance do not use pCR labels.
- Scaling, imputation, model-based feature selection, hyperparameter tuning, and train/test splits should be fit inside each training fold only.

## Main outputs
- `data_processed/gse194040_ml_ready_pcr_expression.csv` (intentionally excluded;
  SHA-1 `714aacadbdbfecbc882662ad36f578afc398201c`; SHA-256
  `4f00b3fdf4006129ed31835763dfc906245da1c6d383546a7fe354d5069de78a`)
- `data_processed/gse194040_data_dictionary.csv`
- `data_processed/gse194040_gene_feature_manifest.csv`
- `results/tables/gse194040_qc_summary.csv`
- `results/tables/gse194040_gene_feature_qc.csv`
