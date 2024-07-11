# Data Preprocessing, Algorithm Selection, and Model Evaluation for Clear Cell Renal Cell Carcinoma Glycoproteomic Classifier
## Data Source
The data is from Lih, T Mamie et al. “Integrated glycoproteomic characterization of clear cell renal cell carcinoma.” Cell reports vol. 42,5 (2023): 112409. doi:10.1016/j.celrep.2023.112409 and was retrieved from the Proteomic Data Commons (PDC) and can be accessed at https://proteomic.datacommons.cancer.gov/pdc/study/PDC000471. 

## Training Dataset
The datasets contain intact glycopeptide abundances, biospecimen and clinical metadata from 183 resected clear cell renal cell carcinoma (ccRCC) tumor and normal adjacent tissues collected by the CPTAC program. Glycopeptide abundances with missing values imputed for intact glycopeptides quantified in >50% of the samples using DreamAI (https://github.com/WangLab-MSSM/DreamAI). Inclusion-exclusion criteria and risk assignment (High or Low) are based on the following metadata columns: "vital status","days to last known disease status","disease response","last known disease status","days to death","tissue type". Only glycopeptide abundances from tumor
samples were used for training.

## Classifier and Predictor
### Classifier Code:
The classifier code takes patient data, calls the preprocessing utility function, cleans the data, assigns target labels, splits the data into training (80%) and testing (20%) sets. It then runs a pipeline standardize the data, select the best features using LASSO, and train a Multilayer Perceptron Classifier on the training data. The trained classifier is then serialized and stored as a .pkl file for later use. The trained classifier predicts whether the patient is at high or low risk of death or disease progression within 5 years from tumor resection. After training, the classifier is run on the test set and metrics are printed.

### Predictor Code:
The predictor code expects a single patient input file with 10814 glycopeptide abundances, and accepts a file name argument (ccrcc_predict.py --file example_input.csv). It then loads the pre-trained Multilayer Perceptron Classifier from the .pkl file, reads the input data, and reshapes the input data to match the classifier's requirements. The loaded classifier predicts whether the patient is at high or low risk of death or disease progression within 5 years from tumor resection. The prediction result is printed to the console.

## Intervention & Outcomes
No intervention.

## Algorithm & Model Performance
Algorithm: Multilayer Perceptron Classifier
F1 score: 0.911
Accuracy: 0.917
AUC: 0.943
