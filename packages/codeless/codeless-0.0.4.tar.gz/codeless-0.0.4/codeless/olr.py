"""
The :mod:`codeless.olr` module includes methods 
to handle outliers.
"""


import numpy as _np


def StdOutlier(df, columns, strategy='replace'):
    '''
    This method removes all outliers and replace it with 3rd standard 
    deviation value.
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/Series
        List of all the column on which log transformation is to apply
    strategy: replace/remove, optional
        if "replace" then replace the outliers will be replaced with 3rd standard 
        deviation value
        if "remove" then remove all the rows having outliers
        
    Returns
    -------------------
    df: dataset after acting on the outliers
    '''
    for col in columns:
        # find the upper limit
        upper = df[col].mean() + 3* df[col].std()
        # find the lower limit
        lower = df[col].mean() - 3* df[col].std()
        
        if strategy == 'replace':
            df[col] = _np.where(df[col]>upper, upper, df[col])
            df[col] = _np.where(df[col]<lower, lower, df[col])
        elif strategy == 'remove':
            df.drop(df[df[col] > upper].index, axis=0, inplace=True)
            df.drop(df[df[col] < lower].index, axis=0, inplace=True)
    return df



def IqrOutlier(df, columns, strategy='replace', extreme=False):
    '''
    This method removes all outliers and replace it with a maximum value 
    ie. maximum inter_quantile value calculated.
    
    Parameters
    --------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/Series
        List of all the column on which log transformation is to apply
    strategy: replace/remove, optional
        if "replace" then replace the outliers will be replaced with 3rd standard 
        deviation value
        if "remove" then remove all the rows having outliers
    extreme: boolean, optional
        whether the inter_quantile range to find is extreme or not. 
        if extreme then IQR(Inter Qunatile Range) is multiplied
        with 3 else IQR is multiplied with 1.5
        
        Note:generally for skew distribution, extreme iqr is calculated, 
        and for gaussian simple inter_quantile range is calculated.
        
    Returns
    -------------------
    df: dataset after acting on the outliers
    '''
    

    mul = 1.5 if extreme==False else 3
    
    for col in columns:
        IQR = df[col].quantile(0.75)-df[col].quantile(0.25)
        upper_bridge = df[col].quantile(0.75) + (mul * IQR)
        lower_bridge = df[col].quantile(0.25) - (mul * IQR)
        
        if strategy == 'replace':
            df[col] = _np.where(df[col]>upper_bridge, upper_bridge, df[col])
            df[col] = _np.where(df[col]<lower_bridge, lower_bridge, df[col])
        elif strategy == 'remove':
            df.drop(df[df[col] > upper_bridge].index, axis=0, inplace=True)
            df.drop(df[df[col] < lower_bridge].index, axis=0, inplace=True)
    return df



__all__ = [
        'StdOutlier', 
        'IqrOutlier'
        ]

