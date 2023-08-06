"""
The :mod:`codeless.fs` module includes methods to
select best features/most relevant fetures.
"""


# For univariate Selection
from sklearn.feature_selection import SelectKBest as _skb# SelectKBest selects the k best features
from sklearn.feature_selection import chi2 as _chi#This is used for applying the statistical analysis eg.Hypothesis testing,
                                            # null hypothesis, alternate hypothesis etc.
# For Feature Importance
from sklearn.ensemble import ExtraTreesClassifier as _etc
# For Information Gain
from sklearn.feature_selection import mutual_info_classif as _mic

import pandas as _pd
import numpy as _np



def UVSelection(X, y, k=10):
    '''
    SELECT K-BEST
    Select features according to the k highest scores. Greater the Score
    more important the feature is.
    
    Parameters
    -------------
    X: Series/DataFrame
        Dataframe of all dependent feature.
    y: Series/DataFrame
        Independent Column
    k: Integer, optional
        based on Score, top k columns with highest Scores are selected.
        
    Returns
    ------------
    DataFrame: rectangular dataset
        a dataframe with two columns (ie. Feature, Score) is returned. 
        'Feature' containing names of all the column names & 'Score' 
        containing scores of each column arrange in deacreasing order 
        of score.
    '''
    
    # It'll take top k best feature
    ordered_rank_features = _skb(score_func=_chi,k=len(X.columns)) 
    ordered_feature=ordered_rank_features.fit(X,y)
    
    # feature_rank = pd.DataFrame(ordered_feature.scores_)
    feature_rank = _pd.DataFrame(ordered_feature.scores_, index=X.columns, columns=['Score'])
    return feature_rank.nlargest(k, 'Score')



def FeatureImportance(X, y):
    '''
    FEATURE IMPORTANCE
    This technique gives you a score for each feature of the data,
    the higher the score more relevant it is.
    
    Parameters
    -------------
    X: Series/DataFrame
        Dataframe of all dependent feature.
    y: Series/DataFrame
        Independent Column
        
    Returns
    ------------
    DataFrame: rectangular dataset
        a dataframe with a columns (ie. Score) is returned. 
        'Score' containing scores of each column arrange in deacreasing order 
        of score. Index column contains name of columns.
        
        To get top n features from the dataframe write
        list(ranked_features.nlargest(n, 'Score')['Feature'])
    '''
    
    model = _etc()
    model.fit(X, y)
    ranked_features = _pd.DataFrame(model.feature_importances_, index=X.columns, columns=['Score'])
    return ranked_features.nlargest(len(X.columns), 'Score')



def Corr(df, threshold=0.9, strategy=None):
    '''
    CORRELATION
    Find columns with correlation more then threshold. 
    
    Parameters
    -------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    threshold: float, optional
        All columns having more correlation value then threshold will be 
        taken into cosideration.
    strategy: string, optional
        Only two value is accepted ie. None & 'drop'
        If None then set of all the columns having correlation more then
        threshold will be returned.
        If 'drop' then all the columns having correlation more then 
        threshold will be droped from the dataset passed.
        
    Returns
    ------------
    df: rectangular dataset
        df is modified dataset after all the steps are done.
    col_corr: set
        set of all the columns with correlation more than threshold.
    '''
    col_corr = set() # Set of all the names of correlated columns
    corr_matrix = df.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j] > threshold): #we are interest in absolute coeff value
                colname = corr_matrix.columns[i] #getting the name of the column
                col_corr.add(colname)
                    
    if strategy=='drop':
        df = df.drop(col_corr, axis=1)
    return df, col_corr



def InfoGain(X, y):
    '''
    INFORMATION GAIN
    Estimate mutual information for a discrete target variable.

    Mutual information (MI) [1]_ between two random variables is a non-negative
    value, which measures the dependency between the variables. It is equal
    to zero if and only if two random variables are independent, and higher
    values mean higher dependency.

    The function relies on nonparametric methods based on entropy estimation
    from k-nearest neighbors distances as described in [2]_ and [3]_. Both
    methods are based on the idea originally proposed in [4]_.
    
    Parameters
    -------------
    X: Series/DataFrame
        Dataframe of all dependent feature.
    y: Series/DataFrame
        Independent Column
        
    Returns
    ------------
    DataFrame: rectangular dataset
        a dataframe with a columns (ie. Score) is returned. 
        'Score' containing scores of each column arrange in deacreasing order 
        of score. Index column contains name of columns.

        To get top n features from the dataframe write
        list(ranked_features.nlargest(n, 'Score')['Feature'])
    '''
    
    mutual_info = _mic(X, y)
    # mutual_info
    mutual_data = _pd.DataFrame(mutual_info, index=X.columns, columns=['Score'])
    return mutual_data.nlargest(len(X.columns), 'Score')




__all__ = [
        'UVSelection', 
        'FeatureImportance', 
        'Corr', 
        'InfoGain'
        ]