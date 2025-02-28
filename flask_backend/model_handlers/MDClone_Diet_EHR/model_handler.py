import pickle
import io

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import shap

from base64 import b64encode


class MDClone_EHRTreeHandler:
    def __init__(self):
        with open(
            "./models/MDClone_Diet_Counseling_v1.1/old/MDClone_DTCv1.2.pickle", "rb"
        ) as fp:
            pickled_tree = pickle.load(fp)
        fp.close()
        self.pickled_tree = pickled_tree
        self.explainer = shap.Explainer(pickled_tree)
        # For shipping images

    def make_prediction(self, df):

        # headers, data = raw_data[0], np.array([raw_data[1]])
        # df = pd.DataFrame(data, columns=headers)

        prediction = self.pickled_tree.predict(df)[0]
        shap_values = self.explainer.shap_values(df)
        result = "expected" if prediction == "R" else "not expected"
        # To return an image
        shap.force_plot(
            self.explainer.expected_value[0],
            shap_values[0],
            df.iloc[0],
            matplotlib=True,
            show=False,
        )
        buf = io.BytesIO()
        # XXX?
        # width, height = plt.gcf().get_size_inches()
        # app.logger.debug(f"Image dimensions are {height} x {width}")
        # plt.gcf().set_size_inches(height * 2, width * 2)
        # app.logger.debug(
        #     "Image dimensions are NOW {0} x {1}".format(*(plt.gcf().get_size_inches()))
        # )
        plt.savefig(buf, format="png", bbox_inches="tight")
        b64_image = b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")
        return {
            "result": f"This patient is {result} to respond to the intervention based on EHR input",
            "image": b64_image,
        }
        # To return JSONified information
        # fp = shap.force_plot(
        #     self.explainer.expected_value[0], shap_values[0], data.iloc[0]
        # )
        # return {
        #     "result": f"This patient is {result} to respond to the intervention based on EHR input",
        #     "plot": json.dumps(fp.data),
        # }
