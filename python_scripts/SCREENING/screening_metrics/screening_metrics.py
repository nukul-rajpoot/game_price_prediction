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




import numpy as np
from calculate_metrics import calculate_price_percentage_change, calculate_volume, calculate_market_cap, calculate_market_cap_jupyter
import pandas as pd

def calculate_screening_metrics(df,item):
    # Calculate start_date and end_date
    start_date = df.index[0]
    end_date = df.index[-1]
    last_30d_start = end_date - pd.Timedelta(days=30)
    
    # Calculate price percentage change (lt, 30d)
    latest_price = df['price_usd'].iloc[-1]
    percentage_change = calculate_price_percentage_change(df, start_date, end_date)
    last_30d_percentage_change = calculate_price_percentage_change(df.loc[last_30d_start:end_date], last_30d_start, end_date)
    
    # Calculate the lifetime volume traded (lt, 30d)
    lifetime_volume = calculate_volume(df, start_date, end_date)
    last_30d_volume = calculate_volume(df.loc[last_30d_start:end_date], last_30d_start, end_date)
    
    # Add the 'close' column for market cap calculation
    df['close'] = df['price_usd']
    
    # Calculate market cap (lt, 30d)
    lifetime_market_cap = calculate_market_cap_jupyter(df, start_date, end_date)
    last_30d_market_cap = calculate_market_cap_jupyter(df.loc[last_30d_start:end_date], last_30d_start, end_date)
    
    # Calculate average price (lt, 30d)
    lifetime_average_price = df['price_usd'].mean()
    last_30d_average_price = df.loc[last_30d_start:end_date, 'price_usd'].mean()
    
    # Append the item name + METRICS!
    metrics_row=({
        'item_name': item,
        'latest_price': round(latest_price, 1),
        'lifetime_price_%_change': round(percentage_change, 0),
        '30d_price_%_change': round(last_30d_percentage_change, 2),
        'lifetime_volume': round(lifetime_volume, 0),
        '30d_volume_metric': round(last_30d_volume, 0),
        'lifetime_market_cap': round(lifetime_market_cap, 0),
        '30d_market_cap': round(last_30d_market_cap, 0),
        'lifetime_average_price': round(lifetime_average_price, 2),
        'last_30d_average_price': round(last_30d_average_price, 2),
    })
    return metrics_row