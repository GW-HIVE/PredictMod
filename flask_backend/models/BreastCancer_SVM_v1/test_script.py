import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import OneHotEncoder
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--input", type=str, required=True)
parser.add_argument("--model", type=str, required=True)
args = parser.parse_args()

FEATURE_COLS = [
    "Expression", "nGene", "percent_mito", "percent_hsp",
    "percent_ig", "percent_rp", "nUMI", "PDCD1"
]
CHEMO_FEATURE_COLS = ["Expression", "Origin_breast", "Origin_liver", "nGene",	"percent_mito",	"percent_hsp",	"percent_ig",	"percent_rp",	"nUMI",	"PDCD1"]
COMBO_FEATURE_COLS = ["Expression",	'Origin_chest_wall', 'Origin_liver','Origin_lymph_node', "nGene",	"percent_mito",	"percent_hsp",	"percent_ig",	"percent_rp",	"nUMI",	"PDCD1"]

model = joblib.load(args.model)

def run_prediction(df: pd.DataFrame) -> dict:

    # 1️⃣ Handle timeline safely
    if "Timeline" in df.columns:
        df = df[df["Timeline"] == "Pre_treatment"].copy()

    # 2️⃣ Keep required columns
    df = df[FEATURE_COLS + ["Origin"]].copy()

    # 3️⃣ One-hot encode Origin
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    origin_encoded = encoder.fit_transform(df[["Origin"]])
    origin_df = pd.DataFrame(
        origin_encoded,
        columns=encoder.get_feature_names_out(["Origin"])
    )

    df = pd.concat([df.drop(columns=["Origin"]).reset_index(drop=True),
                    origin_df.reset_index(drop=True)], axis=1)

    results = {}

    # ======================
    # MODEL SELECTION
    # ======================
    if args.model == "chemo_model.pkl":
        X = df.reindex(columns=CHEMO_FEATURE_COLS, fill_value=0)
    elif args.model == "combo_model.pkl":
        X = df.reindex(columns=COMBO_FEATURE_COLS, fill_value=0)

    preds = model.predict(X)
    rate = np.mean(preds) * 100

    return round(rate, 2)

if __name__ == "__main__":

    input_path = args.input
    df = pd.read_csv(input_path)
    percentage = run_prediction(df)
    print(f"Response Percentage: {percentage}")


    