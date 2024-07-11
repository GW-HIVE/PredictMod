import joblib
import numpy as np
import pandas as pd


class Epilepsy_Microbiome_Handler:
    def __init__(self):
        with open(
            "./models/Epilepsy_microbiome_v1/Epilepsy_keto_classifier_and_features.pickle",
            "rb",
        ) as fp:
            pickled_objects = joblib.load(fp)
            self.classifier = pickled_objects["classifier"]
            self.feature_names = pickled_objects["feature_names"]
            self.encoder = pickled_objects["encoder"]
        fp.close()

    def preprocess_data(self, patient_data):
        # See ../../models/Epilepsy_microbiome/{files} for implementation details

        # Check for missing columns in the new data
        missing_cols = set(self.feature_names) - set(patient_data.columns)
        for c in missing_cols:
            patient_data[c] = 0  # or some other value that makes sense in your context

        # Check for extra columns in the new data
        extra_cols = set(patient_data.columns) - set(self.feature_names)
        if extra_cols:
            print(
                f"Warning: Found extra columns in the new data that were not in the training data: {extra_cols}"
            )
            patient_data = patient_data.drop(columns=extra_cols)

        # Reorder the columns of the new data
        patient_data_sort = patient_data.reindex(columns=self.feature_names)
        if not patient_data.equals(patient_data_sort):
            print(
                f"Message: patient data features was sorted to match order of model features"
            )
        return patient_data_sort

    def make_prediction(self, raw_data):

        headers, data = raw_data[0], np.array([raw_data[1]])
        df = pd.DataFrame(data, columns=headers)

        # Make a prediction
        prediction = self.classifier.predict(df)
        # Decode the result
        decoded_result = self.encoder.inverse_transform(prediction)[0]
        return {
            "result": "This patient {} expected to respond to the intervention based on EHR input".format(
                "is" if prediction == "R" else "is not"
            )
        }
        # if prediction == "R":
        #     return "This patient is expected to respond to the intervention based on Metagenomic input"
        # return "This patient is not expected to respond to the intervention based on Metagenomic input"
