# prediabetes_proteomics_model
The following information provided in this document details our process for data preprocessing, algorithm selection, hyperparameters, model evaluation, and quality control. Additionally, the goal of this document is to highlight source code associated with each iteration of the proteomics model.

## Data Source 
This dataset was retrieved from a publication interested in identifying the protein-related predictors for exercise. 
The training dataset included 48 patients and 688 variables.
PMID: 36787735

## Intervention & Outcomes 
The intervention consisted of a 12-week high-intensity interval exercise training program for medication-naïve overweight or obese men with prediabetes.

## Algorithm & Model Performance 
A Logistic Regression was employed, with data preprocessing incorporating augmented noise for synthetic resampling of both classes. This improved the LR performance and mitigated overfitting that was previously an issue with this model. 

## Algorithm Stats
**Overall Accuracy:** 0.9

**Overall F1 Score:** 0.92

**Overall AUC:** 0.93


