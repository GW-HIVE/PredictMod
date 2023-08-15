# %%
import pandas as pd
import numpy as np

accessions = pd.read_csv(
    "/Users/urnishabhuiyan/Desktop/b4referencefilter.csv"
)  # enter file path
accessions.head()
# %%
uaccessions = accessions[
    "Accession"
].drop_duplicates()  # drops duplicated accessions in column
# uaccessions.count()

with open(
    "unique_accessions.txt", "w"
) as output:  # generates a txt list of unique accessions
    for row in uaccessions:
        output.write(str(row) + "\n")
