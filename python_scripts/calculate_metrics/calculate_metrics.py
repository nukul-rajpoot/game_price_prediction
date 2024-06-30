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

def calculate_sma(df, window):
    # rolling = used to change period for average. (this case -> 2 days)
    df['smoothened_price'] = df['price_usd'].rolling(window=window).mean()
    return df

def calculate_ema(df, span):
    df['smoothened_price'] = df['price_usd'].ewm(span=span).mean()
    return df