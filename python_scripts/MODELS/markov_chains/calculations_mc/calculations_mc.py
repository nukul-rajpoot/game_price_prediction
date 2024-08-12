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
import pandas as pd
import matplotlib.pyplot as plt


def dtmc_state_split(df): 
    df['diff'] = df['price_usd'].diff()
    df['state'] = df['diff'].apply(lambda x: 'up' if x > 0 else 'down')
    df['state'].fillna('none', inplace=True)

    # Create the next_state column by shifting the state column
    df['next_state'] = df['state'].shift(-1)

    transition_counts = pd.crosstab(df['state'], df['next_state'])
    transition_matrix = transition_counts.div(transition_counts.sum(axis=1), axis=0)
    current_state = df['state'].iloc[-1]

    return df, transition_matrix, current_state


def next_state_forecast(transition_matrix, current_state):
    # Find the most probable next event according to transition matrix and current state
    next_state = transition_matrix.loc[current_state].idxmax()
    next_state_probability = transition_matrix.loc[current_state, next_state] * 100

    # infomation; Current state, next_state, next_state_probability. 
    info = f"Transition Matrix:\n{transition_matrix}\n Current state: {current_state}\n Most probable next state: {next_state} at {next_state_probability:.2f}% chance."

    return info


def plot_states(df, item_name):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df.index, df['price_usd'], label='Price USD')

    for i in range(len(df) - 1):
        if df['state'].iloc[i] == 'up':
            ax.axvspan(df.index[i], df.index[i+1], facecolor='green', alpha=0.3)
        elif df['state'].iloc[i] == 'down':
            ax.axvspan(df.index[i], df.index[i+1], facecolor='red', alpha=0.3)

    ax.set_xlabel('Date')
    ax.set_ylabel('Price USD')
    ax.set_title(f"Price USD and States for {item_name}")
    ax.legend()
    return fig, ax