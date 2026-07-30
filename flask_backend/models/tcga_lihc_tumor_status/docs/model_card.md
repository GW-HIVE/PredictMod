# Model Card: TCGA-LIHC Tumor Status Classifier

## Model purpose

Predict binary follow-up tumor status in TCGA-LIHC liver cancer patients: Tumor Free vs With Tumor.

## Intended use

Baseline PredictMod-style training package for educational/research workflow development. This model is not intended for clinical use.

## Data

- TCGA-LIHC clinical/follow-up metadata from GDC.
- TCGA-LIHC primary tumor RNA-seq expression data from UCSC Xena/GDC Hub.
- 352 matched primary tumor samples used after excluding missing/unknown tumor-status labels.

## Outcome

- Tumor Free = 0
- With Tumor = 1

## Features

Clinical variables and RNA-seq gene-expression values. Initial candidate gene features were filtered to the top 500 most variable genes, then Random Forest feature importance selected the top 15 final modeling features.

## Algorithms compared

- Logistic Regression
- Random Forest
- XGBoost
- Support Vector Machine
- Decision Tree

## Best model

Random Forest was selected as the current best model by AUROC.

## Performance

| Model | Accuracy | AUROC | F1 With Tumor |
|---|---:|---:|---:|
| Random Forest | 0.803 | 0.798 | 0.759 |

## Limitations

The tumor-status outcome comes from clinical follow-up records and is not a standardized controlled treatment-response label. This model should be described as a tumor-status/prognosis classifier, not a clean immunotherapy responder/non-responder model.

## Ethical/clinical note

This package is for research and training only. It should not be used to make clinical decisions.
