import joblib
import numpy as np
import pandas as pd


class MDClone_Exercise_Classifier:
    def __init__(self, path="./models/mdclone_exercise/Diabetes_EHR_classifier_and_features.pickle"):
        model_data = joblib.load(path)
        self.classifier = model_data["classifier"]
        self.scaler = model_data["scaler"]
        self.feature_names = model_data["feature_names"]

    def make_prediction(self, df):
        # headers, data = raw_data[0], np.array([raw_data[1]])
        # df = pd.DataFrame(data, columns=headers)

        # Re-order columns ...?
        df = df[self.feature_names]

        # Scale features
        df = self.scaler.transform(df)

        prediction = self.classifier.predict(df)[0]
        return {
            "result": "This patient {} expected to respond to the intervention based on Metagenomic input".format(
                "is" if prediction == 1 else "is not"
            )
        }

if __name__ == "__main__":

    data = pd.read_csv("../../models/mdclone_exercise/single_patient_mdclone_exercise.csv")
    pickle_path = "../../models/mdclone_exercise/Diabetes_EHR_classifier_and_features.pickle"

    classifier = MDClone_Exercise_Classifier(path=pickle_path)
    print(f"==== {classifier.make_prediction(data)} ====")
    
