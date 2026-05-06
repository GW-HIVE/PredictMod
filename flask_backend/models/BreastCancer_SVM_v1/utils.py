import os
import sys
import numpy as np
import pandas as pd
from typing import List

def int_conventor(df: pd.DataFrame, col_names: list [str]) -> pd.DataFrame:
    '''
    A function to convert the column names from another data type to integer
    :param df: data frame
    :param col_names: Column names to be converted in to integer
    :return: pd.dataFrame
    '''
    try:
        for col in col_names:
            df[col] = df[col].astype(int)
        return df

    except Exception as e:
        raise e

def float_conventor(df: pd.DataFrame, col_names: list[str]) -> pd.DataFrame:
    '''
    A function to convert the column names from another data type to integer
    :param df: data frame
    :param col_names: Column names to be converted in to integer
    :return: pd.dataFrame
    '''
    try:
        for col in col_names:
            df[col] = df[col].astype(float)
        return df

    except Exception as e:
        raise e

def remove_cols(df: pd.DataFrame, col_names: list[str]) -> pd.DataFrame:
    '''
    A function to remove columns from a data type
    :param df:
    :param col_names:
    :return: pd.DataFrame
    '''

    try:
        df = df.drop(col_names, axis=1, errors='ignore')
        return df
    except Exception as e:
        raise e


def remove_iqr_outliers(df, cols):
    """
    Removes outliers using IQR method for the given numeric columns.
    Keeps rows where each feature is within [Q1 - 1.5*IQR, Q3 + 1.5*IQR].
    """
    df_clean = df.copy()

    for col in cols:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]

    return df_clean
