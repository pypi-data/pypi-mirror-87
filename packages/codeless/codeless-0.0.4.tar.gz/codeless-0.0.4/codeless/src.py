"""
The :mod:`codeless.src` module includes methods 
to plot different types of graphs.
"""

import matplotlib.pyplot as _plt
import seaborn as _sns
import scipy.stats as _stats
import pylab as _pylab
import math as _math
import numpy as _np



def PlotHist(df, columns, figuresize=(10, 10), bins=40, color='blue'):
    '''
    Plot histogram for all the columns provided using
    matplotlib
    
    Parameters
    -------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/tuple
        list of all the colum names. It must be an iterable like list, set, 
        touple etc
    figsize: tuple, optional
        size of the figure to be plot. value should be passed in tuple. 
        figuresize=(width, height).
    bins:Int, optional 
        what is the size of each bar. By default it is 40.
    color: string, optional
        specify the color of the graph. eg 'red', 'green', 'darkred', 'darkgreen' etc.
    
    Returns
    ----------
    None: This method returns None.
    '''
    # fix the figure size
    _plt.figure(figsize=figuresize)
    
    # find how many rows 
    # no1 = len(columns)/2
    # no2 = len(columns)//2
    # no = no2 if no1==no2 else no2+1
    no = _math.ceil(len(columns)/2)
   
    # for each column plot a graph in the figure
    for index, col in enumerate(columns):
        _plt.subplot(no, 2, index+1)
        _plt.hist(x=col, data=df, color=color, bins=bins)
        _plt.title(col)
    _plt.show()


def PlotDist(df, columns, figuresize=(10, 10), bins=40, color='blue'):
    '''
    This method plots the distplot for all the columns provided using seaborn.
    
    Parameters
    --------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/tuple
        list of all the colum names. It must be an iterable like list, set, 
        touple etc
    figuresize: tuple, optional
        size of the figure to be plot. value should be passed in tuple. 
        figuresize=(width, height).
    bins: Int, optional
        size of each bar. By default it is 40.
    color: string, optional
        color of each bar. eg. 'red', 'green', 'darkred', 'darkgreen' etc
    
    Returns
    --------------
       This method returns None.
    '''
    # fix the figure size
    _plt.figure(figsize=figuresize)
    
    # find how many rows 
    # no1 = len(columns)/2
    # no2 = len(columns)//2
    # no = no2 if no1==no2 else no2+1
    no = _math.ceil(len(columns)/2)
   
    # for each column plot a graph in the figure
    for index, col in enumerate(columns):
        _plt.subplot(no, 2, index+1)
        _sns.distplot(df[col], color=color, bins=bins)


def PlotBox(df, columns, figuresize=(10, 10)):
    '''
    This method plots the boxplot for all the columns provided.
    
    Parameters
    -------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/tuple
        list of all the colum names. It must be an iterable like list, set, 
        touple etc
    figuresize: tuple, optional
        size of the figure to be plot. value should be passed in tuple. 
        figuresize=(width, height).
    
    Returns
    -------------
    None: This method returns None.
    '''
    # fix the figure size
    _plt.figure(figsize=figuresize)
    
    # find how many rows 
    # no1 = len(columns)/2
    # no2 = len(columns)//2
    # no = no2 if no1==no2 else no2+1
    no = _math.ceil(len(columns)/2)
   
    # for each column plot a graph in the figure
    for index, col in enumerate(columns):
        _plt.subplot(no, 2, index+1)
        _plt.boxplot(x=col, data=df)
        _plt.title(col)
    _plt.show()


def PlotQQ(df, columns, figuresize=(10, 20), color='blue', bins=40):
    '''
    Plots QQ graph for all the columns provided.
    
    QQ graph is used to check the distribution of the columns, whether it is
    in Gaussian or not. More the blue points are align with the straight red
    line more Gaussian the distribution is else not.
    
    Parameters
    --------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/tuple
        list of all the colum names. It must be an iterable like list, set, 
        touple etc
    figuresize: tuple, optional
        size of the figure to be plot. value should be passed in tuple. 
        figuresize=(width, height).
    color: string, optional
        color of the histogram of each column.
    bins: int, optional
        size of each histogram bar.
    
    Return
       This method returns None.
    '''
    # fix the figure size
    _plt.figure(figsize=figuresize)
    
    # find how many rows 
    no = len(columns)
   
    # for each column plot a graph in the figure
    count = 1
    for index, col in enumerate(columns):
        _plt.subplot(no, 2, count)
        _plt.hist(x=col, data=df, color=color, bins=bins)
        _plt.title(col)
        _plt.subplot(no, 2, count+1)
        _stats.probplot(df[col], dist='norm', plot=_pylab)
        count = count + 2
        
    _plt.show()


