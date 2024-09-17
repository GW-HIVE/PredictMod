import joblib
import numpy as np
import pandas as pd


class Diabetes_Glycomic_Handler:
    def __init__(self):
        self.pickled_model = joblib.load("./Diabetes_glycomic/diabetes_classifier.pkl")

        # See ../../models/Diabetes_glycomic_v1/{files} for original source
        self.headers = pd.read_csv("./Diabetes_glycomic/gtc_headers.csv", sep=",")[
            "Header"
        ].to_list()

        self.glycan_dict = {
            "GP32-33_G67579EM": ["GP32_G67579EM", "GP33_G67579EM"],
            "GP38-39_G12638YK": ["GP38_G12638YK", "GP39_G12638YK"],
            "GP41-43_G16933RK": ["GP41_G16933RK", "GP42_G16933RK", "GP43_G16933RK"],
        }

    def preprocess_input(self, df):
        # See ../../models/Diabetes_glycomic_v1/{files} for original source

        df.columns = self.headers

        processed_df = pd.DataFrame()
        for key, value in self.glycan_dict.items():
            processed_df[key] = df[value].sum(axis=1)

        # Join combined features with original dataframe, drop individual peaks included in combined features
        df_out = df.join(processed_df)
        df_out = df_out.drop(
            columns=[
                "GP32_G67579EM",
                "GP33_G67579EM",
                "GP38_G12638YK",
                "GP39_G12638YK",
                "GP41_G16933RK",
                "GP42_G16933RK",
                "GP43_G16933RK",
            ]
        )

        return df_out

    def make_prediction(self, raw_data):

        headers, data = raw_data[0], np.array([raw_data[1]])
        df = pd.DataFrame(data, columns=headers)
        processed_df = self.preprocess_input(df)

        prediction = self.pickled_model.predict(processed_df)
        return {
            "result": "This patient {} expected to respond to the intervention based on Glycomic input".format(
                "is not" if prediction == 1 else "is"
            )
        }
        # if prediction == "R":
        #     return "This patient is expected to respond to the intervention based on Metagenomic input"
        # return "This patient is not expected to respond to the intervention based on Metagenomic input"
