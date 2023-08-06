'''
Python module for cleaning data for further analysis or plotting.
'''
import sklearn.preprocessing
import pandas


def standardize_df(df):
    '''
    Standardize/scale numerical df columns so that they
    all have variance of 1 and mean of 0.
    '''
    standardized_df = pandas.DataFrame(sklearn.preprocessing.scale(df), index=df.index, columns=df.columns)
    return standardized_df
