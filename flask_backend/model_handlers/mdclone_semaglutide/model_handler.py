import joblib
import numpy as np
import pandas as pd


class MDCloneSemaglutideHandler:
    def __init__(self):
        model_bundle = joblib.load("./models/mdclone_semaglutide/decision_tree_model_bundle.pkl")
        # Extract classifier, scaler, and feature names
        self.classifier = model_bundle['model']
        self.scaler = model_bundle['scaler']
        self.feature_names = model_bundle['columns']

    def make_prediction(self, df):
        
        prediction = self.classifier.predict(df)[0]

        return {
            "result": "This patient {} expected to respond to the intervention based on Metagenomic input".format(
                "is" if prediction == 1 else "is not"
            )
        }
