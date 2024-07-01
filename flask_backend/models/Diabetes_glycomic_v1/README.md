# Data Preprocessing, Algorithm Selection, and Model Evaluation for Diabetes Glycomic Classifier
## Data Source
The data is from Keser, Toma et al. “Increased plasma N-glycome complexity is associated with higher risk of type 2 diabetes.” Diabetologia vol. 60,12 (2017): 2352-2360. doi:10.1007/s00125-017-4426-9 and was provided by Dr. Olga Gornik, Faculty of Pharmacy and Biochemistry, University of Zagreb.

## Training Dataset
The dataset contains abundance information on the plasma N-glycome of individuals participating in the FinRisk study, a study designed to investigate risk factors in a population from Finland. Baseline samples were analyzed from 37 individuals who developed type 2 diabetes within 10 years and 37 sex and age matched individuals who remained normoglycaemic. HILIC-UPLC chromatograms were separated into 46 peaks, and were assigned to the most abundant glycan structures in each peak. The dataset consists of 74 patients and 68 columns (including metadata, glycan peaks and derived traits). Only abundances of 46 glycans from HILIC-UPLC chromatograms were used for training.

## Classifier and Predictor
### Classifier Code:
The classifier code takes patient data and labels, cleans the data, maps the peak numbers to GlyTouCan (https://glytoucan.org/) accessions, splits the data into training (80%) and testing (20%) sets, and trains an XGBoost Classifier on the training data. The trained classifier is then serialized and stored as a .pkl file for later use. The trained classifier predicts whether the patient will develop type 2 diabetes or remain normoglycaemic within 10 years. After training, the classifier is run on the test set and metrics are printed.

### Predictor Code:
The predictor code expects a single patient input file with abundances for glycans peaks GP1-46, and accepts a file name argument (diabetes_predict.py --file example_input.csv). It then loads the pre-trained XGBoost Classifier from the .pkl file, reads the input data, and reshapes the input data to match the classifier's requirements. The loaded classifier predicts whether the patient will develop type 2 diabetes or remain normoglycaemic within 10 years. The prediction result is printed to the console.

## Intervention & Outcomes
No intervention.

## Algorithm & Model Performance
Algorithm: XGBoost Classifier
F1 score: 0.732
Accuracy: 0.733
AUC: 0.804
