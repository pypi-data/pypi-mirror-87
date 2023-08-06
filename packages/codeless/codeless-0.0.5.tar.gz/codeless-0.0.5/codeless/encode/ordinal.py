"""
The :mod:`codeless.encode.ordinal` module includes methods to
perform encoding for ordinal category features.
"""


import datetime as _datetime
import pandas as _pd


def EncodTime(df, columns, drop_original=False):
    '''
    ORDINAL NUMBER ENCODING
    This method encodes time series data. Here first the week day is
    calculated based on the data. Then the week day is encoded considering
    Monaday as 1, Tuesday as 2 etc. 
    
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
    
    dictionary = {'Monday':1, 'Tuesday':2, 'Wednesday':3, 'Thursday':4,
    'Friday':5, 'Saturday':6, 'Sunday':7 }
    
    for col in columns:
        # get all the day name from the timestamps in the dataframe
        df['weekday']=df[col].dt.day_name()
        # map our dictionary with the weekday
        df[col+'_TSEncoded']=df['weekday'].map(dictionary)
        # drop the weekday column as it is not necessary
        df = df.drop('weekday', axis=1)
    if drop_original == True:
        df = df.drop(columns, axis=1)
    return df


def EncodFrequency(df, columns, drop_original=False):
    '''
    COUNT OR FREQUENCY ENCODING
    This method encodes features based on the number of time each feature
    present in the column. eg in country column USA present 100 times, India 
    present 50 times. then USA will be encoded as 100 & India as 50.
    
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
        # First create a map of the column w.r.t the frequency of features.
        col_map = df[col].value_counts().to_dict()
        # map col_map to each feature in our dataframe.
        df[col+'_FEncoded'] = df[col].map(col_map)
    if drop_original == True:
        df = df.drop(columns, axis=1)
    return df


def EncodTarget(df, columns, target_feature, drop_original=False):
    '''
    TARGET GUIDED ORDINAL ENCODING
    Ordering the labels according to the target ie. probability of each 
    category is calculated based on the dependent features.. Then we 
    sort it and assign according to the sorted order. Assigned a target 
    number to each category. 
    Replace the labels by the joint probability of being 1 or 0.
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/Series
        List of all the column on which log transformation is to apply
    target_feature: String
        name of the target feature or dependent feature of the dataset.
    drop_original: boolean, optional
        if 'True' then original column is droped from the dataset else
        it is not droped.
        
    Returns
    -------------------
    df: encoded dataset
    '''
    
    for col in columns:
        ordinal_labels = df.groupby([col])[target_feature].mean().sort_values().index
        ordinal_labels2 = {k:i for i, k in enumerate(ordinal_labels, start=0)}
        df[col+'_TGEncoded'] = df[col].map(ordinal_labels2)
    if drop_original== True:
        df = df.drop(columns, axis=1)
    return df


def EncodMean(df, columns, target_feature, drop_original=False):
    '''
    MEAN ENCODING
    probability of each category is calculated based on the dependent features.
    Then assigned the mean to each category.
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/Series
        List of all the column on which log transformation is to apply
    target_feature: String
        name of the target feature or dependent feature of the dataset.
    drop_original: boolean, optional
        if 'True' then original column is droped from the dataset else
        it is not droped.
        
    Returns
    -------------------
    df: encoded dataset
    '''
    
    for col in columns:
        mean_ordinal = df.groupby([col])[target_feature].mean().to_dict()
        df[col+'_MEncoded'] = df[col].map(mean_ordinal)
    if drop_original== True:
        df = df.drop(columns, axis=1)
    return df


def EncodProbbility(df, columns, target_feature, drop_original=False):
    '''
    PROBABILITY RATION ENCODING
    probability ratio (probability of True/probability False) of each category
    is calculated based on the dependent features.
    Then assigned it to each category feature.
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/Series
        List of all the column on which log transformation is to apply
    target_feature: String
        name of the target feature or dependent feature of the dataset.
    drop_original: boolean, optional
        if 'True' then original column is droped from the dataset else
        it is not droped.
        
    Returns
    -------------------
    df: encoded dataset
    '''
    
    for col in columns:
        prob_df = _pd.DataFrame(df.groupby([col])[target_feature].mean())
        prob_df['Died'] = 1-prob_df[target_feature]
        prob_df['Probability_ratio']=prob_df[target_feature]/prob_df.Died
        probability_encoding = prob_df.Probability_ratio.to_dict()
        df[col+'_PREncoded'] = df[col].map(probability_encoding)
    
    if drop_original == True:
        df = df.drop(columns, axis=1)
    return df



__all__ = [
        'EncodTime',
        'EncodFrequency',
        'EncodTarget',
        'EncodMean',
        'EncodProbbility'
        ]