"""

!!!!!! WRITE PROPER DOCSTRING !!!!!!
This module provides utility functions for string manipulations. It includes functions to 
transform case, check palindrome status, and count specific characters within a string.

Functions:
- to_upper_case(s): Converts a string to uppercase.
- is_palindrome(s): Checks whether a string is a palindrome.
- char_frequency(s, char): Returns the frequency of a character in a string.

Example usage:
>>> to_upper_case('hello')
'HELLO'
>>> is_palindrome('radar')
True
>>> char_frequency('hello world', 'l')
3
"""


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import pandas as pd
import numpy as np

# Convert date to ordinal for regression

def model_weighted_least_squares(df, weights):

    df['date_ordinal'] = df.index.map(pd.Timestamp.toordinal)
    X = df['date_ordinal'].values.reshape(-1, 1)
    y = df['price_usd'].values


    # Train test split (first 80% train, last 20% test)
    split_point = int(len(X) * 0.80)
    X_train, X_test = X[:split_point], X[split_point:]
    y_train, y_test = y[:split_point], y[split_point:]
    weights_train, weights_test = weights[:split_point], weights[split_point:]

    # Initialize and fit the WLS model
    model_wls = sm.WLS(y, sm.add_constant(X), weights=weights).fit()


    return model_wls
