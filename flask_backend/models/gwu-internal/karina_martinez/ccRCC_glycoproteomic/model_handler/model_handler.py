import os
import joblib
import numpy as np
import pandas as pd
import time

CLASSIFIER_PICKLE = "./ccRCC_glycoproteomic/ccrcc_classifier_new.pkl"


def get_glycoforms(glycoform_df):
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

        glycosite = gene + "_" + str(glycosylation_site) + "_" + glycan

        if glycosite not in site_dict:
            site_dict[glycosite] = [i]

        else:
            site_dict[glycosite].append(i)

    df_dict = {}

    for key, value in site_dict.items():
        df_dict[key] = glycoform_df[value].sum(axis=1)

    return pd.DataFrame(df_dict)


class ccRCC_ClassifierHandler:
    def __init__(self):
        self.classifier = joblib.load(CLASSIFIER_PICKLE)

    def make_prediction(self, df):

        if self.classifier is None:
            return {
                "result": "Results are from this model are undergoing revision.\nCheck back soon!"
            }

        print(f"===> ccRCC Handler - Got a request! <===")

        # headers, data = raw_data[0], np.array([raw_data[1]])
        # df = pd.DataFrame(data, columns=headers)

        start = time.time()
        processed_df = get_glycoforms(df)
        # print(
        #     f"===> Preprocessing required {time.time() - start:.3f} seconds of compute..."
        # )

        start = time.time()
        pred = self.classifier.predict(processed_df)
        # print(
        #     f"===> Prediction required {time.time() - start:.3f} seconds of compute..."
        # )
        outcome = "Low risk" if pred == 1 else "High risk"

        # return {"error": "Please contact the Predictmod development team for updates."}

        return {
            "result": f"Prediction based on tumor N-glycoproteomic profile: {outcome}"
        }
        # if prediction == "R":
        #     return "This patient is expected to respond to the intervention based on Metagenomic input"
        # return "This patient is not expected to respond to the intervention based on Metagenomic input"
