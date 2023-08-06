"""
The :mod:`codeless.impute.num` module includes methods to
handle numerical NaN values.
"""

import numpy as _np


def GetFeatures(df):
    '''
    This method returns name of all the numerical features.
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
        
    Returns
    -------------------
    features: returns a list of all the numerical features.
    '''
    
    features = df.select_dtypes(exclude=['object']).columns
    return features


def ImputeMmm(df, columns, strategy='Median'):
    '''
    MEAN/MEDIAN/MODE IMPUTATION
    This method imputes Mean, Median or Mode value for all Numerical
    columns provided.
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/Series
        List of all the column on which log transformation is to apply
    strategy: String, optional
        only three values are accepted ie. Median, Mean, Mode
        if Median then replace NaN values with median.
        if Mode then replace NaN values with mode.
        if Mean then replace NaN values with mean.
        
    Returns
    -------------------
    df: imputed dataset
    '''
    for col in columns:
        if strategy == 'Median':
            val = df[col].median()
        elif strategy == 'Mean':
            val = df[col].mean()
        elif strategy == 'Mode':
            val = df[col].mode()[0]
        df[col] = df[col].fillna(val)
    return df


def ImputeSample(df, columns):
    '''
    RANDOM SAMPLE IMPUTATION
    This method selects Random Sample of data equal to number of rows with
    missing values & imputes these sample data into all the NaN values.
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/Series
        List of all the column on which log transformation is to apply.
        
    Returns
    -------------------
    df: imputed dataset
    '''
    
    for col in columns:
        # pick that many random samples as many NaN values are present in the column
        random_sample = df[col].dropna().sample(df[col].isnull().sum(), random_state=0)

        # pandas need to have same index in order to merge the dataset
        random_sample.index= df[df[col].isnull()].index

        # using loc we are replacing with random sample whenever it finds null
        df.loc[df[col].isnull(), col] = random_sample
    return df


def ImputeColumn(df, columns, strategy='Median'):
    '''
    CAPTURING NAN VALUES WITH A NEW FEATURE
    This method creates a new column with 1 in all those rows containing 
    null values and 0 in rows with non-null values. In this way importance
    of null rows are taken into consideration. Also imputes Mean/ 
    Median/Mode value in the original column.
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/Series
        List of all the column on which log transformation is to apply
    strategy: String, optional
        only three values are accepted ie. Median, Mean, Mode
        if Median then replace NaN values with median in original column.
        if Mode then replace NaN values with mode in original column.
        if Mean then replace NaN values with mean in original column.
        
    Returns
    -------------------
    df: imputed dataset
    '''
    for col in columns:
        if strategy == 'Median':
            val = df[col].median()
        elif strategy == 'Mean':
            val = df[col].mean()
        elif strategy == 'Mode':
            val = df[col].mode()[0]
        df[col+'_Nan'] = _np.where(df[col].isnull(), 1, 0)
        df[col] = df[col].fillna(val)
    return df


def ImputeEod(df, columns):
    '''
    END OF DISTRIBUTION IMPUTATION for NUMERIC
    This method imputes a large value [ie. (mean() + 3*std())] inplace of 
    all NaN values.
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/Series
        List of all the column on which log transformation is to apply.
        
    Returns
    -------------------
    df: imputed dataset
    '''
    
    for col in columns:
        extreme = df[col].mean() + 3*df[col].std()
        df[col] = df[col].fillna(extreme)
    return df



__all__ = [
        'GetFeatures',
        'ImputeMmm',
        'ImputeSample',
        'ImputeColumn',
        'ImputeEod'
        ]