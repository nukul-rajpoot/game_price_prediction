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


"""
Model 2 functions. (Hidden Markov Model)
"""

def discretize_data(data, num_points):
    edges = np.linspace(data.min(), data.max(), num_points + 1)
    discretized = np.digitize(data, edges[1:-1])
    return discretized - 1


def map_2d_to_1d(x, y, x_max): 
    return y * x_max + x


def map_1d_to_2d(n, x_max):
    y = n // x_max
    x = n % x_max
    return x, y



"""
Model 1 functions. (DTMC)
"""

def dtmc_state_split(df): 
    dtmc_df = df.copy()  
    dtmc_df['diff'] = dtmc_df['price_usd'].diff()
    dtmc_df['state'] = dtmc_df['diff'].apply(lambda x: 'up' if x > 0 else 'down')
    dtmc_df['state'].fillna('none', inplace=True)

    # Create the next_state column by shifting the state column
    dtmc_df['next_state'] = dtmc_df['state'].shift(-1)

    transition_counts = pd.crosstab(dtmc_df['state'], dtmc_df['next_state'])
    dtmc_transition_matrix = transition_counts.div(transition_counts.sum(axis=1), axis=0)
    dtmc_current_state = dtmc_df['state'].iloc[-1]

    return dtmc_df, dtmc_transition_matrix, dtmc_current_state


def dtmc_forecast(dtmc_transition_matrix, dtmc_current_state):
    # Find the most probable next event according to transition matrix and current state
    dtmc_next_state = dtmc_transition_matrix.loc[dtmc_current_state].idxmax()
    dtmc_next_state_probability = dtmc_transition_matrix.loc[dtmc_current_state, dtmc_next_state] * 100

    # infomation; Current state, next_state, next_state_probability. 
    dtmc_info = f"Transition Matrix:\n{dtmc_transition_matrix}\n Current state: {dtmc_current_state}\n Most probable next state: {dtmc_next_state} at {dtmc_next_state_probability:.2f}% chance."

    return dtmc_info


def dtmc_plot_states(dtmc_df, item_name):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(dtmc_df.index, dtmc_df['price_usd'], label='Price USD')

    for i in range(len(dtmc_df) - 1):
        if dtmc_df['state'].iloc[i] == 'up':
            ax.axvspan(dtmc_df.index[i], dtmc_df.index[i+1], facecolor='green', alpha=0.3)
        elif dtmc_df['state'].iloc[i] == 'down':
            ax.axvspan(dtmc_df.index[i], dtmc_df.index[i+1], facecolor='red', alpha=0.3)

    ax.set_xlabel('Date')
    ax.set_ylabel('Price USD')
    ax.set_title(f"Price USD and States for {item_name}")
    ax.legend()
    return fig, ax