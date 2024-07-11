import os
import pickle
import numpy as np
from scipy.stats import mannwhitneyu
import pandas as pd

CLASSIFIER_PICKLE = "./classifier.pkl"


class ccRCC_ClassifierHandler:
    def __init__(self):
        self.classifier = None
        # with open("./classifier.pkl", "rb") as fp:
        #     self.classifier = pickle.load(fp)
        # fp.close()
        ...

    def transform_mannwhitneyu(self, X, y):
        """
        Convert stats.mannwhitneyu() inputs from two independent samples to X and y for compatibility with Pipeline.
        """
        arg1, arg2 = X[y == 0], X[y == 1]
        f_statistic, p_values = mannwhitneyu(arg1, arg2)
        return f_statistic, p_values

    def get_glycoforms(self, glycoform_df):
        """
        Helper function to display gene, glycosylation site, sequence, and glycan composition in header.
        """
        site_dict = {}

        for i in glycoform_df.columns:
            row = i.split("_")
            gene, pep_start, sequence, gly_site, glycan = (
                row[0],
                int(row[1]),
                row[2],
                int(row[4]),
                row[5],
            )
            glycosylation_site = pep_start + gly_site - 1
            glycosite = (
                gene + "_" + str(glycosylation_site) + "_" + sequence + "_" + glycan
            )
            site_dict[i] = glycosite

        df_dict = {}

        for key, value in site_dict.items():
            df_dict[value] = glycoform_df[key]

        return pd.DataFrame(df_dict)

    def make_prediction(self, raw_data):

        if self.classifier is None:
            return {
                "result": "Results are from this model are undergoing revision.\nCheck back soon!"
            }

        headers, data = raw_data[0], np.array([raw_data[1]])
        df = pd.DataFrame(data, columns=headers)

        processed_df = self.get_glycoforms(df)

        pred = self.model.predict(processed_df)

        outcome = "Low risk" if pred == 1 else "High risk"

        # return {"error": "Please contact the Predictmod development team for updates."}

        return {
            "result": f"Prediction based on tumor N-glycoproteomic profile: {outcome}"
        }
        # if prediction == "R":
        #     return "This patient is expected to respond to the intervention based on Metagenomic input"
        # return "This patient is not expected to respond to the intervention based on Metagenomic input"
