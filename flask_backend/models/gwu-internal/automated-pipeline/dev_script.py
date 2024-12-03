import pandas as pd

from pipeline import Pipeline

target_file = "../../MG_Exercise_v1.1/cleaned_literature_mg_v1.1.csv"


with open(target_file, "r") as fp:
    data = pd.read_csv(fp)

print(data)
