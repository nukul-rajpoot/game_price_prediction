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

import plotly.graph_objects as go
import pandas as pd
from ipywidgets import interact, DatePicker
import numpy as np

# HISTORIC PRICE
def plot_historic_price(df, start_date, end_date):
    # Filtering the data based on the date range
    mask = (df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))
    filtered_data = df.loc[mask]

    # Creating the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data['price_usd'], mode='lines+markers', name='Price USD'))

    # Formatting
    fig.update_layout(
        title='Historic Price over time',
        xaxis_title='Date',
        yaxis_title='Price USD',
        yaxis=dict(
            title='Price USD',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis=dict(  # Added lines for range slider
            rangeslider=dict(
                visible=True
            ),
            type="date"
        ),
        showlegend=True

        )

    fig.show()



# HISTORIC VOLUME
def plot_historic_volume(df, start_date, end_date):
    # Filtering the data based on the date range
    mask = (df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))
    filtered_data = df.loc[mask]

    # Creating the plot
    fig = go.Figure()
    fig.add_trace(go.Bar(x=filtered_data.index, y=filtered_data['volume'], name='Price USD'))

    # Formatting
    fig.update_layout(
        title='Volume Chart',
        xaxis_title='Date',
        yaxis_title='Price USD',
        yaxis=dict(
            title='Price USD',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis=dict(  # Added lines for range slider
            rangeslider=dict(
                visible=True
            ),
            type="date"
        ),
        showlegend=True
    )

    fig.show()



# SIMPLE MOVING AVERAGE
# Function to update the graph based on the selected date range
def plot_simple_moving_average(df, start_date, end_date):
    # Filtering the data based on the date range
    mask = (df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))
    filtered_data = df.loc[mask]

    # Creating the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data['smoothened_price'], mode='lines', name='Smoothened Price'))

    # Formatting
    fig.update_layout(
        title='Simple Moving Average Chart',
        xaxis_title='Date',
        yaxis_title='Price USD',
        yaxis=dict(
            title='Price USD',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis=dict(  # Added lines for range slider
            rangeslider=dict(
                visible=True
            ),
            type="date"
        ),
        showlegend=True

        )

    fig.show()



# EXPONENTIAL MOVING AVERAGE

def plot_exponential_moving_average(df, start_date, end_date):
    mask = (df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))
    filtered_data = df.loc[mask]

    # Creating the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data['smoothened_price'], mode='lines', name='Smoothened Price'))

    # Formatting
    fig.update_layout(
        title='Exponential Moving Average Chart',
        xaxis_title='Date',
        yaxis_title='Price USD',
        yaxis=dict(
            title='Price USD',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis=dict(  # Added lines for range slider
            rangeslider=dict(
                visible=True
            ),
            type="date"
        ),
        showlegend=True

        )
    
    fig.show()



def plot_weighted_least_squares(df, start_date, end_date, y_pred, split_point, y_test):
    # Filtering the data based on the date range
    mask = (df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))
    filtered_data = df.loc[mask]
    filtered_pred = y_pred[mask]

    # Creating the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_data.index[:split_point], y=filtered_data['price_usd'], mode='lines+markers', name='Price USD'))

    # Add the test set prices
    fig.add_trace(go.Scatter(x=filtered_data.index[split_point:], y=y_test, mode='lines+markers', name='Test Set Data'))

    # Add the predicted prices
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_pred, mode='lines', name='Regression Line'))



    # Formatting
    fig.update_layout(
        title='Weighted Least Squares Regression Model',
        xaxis_title='Date',
        yaxis_title='Price USD',
        yaxis=dict(
            title='Price USD',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis=dict(  
            rangeslider=dict(
                visible=True
            ),
            type="date"
        ),
        showlegend=True
    )

    fig.show()