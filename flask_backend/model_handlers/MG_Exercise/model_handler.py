import pickle
import numpy as np
import pandas as pd


class MGTreeHandler:
    def __init__(self):
        with open("./models/MG_Exercise_v1.1/pickled_mg_tree.pickle", "rb") as fp:
            self.pickled_tree = pickle.load(fp)
        fp.close()

    def make_prediction(self, df):

        # headers, data = raw_data[0], np.array([raw_data[1]])
        # df = pd.DataFrame(data, columns=headers)
        try:
            df = df.drop(["Status"], axis=1)
        except:
            pass

        prediction = self.pickled_tree.predict(df)[0]
        return {
            "result": "This patient {} expected to respond to the intervention based on Metagenomic input".format(
                "is" if prediction == "R" else "is not"
            )
        }
