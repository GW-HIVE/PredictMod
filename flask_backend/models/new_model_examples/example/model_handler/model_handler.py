import os
import joblib
import numpy as np
import pandas as pd
import time

CLASSIFIER_PICKLE = "./new_model_examples/example_1/pickled-and-stored-classifier.pkl"

class ExampleHandler:
    def __init__(self):
        self.classifier = joblib.load(CLASSIFIER_PICKLE)

    def make_prediction(self, df):

        if self.classifier is None:
            return {
                "result": "Results are from this model are undergoing revision.\nCheck back soon!"
            }

        # Handle any data preprocessing that the backends should manage here
        processed_df = df

        pred = self.classifier.predict(processed_df)

        outcome = "Outcome Label 1" if pred == 1 else "Outcome Label 2"

        return {
            "result": f"Example 1 Prediction: {outcome}"
        }
