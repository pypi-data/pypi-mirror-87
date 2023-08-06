"""
The :mod:`codeless.encode.nominal` module includes methods to
perform encoding for nominal category features.
"""


import numpy as _np
import pandas as _pd



def EncodOnehot(df, columns, drop_original=False):
    '''
    ONE HOT ENCODING
    If the column contails less number of category features then OneHotEncoding
    is performed using pandas inbuilt get_dummies function.
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/Series
        List of all the column on which log transformation is to apply
    drop_original: boolean, optional
        if 'True' then original column is droped from the dataset else
        it is not droped.
    
    Returns
    -------------------
    df: encoded dataset
    '''
    
    for col in columns:
        dummy = _pd.get_dummies(df[col], drop_first=True)
        df = _pd.concat([df, dummy], axis=1)
    if drop_original == True:
        df = df.drop(columns, axis=1)
    return df



def EncodOnehotTopN(df, columns, n_feature=10, drop_original=False):
    '''
    ONE HOT ENCODING- VARIABLES WITH MANY CATEGORIES
    In the winning solution of the KDD 2009 cup: 'Winning the KDD Cup Orang
    Callenge with Ensemble Selection the author limit one hot encoding to
    the 10 most frequent labels of the variable. This means that they would
    make one binary variable for each of the 10 most frequent labels only.
    This is equivalent to grouping all the other labels under a new category,
    that in this case will be dropped. Thus the 10 new dummy variables indicate 
    if one of the 10 most frequent labels is present (1) or not(0) for a
    particular observation'
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/Series
        List of all the column on which log transformation is to apply
    n_feature: Int, optional
        number of top n features to consider for encoding. By default it
        is 10 => top 10 most frequent category feature will be encoded
        & others will be ignored.
    drop_original: boolean, optional
        if 'True' then original column is droped from the dataset else
        it is not droped.
        
    Returns
    -------------------
    df: encoded dataset
    '''
    
    for col in columns:
        # This will return top n feature name without count value
        lst_n = list(df[col].value_counts().sort_values(ascending=False).head(n_feature).index)
        for categories in lst_n:
            # for each feature from lst_n create a new column 
            df[col+'_'+categories] = _np.where(df[col]==categories, 1, 0)
    if drop_original == True:
        df = df.drop(columns, axis=1)
    return df




__all__ = [
        'EncodOnehot',
        'EncodOnehotTopN'
        ]