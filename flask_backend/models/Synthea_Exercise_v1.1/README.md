# Synthea_Exercise_v1.1 README

Synthetic Electronic Health Record (EHR) generation utilizing Generative Adversial Network (GAN)

# Usage
- Item 1: Load_and_format.py:
    Responsible for taking input patient data and diagnosis and format into an mxn matrix where each row is a unique patient and each column is a measurable biomarker
- Item 2: Synthetic_EHR_data_diabetes.py:
    Takes formatted data produced from Load_and_format.py and trains a generator and discriminator to upscale original diabetic data using a Generative Adversial Network (GAN)
To generate synthetic data, first run Load_and_format.py, then Synthetic_EHR_data_diabetes.py
- Item 3: sample_synthetic_EHR_data_1000patients.xlsx contains 1000 synthetic patients with measurments for Diastolic Blood Pressure, Systolic Blood Pressure, Urea, Nitrogen, Creatinine, Calcium, Sodium
- Item 4: Classifier Folder: Decision Tree Classifier to show how single patient EHR data (Patient from 1000 Synthetic EHR  xlsx file) will predict response or non-response to standard diabetes treatment. Requires console user input to determine which patient (1-1000) to predict treatment outcome

# Notes
Load_and_format.py and Synthetic_EHR_data_diabetes currently are hard coded for take only Diastolic Blood Pressure, Systolic Blood Pressure, Urea, Nitrogen, Creatinine, Calcium, Sodium. Future progress on this will include a dynamic approach to pre-select variables for training the GAN
