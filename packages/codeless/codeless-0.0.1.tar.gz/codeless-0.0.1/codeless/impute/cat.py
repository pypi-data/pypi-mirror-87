"""
The :mod:`codeless.impute.cat` module includes methods to
handle categorical NaN values.
"""


import numpy as _np


def GetFeatures(df):
    '''
    This method returns name of all the categorical features.
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
        
    Returns
    -------------------
    features: returns a list of all the categorical features.
    '''
    
    features = df.select_dtypes(include=['object']).columns
    return features


def ImputeMode(df, columns):
    '''
    FREQUENT CATEGORY IMPUTATION
    This method replaces all the NaN values with the highest occuring feature
    in the column or feature with highest frequency. This technique is mostly
    used if the missing data is less than 40%.
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/Series
        List of all the column on which log transformation is to apply
        
    Returns
    -------------------
    df: imputed dataset
    '''
    
    for col in columns:
        # find the most frequently occuring category in the varibale column
        most_frequent_category = df[col].value_counts().index[0]
        # below code can also be used to find highest occuring feature
        ### most_frequent_category = df[variable].mode()[0]
        # fill all the values with NaN using most frequently occuring category
        df[col].fillna(most_frequent_category, inplace=True)
    return df


def ImputeColumn(df, columns):
    '''
    CAPTURING NAN VALUES WITH A NEW COLUMN
    This method creates a new column with 1 in all those rows containing 
    NaN values and 0 in rows with not NaN values. Also imputes highest
    occuring feature of the column in the original column.
    For columns with more NaN value(above 40%) we can use this method. As 
    an extra column holds the importance of Nan value
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/Series
        List of all the column on which log transformation is to apply
        
    Returns
    -------------------
    df: imputed dataset
    '''
    for col in columns:
        df[col+'_Nan'] = _np.where(df[col].isnull(), 1, 0)
        most_frequent_category = df[col].value_counts().index[0]
        df[col].fillna(most_frequent_category, inplace=True)
    return df


def ImputeMissing(df, columns):
    '''
    REPLACE NAN WITH NEW CATEGORY
    This method imputes a new feature ie 'columnName_Missing' inplace of all 
    the NaN value.
    This is the most used technique nowadays.
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/Series
        List of all the column on which log transformation is to apply
        
    Returns
    -------------------
    df: imputed dataset
    '''
    
    
    for col in columns:
        df[col] = _np.where(df[col].isnull(), col+'_Missing', df[col])
    return df



__all__ = [
        'GetFeatures',
        'ImputeMode',
        'ImputeColumn',
        'ImputeColumn'
        ]