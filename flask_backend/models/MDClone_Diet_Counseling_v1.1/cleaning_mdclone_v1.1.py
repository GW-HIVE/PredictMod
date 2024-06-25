#%%
import pandas as pd
import numpy as np
#%%
df = pd.read_csv("raw_mdclone_v1.1.csv")
df.head()
#%%
#Drop rows that do not contain a value of 1 for bmi 30
df = df[df['bmi30'] == 1]
df["bmi30"].head()
#Drop rows that do not have a record for initial and final weight - this is required to determine response outcome
df = df[df['wt']> 0]
df = df[df['resulting_wt']> 0]
df['resulting_wt'].head()
# %%
#Create new column named "wt_red" that contains percent decrease in weight for each patient
df["wt_red"] = ((df['wt'] - df['resulting_wt'])/df['wt'])*100
df["wt_red"].head()
# %%
#Function that creates a new column that contains 1 for responders and 0 for non-responders 
def response_status (value): 
    if value >= 5:
        return 1
    else:
        return 0
df['response'] = df["wt_red"].apply(response_status)
# %%
#Drop the "resulting_wt" and "wt_red" columns - smoke was dropped due to inadequate data 
df = df.drop(["resulting_wt", "wt_red", "smoke"], axis=1)
#%%
#merge loinc and key features into a singular feature for each EHR variable. Then create new column that contains a value for that variable either from the loinc or key features.
import pandas as pd
import numpy as np

def handle_missing_values(key, loinc):
    if not pd.isnull(key):
        return key
    elif not pd.isnull(loinc):
        return loinc
    else:
        return np.nan

def merge_columns(df, key_col, loinc_col, output_col):
    df[output_col] = df.apply(lambda row: handle_missing_values(row[key_col], row[loinc_col]), axis=1)
    df = df.drop([loinc_col, key_col], axis=1)
    return df

# conduct the merges and create output column with just EHR variable name 
df = merge_columns(df, "protein_key", "protein_loinc", "protein")
df = merge_columns(df, "platelet_key", "platelet_loinc", "platelet")
df = merge_columns(df, "sodium_key", "sodium_loinc", "sodium")
df = merge_columns(df, "potassium_key", "potassium_loinc", "potassium")
df = merge_columns(df, "fast_glucose_key", "fast_glucose_loinc", "fast_glucose")
df = merge_columns(df, "ldl_key", "ldl_loinc", "ldl")
df = merge_columns(df, "hdl_key", "hdl_loinc", "hdl")
df = merge_columns(df, "triglycerides_key", "triglycerides_loinc", "triglycerides")
df = merge_columns(df, "hematocrit_key", "hematocrit_loinc", "hematocrit")
df = merge_columns(df, "bun_key", "bun_loinc", "bun")
df = merge_columns(df, "calcium_key", "calcium_loinc", "calcium")
df = merge_columns(df, "co2_key", "co2_loinc", "co2")
df = merge_columns(df, "chloride_key", "chloride_loinc", "chloride")
df = merge_columns(df, "creatinine_key", "creatinine_loinc", "creatinine")
df = merge_columns(df, "chol_total_key", "chol_total_loinc", "chol_total")
#%%
#Retreive dummy values for gender, race, and ethnicity 
df = pd.get_dummies(df, columns=['gender', 'race', 'ethnicity'])
#%%
filename= "clean_mdclone_v1.1.csv" #change version number when applicable 
df.to_csv(filename, index=False)
#%%