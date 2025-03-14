import joblib
import numpy as np
import pandas as pd


class OCMethylationPredictor:
    def __init__(self):
        bundled_info = joblib.load(
            "./models/ovarian_cancer_methylation/methylation_model.pkl"
        )
        self.classifier = bundled_info["model"]
        self.bundled_info = bundled_info

    def make_prediction(self, df):

        # headers, data = raw_data[0], np.array([raw_data[1]])
        # df = pd.DataFrame(data, columns=headers)

        # print(f"---> Received length: {df['Value'].__len__()}")

        data = np.array(df["Value"].values.tolist())
        data = np.reshape(data, (1, -1))
        # data = np.reshape(data, (-1, 2))
        # print(f"{data}")

        prediction = self.classifier.predict(data)
        return {
            "result": "This patient {} expected to respond to the intervention ".format(
                "is" if prediction == "R" else "is not"
            ) + "based on methylation input"
        }
