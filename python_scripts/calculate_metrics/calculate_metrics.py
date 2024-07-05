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


def create_ln_df(current_item):
    ln_df = current_item.copy()
    ln_df['price_usd_log'] = np.log1p(current_item['price_usd'])
    ln_df['volume_log'] = np.log1p(current_item['volume'])
    return ln_df



# SMA calculation 
def calculate_sma(df, window):
    # rolling = used to change period for average. (this case -> 2 days)
    df['smoothened_price'] = df['price_usd'].rolling(window=window).mean()

    return df



# EMA calculation 
def calculate_ema(df, span):
    df['smoothened_price'] = df['price_usd'].ewm(span=span).mean()

    return df



# Bollinger Bands calculation
def calculate_bollinger_bands(df, window):
    df['smoothened_price'] = df['price_usd'].rolling(window=window).mean()

    df['std_dev'] = df['price_usd'].rolling(window=window).std()

    # Calculates the 2 Bollinger Bands
    df['upper_band'] = df['smoothened_price'] + 2 * df['std_dev']
    df['lower_band'] = df['smoothened_price'] - 2 * df['std_dev']

    return df



# Price Percentage Change calculation
def calculate_price_percentage_change(df, start_date, end_date):
    filtered_data = df.loc[start_date:end_date]
    percentage_change = (filtered_data['price_usd'].iloc[-1] - filtered_data['price_usd'].iloc[0]) / filtered_data['price_usd'].iloc[0] * 100
    print(f"Percentage change in price_usd from {start_date} to {end_date}: {percentage_change:.2f}%")

    return df



def calculate_relative_strength_index(df, window):
    rsi_data = df.resample(window).agg({
        'price_usd': ['max', 'min', 'first', 'last'],
        'volume': 'sum'
    })
    
    # Slice the multi-level columns and rename them
    rsi_data.columns = ['high', 'low', 'open', 'close', 'volume']

    return rsi_data
    
    
def calculate_money_flow_index(df, window):
    # Resample the data
    mfi_data = df.resample(window).agg({
        'price_usd': ['max', 'min', 'first', 'last'],
        'volume': 'sum'
    })
    
    # Slice the multi-level columns and rename them
    mfi_data.columns = ['high', 'low', 'open', 'close', 'volume']
    
    # Calculate typical price
    mfi_data['typical_price'] = (mfi_data['high'] + mfi_data['low'] + mfi_data['close']) / 3
    
    # Calculate raw money flow
    mfi_data['raw_money_flow'] = mfi_data['typical_price'] * mfi_data['volume']
    
    return mfi_data


def calculate_market_cap(market_cap,date):
    market_cap['market_cap'] = market_cap['close'] * market_cap['volume']
    return market_cap.loc[date,'market_cap']


