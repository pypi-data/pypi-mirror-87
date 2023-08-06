"""
The :mod:`codeless.imb` module includes methods 
to handle imbalance dataset.
"""

from imblearn.under_sampling import NearMiss as _nm
from imblearn.over_sampling import RandomOverSampler as _ros
from imblearn.combine import SMOTETomek as _smt



def Undersampling(x, y, ratio=1):
    '''
    This method makes value_count of all values of y equal by removing 
    few number of rows using NearMiss library from imblearn.
    
    Parameters
    -------------------
    x: dataframe/Array
        independent features
    y: dataframe/Array
        dependent features
    ratio: float, optional
        ration in which both value of y to matched. eg if 1 then both value of 
        y will be present in equal proportion. It must be in the range of (0, 1].
        
    Returns
    -------------------
    x: independent feature
    y: dependent feature
    '''
    ns = _nm(ratio) 
    x, y = ns.fit_sample(x, y)
    return x, y


def Oversampling(x, y, ratio=1):
    '''
    This method makes value_count of all values of y equal by increasing 
    number of rows using RandomOverSampler from imblearn.
    
    Parameters
    -------------------
    x: dataframe/Array
        independent features
    y: dataframe/Array
        dependent features
    ratio: float, optional
        ration in which both value of y to matched. eg if 1 then both value of 
        y will be present in equal proportion. It must be in the range of (0, 1].
        
    Returns
    -------------------
    x: independent feature
    y: dependent feature
    '''
    os = _ros(ratio) 
    x, y = os.fit_sample(x, y)
    return x, y


def Smotetomek(x, y, ratio=1):
    '''
    This method makes value_count of all values of y equal by increasing 
    number of rows using SMOTETomek from imblearn.
    
    Parameters
    -------------------
    x: dataframe/Array
        independent features
    y: dataframe/Array
        dependent features
    ratio: float, optional
        ration in which both value of y to matched. eg if 1 then both value of 
        y will be present in equal proportion. It must be in the range of (0, 1].
        
    Returns
    -------------------
    x: independent feature
    y: dependent feature
    '''
    os = _smt(ratio) 
    x, y = os.fit_sample(x, y)
    return x, y



__all__ = [
        'Undersampling',
        'Oversampling', 
        'Smotetomek'
        ]