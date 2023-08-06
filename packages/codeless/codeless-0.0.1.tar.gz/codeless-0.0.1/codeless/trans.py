"""
The :mod:`codeless.trans` module includes methods for
transforming data whose distribution are not Gaussian.
It also contains a method to check skewness of a distribution.
"""

from scipy.stats import boxcox as _boxcox
from scipy.stats import skew as _skew
import numpy as _np



def Skewness(df, threshold=0.75):
    '''
    This method finds skewness of the columns. More +ve the value is more right skewed the 
    distribution is. More -ve the value is more left skewed the distribution is.
    
    Parameters
    ------------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    threshold: float, optional
        minimum absolute skewness value. All columns having skewness value more than 
        threshold are considered.
        
    Returns
    ------------------
    skewness: pandas.core.series.Series
        returns list of all the columns having skewness more than threshold along with 
        skewness value.
    '''
    skewness = df.apply(lambda z: _skew(z.dropna()))
    skewness = skewness[abs(skewness) > threshold]
    return skewness


def TransLog(df, columns):
    '''
    LOG TRANSFORMATION
    This method applies log transformation to all the values of the column
    to convert skew distribution into Gaussian distribution.
    
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
    df: transformed dataset
    '''
    for col in columns:
        if (df[col] == 0).any():
            df[col] = _np.log1p(df[col])
        else:
            df[col] = _np.log(df[col])
    return df


def TransSqrt(df, columns):
    '''
    SQUARE ROOT TRANSFORMATION
    This method applies square root transformation to all the values of the column
    to convert skew distribution into Gaussian distribution.
    
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
    df: transformed dataset
    '''
    for col in columns:
        df[col] = df[col]**(0.5)
    return df


def TransRecip(df, columns):
    '''
    RECIPROCAL TRANSFORMATION
    This method applies reciprocal transformation to all the values of the column
    to convert skew distribution into Gaussian distribution.
    
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
    df: transformed dataset
    '''
    for col in columns:
        if (df[col] == 0).any():
            df[col] = 1/(df[col]+1)
        else:
            df[col] = 1/df[col]
    return df


def TransBoxcox(df, columns):
    '''
    BOXCOX TRANSFORMATION
    This method applies BoxCox transformation to all the values of the column
    to convert skew distribution into Gaussian distribution.
    
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
    df: transformed dataset
    '''
    for col in columns:
        df[col], lmbda = _boxcox(df[col], lmbda=None)




__all__ = ['Skewness', 
        'TransLog',
        'TransSqrt',
        'TransRecip',
        'TransBoxcox']


