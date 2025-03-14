import joblib
import numpy as np
import pandas as pd


class OCRNASeqPredictor:
    def __init__(self):
        bundled_info = joblib.load(
            "./models/ovarian_rnaseq/ovarian_rnaseq_model.pkl"
        )
        self.classifier = bundled_info["model"]
        self.normalizer = bundled_info["normalizer"]
        self.bundled_info = bundled_info

    def make_prediction(self, df):

        # headers, data = raw_data[0], np.array([raw_data[1]])
        # df = pd.DataFrame(data, columns=headers)
        
        data = np.array(df["1"].values.tolist())
        data = np.reshape(data, (1, -1))

        normalized_data = self.normalizer.transform(data)
        prediction = self.classifier.predict(normalized_data)

        return {
            "result": "This patient {} expected to respond to the ".format(
                "is" if prediction == "1" else "is not"
            ) + "intervention based on RNAseq input"
        }
