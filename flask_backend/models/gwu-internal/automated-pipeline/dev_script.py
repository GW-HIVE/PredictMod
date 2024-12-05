import pandas as pd

from pipeline import Pipeline

target_file = "../../MG_Exercise_v1.1/cleaned_literature_mg_v1.1.csv"


with open(target_file, "r") as fp:
    data = pd.read_csv(fp)

# print(data)

pl = Pipeline()

label_column = "Status"

response = pl.train_models(data, label_column, outcome_type="binary")

print(f"Got response:\n{response}")
