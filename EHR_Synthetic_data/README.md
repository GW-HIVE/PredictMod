# This is heading

Synthetic Electronic Health Record (EHR) generation utilizing Generative Adversial Network (GAN)

# Usage
- Item 1: Load_and_format.py:
    Responsible for taking input patient data and diagnosis and format into an mxn matrix where each row is a unique patient and each column is a measurable biomarker
- Item 2: Synthetic_EHR_data_diabetes.py:
    Takes formatted data produced from Load_and_format.py and trains a generator and discriminator to upscale original diabetic data using a Generative Adversial Network (GAN)
To generate synthetic data, first run Load_and_format.py, then Synthetic_EHR_data_diabetes.py

# Notes
Load_and_format.py and Synthetic_EHR_data_diabetes currently are hard coded for take only Diastolic Blood Pressure, Systolic Blood Pressure, Urea, Nitrogen, Creatinine, Calcium, Sodium. Future progress on this will include a dynamic approach to pre-select variables for training the GAN