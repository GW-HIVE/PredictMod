import pickle
import numpy as np
import pandas as pd


class PrediabetesProteomicsHandler:
    def __init__(self):
        with open("./models/prediabetes_proteomics/prediabetes_proteomics_model.pkl", "rb") as fp:
            model = pickle.load(fp)

        self.classifier = model

    def make_prediction(self, df):
        
        prediction = self.classifier.predict(df)[0]

        return {
            "result": "This patient {} expected to respond to the intervention based on Metagenomic input".format(
                "is" if prediction == 1 else "is not"
            )
        }
