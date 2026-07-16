"""
Utility Functions for Breast Cancer Model Training
"""

import pandas as pd
import numpy as np


def remove_iqr_outliers(df, feature_cols, multiplier=1.5):
    """
    Remove outliers using IQR method and return bounds.

    Args:
        df: DataFrame containing the data
        feature_cols: List of feature column names to check for outliers
        multiplier: IQR multiplier for outlier detection (default: 1.5)
    
    Returns:
        clean_df: DataFrame with outliers removed
        iqr_bounds: Dictionary of {column: (lower_bound, upper_bound)}
    """
    iqr_bounds = {}
    mask = pd.Series(True, index=df.index)
    
    for col in feature_cols:
        # Skip if column doesn't exist or is not numeric
        if col not in df.columns:
            continue
        
        if df[col].dtype == 'object':
            continue
        
        # Calculate IQR
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        # Calculate bounds
        lower = Q1 - multiplier * IQR
        upper = Q3 + multiplier * IQR
        
        # Store bounds for later use on test set
        iqr_bounds[col] = (lower, upper)
        
        # Create mask for this column
        col_mask = (df[col] >= lower) & (df[col] <= upper)
        mask = mask & col_mask
    
    # Apply mask
    clean_df = df[mask].copy()
    
    print(f"  IQR outlier removal: {len(df)} -> {len(clean_df)} rows ({len(df)-len(clean_df)} outliers removed)")
    
    return clean_df, iqr_bounds


def apply_iqr_bounds(df, iqr_bounds):
    """
    Apply pre-computed IQR bounds to filter a dataset.
    
    This function is used to apply training-set outlier bounds to test data,
    ensuring no test data statistics leak into preprocessing.
    
    Args:
        df: DataFrame to filter
        iqr_bounds: Dictionary of {column: (lower_bound, upper_bound)} from training set
    
    Returns:
        filtered_df: DataFrame with outliers removed based on training bounds
    """
    mask = pd.Series(True, index=df.index)
    
    for col, (lower, upper) in iqr_bounds.items():
        if col in df.columns:
            col_mask = (df[col] >= lower) & (df[col] <= upper)
            mask = mask & col_mask
    
    filtered_df = df[mask].copy()
    
    print(f"  Applied IQR bounds: {len(df)} -> {len(filtered_df)} rows ({len(df)-len(filtered_df)} outliers removed)")
    
    return filtered_df


def validate_preprocessing_pipeline(train_df, test_df, feature_cols):
    """
    Validate that preprocessing was done correctly (no data leakage).
    
    Args:
        train_df: Training dataframe
        test_df: Test dataframe
        feature_cols: List of feature columns
    
    Returns:
        dict: Validation results
    """
    validation = {
        'train_test_overlap': False,
        'feature_columns_match': False,
        'no_nulls_train': False,
        'no_nulls_test': False
    }
    
    # Check for patient overlap
    train_patients = set(train_df['Patient_code'].unique())
    test_patients = set(test_df['Patient_code'].unique())
    overlap = train_patients & test_patients
    
    if len(overlap) == 0:
        validation['train_test_overlap'] = True
        print("✅ No patient overlap between train and test")
    else:
        print(f" Patient overlap detected: {overlap}")
    
    # Check feature columns
    train_features = set(train_df.columns) & set(feature_cols)
    test_features = set(test_df.columns) & set(feature_cols)
    
    if train_features == test_features:
        validation['feature_columns_match'] = True
        print("✅ Feature columns match between train and test")
    else:
        missing_in_test = train_features - test_features
        missing_in_train = test_features - train_features
        if missing_in_test:
            print(f" Features missing in test: {missing_in_test}")
        if missing_in_train:
            print(f" Features missing in train: {missing_in_train}")
    
    # Check for nulls
    if not train_df[feature_cols].isnull().any().any():
        validation['no_nulls_train'] = True
        print("✅ No nulls in training features")
    else:
        null_cols = train_df[feature_cols].columns[train_df[feature_cols].isnull().any()].tolist()
        print(f" Nulls found in training features: {null_cols}")
    
    if not test_df[feature_cols].isnull().any().any():
        validation['no_nulls_test'] = True
        print("✅ No nulls in test features")
    else:
        null_cols = test_df[feature_cols].columns[test_df[feature_cols].isnull().any()].tolist()
        print(f" Nulls found in test features: {null_cols}")
    
    return validation