def PlotCount(df, columns, figuresize=(10, 10), grid=True, colormap='vlag'):
    '''
    Plots COUNT PLOT for all the columns provided.
    
    Count Plot is used to see which value is present how many times in 
    the column.
    
    Parameters
    --------------
    df: rectangular dataset
        2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
        is provided, the index/column information will be used to label the
        columns and rows.
    columns: list/set/tuple
        list of all the colum names. It must be an iterable like list, set, 
        touple etc
    figuresize: tuple, optional
        size of the figure to be plot. value should be passed in tuple. 
        figuresize=(width, height).
    grid: Boolean, optional
        if True then grid is shown on the graph for better visualization.
    colormap: String, optional
        style to apply to each graphs. It ranges from [0-5 & 14-23] of 
        _SeabornPalettes() method.
    
    Return
       This method returns None.
    '''
    # fix the figure size
    _plt.figure(figsize=figuresize)
    
    # find how many rows 
    no = len(columns)
   
    # for each column plot a graph in the figure
    for index, col in enumerate(columns):
        _plt.subplot(no, 1, index+1)
        df[col].value_counts().sort_values().plot(kind = 'barh', title=col, 
                                                  grid=grid, legend=True, 
                                                  colormap=colormap)
    _plt.show()



# -------------------------------------ALL SUPPORTED COLORS--------------------------------
def _ColorBlack():
    '''
    This method returns the list of all the black colors supported by matplotlib
    '''
    black = ['black', 'dimgray', 'gray', 'grey']
    return black

def _ColorRed():
    '''
    This method returns the list of all the red colors supported by matplotlib
    '''
    red = ['rosybrown', 'lightcoral', 'indianred', 'brown', 'firebrick', 'maron', 'darkred', 
          'red', 'salmon', 'tomato', 'darksalmon', 'coral', 'orangered', 
           'lightsalmon']
    return red

def _ColorBrown():
    '''
    This method returns the list of all the brown colors supported by matplotlib
    '''
    brown = ['sienna', 'seashell', 'chocolate', 'saddlebrown', 'sandybrown','peru']
    return brown

def _ColorOrange():
    '''
    This method returns the list of all the orange colors supported by matplotlib
    '''
    orange = ['darkorange', 'orange']
    return orange

def _ColorGolden():
    '''
    This method returns the list of all the golden colors supported by matplotlib
    '''
    golden = ['darkgoldenrod', 'goldenrod', 'gold', 'khaki', 'darkkhaki']
    return golden

def _ColorGreen():
    '''
    This method returns the list of all the green colors supported by matplotlib
    '''
    green = ['olive', 'yellow', 'olivedrab', 'yellowgreen', 'darkolivegreen', 'darkseagreen',
            'forestgreen', 'darkgreen', 'green']
    return green

def _ColorBlue():
    '''
    This method returns the list of all the blue colors supported by matplotlib
    '''
    blue = ['mediumaquamarine', 'aquamarine', 'lightseagreen', 'darkturquoise', 
           'deepskyblue', 'dodgerblue', 'cornflowerblue', 'royalblue', 'slateblue', 
            'mediumslateblue']
    return blue

def _ColorPurple():
    '''
    This method returns the list of all the purple colors supported by matplotlib
    '''
    purple = ['rebeccapurple', 'blueviolet', 'plum', 'violet', 'fuchsia', 'mediumvioletred',
             'deeppink', 'hotpink', 'palevioletred', 'crimson', 'pink']
    return purple

# ------------------------------SEABORN STYLES------------------------------------------
def _SeabornStyles():
    '''
    This method returns different style name supported by seaborn
    '''
    styles = ['darkgrid', 'whitegrid', 'dark', 'white', 'ticks']
    return styles

# -----------------------------SEABORN COLOR PALETTES------------------------------------
def _SeabornPalettes():
    '''
    This method returns different palette name supported by seaborn.
    '''
    palette = ['RdBu_r', 'Set1', 'Set2', 'Set3', 'RdPu', 'RdBu', 'dark', 'deep', 'colorblind', 
               'bright', 'muted', 'pastel', 'hls', 'husl', 'Paired', 'rocket', 'mako', 
               'magma', 'viridis', 'rocket_r', 'cubehelix', 'Blues', 'YlOrBr', 'vlag', 
               'icefire', 'Spectral', 'coolwarm']
    return palette




__all__ = [
        'PlotHist()',
        'PlotDist',
        'PlotBox',
        'PlotQQ',
        '_ColorBlack',
        '_ColorRed',
        '_ColorBrown',
        '_ColorOrange',
        '_ColorGolden',
        '_ColorGreen',
        '_ColorBlue',
        '_ColorPurple',
        '_SeabornStyles',
        '_SeabornPalettes'
        ]