"""
File:           ccrcc_preprocessing.py
Author:         Karina Martinez
Version:        1.0
Description:    Utility function for combining glycopeptide abundances, biospecimen, clinical, clinical exposure 
                and follow up data into one dataframe. The data is mapped based on 'aliquot submitter id' and
                'case id.' Duplicate columns are dropped if all rows are identical, or renamed if data does 
                not match.
"""

import pandas as pd
import numpy as np


def drop_dup_columns(df_name):
    # After merging files, drop duplicate columns with identical values
    dup_cols = [x for x in df_name.columns if "_y" in x]
    num_dropped = 0
    cols_dropped = []
    for col in dup_cols:
        left_col = col.split("_")[0]
        right_col = col
        # Check if columns contains all the same values
        if len(df_name[[left_col,right_col]][df_name[left_col] != df_name[right_col]].dropna(how="all")) == 0:
            df_name.drop(right_col, axis=1, inplace=True)
            num_dropped += 1
            cols_dropped.append(right_col)
        # Check if columns can be merged without changing any values other than NaN
        elif len(df_name[df_name[left_col].fillna(df_name[right_col]) != df_name[right_col].fillna(df_name[left_col])]) == 0:
            df_name[left_col] = df_name[left_col].fillna(df_name[right_col])
            df_name.drop(right_col, axis=1, inplace=True)
            num_dropped += 1
            cols_dropped.append(right_col)

    return df_name

def preprocessed_data():

    # Import the file as dataframe
    df = pd.read_csv("ccRCC_TMT_intact glycopeptide_abundance_MD-MAD_50percentQuant_imputed.tsv", sep="\t")

    # Transpose the dataframe, reset headers and index
    df_T = df.T
    df_T.columns = df_T.iloc[0]
    df_T = df_T[1:].reset_index()

    # Import biospecimen data, replace blankspace values with NaN, set headers to lowercase
    biospecimen = pd.read_csv("PDC_study_biospecimen_09182023_104440.tsv", sep="\t")
    biospecimen.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    biospecimen.columns = [col.lower() for col in list(biospecimen.columns)]

    # Import clinical data, replace blankspace values with NaN, set headers to lowercase
    clinical = pd.read_csv("PDC_study_clinical_09182023_105327.tsv", sep="\t")
    clinical.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    clinical.columns = [col.lower() for col in list(clinical.columns)]

    # Import clinical exposure data, replace blankspace values with NaN, set headers to lowercase
    clinical_exposure = pd.read_csv("PDC_study_clinical_exposure_09182023_105327.tsv", sep="\t")
    clinical_exposure.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    clinical_exposure.columns = [col.lower() for col in list(clinical_exposure.columns)]

    # Import clinical follow up data, replace blankspace values with NaN, set headers to lowercase
    clinical_followup = pd.read_csv("PDC_study_clinical_followup_09182023_105327.tsv", sep="\t")
    clinical_followup.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    clinical_followup.columns = [col.lower() for col in list(clinical_followup.columns)]
 
    # Merge abundance and biospecimen dataframes
    abundance_biospecimen = pd.merge(df_T,biospecimen, left_on="index", right_on="aliquot submitter id", validate="one_to_one", suffixes=(None, "_y"))
    abundance_biospecimen.drop("index", axis=1, inplace=True)
    abundance_biospecimen = drop_dup_columns(abundance_biospecimen)

    # Merge dataframe from previous step with clinical dataframe
    abundance_biospecimen_clinical = abundance_biospecimen.merge(clinical, on="case id", validate="many_to_one", suffixes=(None, "_y"))
    abundance_biospecimen_clinical = drop_dup_columns(abundance_biospecimen_clinical)

    # Merge dataframe from previous step with clinical exposure dataframe
    abundance_biospecimen_clinical_exposure = abundance_biospecimen_clinical.merge(clinical_exposure, on="case id", validate= "many_to_one", suffixes=(None, "_y"))
    abundance_biospecimen_clinical_exposure = drop_dup_columns(abundance_biospecimen_clinical_exposure)

    # Merge dataframe from previous step with clinical follow up dataframe
    abundance_biospecimen_clinical_exposure_fu = abundance_biospecimen_clinical_exposure.merge(clinical_followup, on="case id", how="left", validate= "many_to_one", suffixes=(None, "_y"))
    abundance_biospecimen_clinical_exposure_fu = drop_dup_columns(abundance_biospecimen_clinical_exposure_fu)

    # Review duplicate columns that could not be dropped or merged
    final_df = abundance_biospecimen_clinical_exposure_fu.copy(deep=True)
    final_df[final_df["days to recurrence"] != final_df["days to recurrence_y"]][["days to recurrence","days to recurrence_y"]].dropna(how="all")

    # Drop "days to recurrence" as the only different rows are NaN
    final_df.drop("days to recurrence", axis=1, inplace=True)
    final_df.rename(columns={"days to recurrence_y": "days to recurrence"}, inplace=True)

    # Rename "progression or recurrence_fu" as follow up resulted in a different value
    final_df.rename(columns={"progression or recurrence_y": "progression or recurrence_fu"}, inplace=True)

    return final_df