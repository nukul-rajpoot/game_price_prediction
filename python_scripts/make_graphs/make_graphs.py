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




# LOG NORMAL HISTORIC PRICE

def plot_lognormalised_historic_price(ln_df, start_date, end_date):
    # Filtering the data based on the date range
    mask = (ln_df.index >= pd.to_datetime(start_date)) & (ln_df.index <= pd.to_datetime(end_date))
    filtered_data = ln_df.loc[mask]

    # Creating the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data['price_usd_log'], mode='lines+markers', name='Price USD (Log)'))

    # Formatting
    fig.update_layout(
        title='Historic Price (Log Normalized) over time',
        xaxis_title='Date',
        yaxis_title='Price USD (Log)',
        yaxis=dict(
            title='Price USD (Log)',
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



# LOG NORMAL HISTORIC VOLUME

def plot_lognormalised_historic_volume(ln_df, start_date, end_date):

    mask = (ln_df.index >= pd.to_datetime(start_date)) & (ln_df.index <= pd.to_datetime(end_date))
    filtered_data = ln_df.loc[mask]

    # Creating the plot
    fig = go.Figure()
    fig.add_trace(go.Bar(x=filtered_data.index, y=filtered_data['volume_log'], name='Volume (Log)'))
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data['volume_log'], mode='lines+markers', name='Volume (Log) Peaks'))


    # Formatting
    fig.update_layout(
        title='Historic Volume (Log Normalized) over time',
        xaxis_title='Date',
        yaxis_title='Volume (Log)',
        yaxis=dict(
            title='Volume (Log)',
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

def plot_simple_moving_average(df, start_date, end_date):

    mask = (df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))
    filtered_data = df.loc[mask]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data['smoothened_price'], mode='lines', name='Smoothened Price'))

    fig.update_layout(
        title='Simple Moving Average Chart',
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



# EXPONENTIAL MOVING AVERAGE

def plot_exponential_moving_average(df, start_date, end_date):
    mask = (df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))
    filtered_data = df.loc[mask]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data['smoothened_price'], mode='lines', name='Smoothened Price'))
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



def plot_bollinger_bands(df, start_date, end_date):
    # Filtering the data based on the date range.
    mask = (df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))
    filtered_data = df.loc[mask]

    # Creating the plot.
    fig = go.Figure()

    # Adding the Historical Price line.
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data['price_usd'], mode='lines', name='Historical Price'))

    # Adding the upper Bollinger Band line.
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data['upper_band'], mode='lines', name='Upper Bollinger Band', line=dict(color='red', dash='dash')))

    # Adding the lower Bollinger Band line.
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data['lower_band'], mode='lines', name='Lower Bollinger Band', line=dict(color='blue', dash='dash')))

    # Formatting the plot.
    fig.update_layout(
        title='Historical Price and Bollinger Bands Chart',
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


def plot_relative_strength_index(start_date, end_date, rsi_data, window):
    # Filtering the data based on the date range.
    mask = (rsi_data.index >= pd.to_datetime(start_date)) & (rsi_data.index <= pd.to_datetime(end_date))
    filtered_data = rsi_data.loc[mask]
   
    # Plotting function
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=rsi_data.index, y=rsi_data['rsi'], mode='lines', name='RSI'))

    # Add horizontal lines at y=30 and y=70 as Scatter traces
    fig.add_trace(go.Scatter(
        x=[filtered_data.index.min(), filtered_data.index.max()],
        y=[30, 30],
        mode="lines",
        line=dict(color="Red", width=1, dash="solid"),
        name="Underbought"
    ))

    fig.add_trace(go.Scatter(
        x=[filtered_data.index.min(), filtered_data.index.max()],
        y=[70, 70],
        mode="lines",
        line=dict(color="Green", width=1, dash="solid"),
        name="Overbought"
    ))
    fig.update_layout(
        title='Relative Strength Index (RSI)',
        xaxis_title='Date',
        yaxis_title='RSI',
        xaxis_rangeslider_visible=True,
        showlegend=True
    )

    fig.show()



def plot_money_flow_index(start_date, end_date, mfi_data, window):
    # Filtering the data based on the date range.
    mask = (mfi_data.index >= pd.to_datetime(start_date)) & (mfi_data.index <= pd.to_datetime(end_date))
    filtered_data = mfi_data.loc[mask]
    
    # Plotting function
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=mfi_data.index, y=mfi_data['mfi'], mode='lines', name='MFI'))

    # Add horizontal lines at y=20 and y=80 as Scatter traces
    fig.add_trace(go.Scatter(
        x=[filtered_data.index.min(), filtered_data.index.max()],
        y=[20, 20],
        mode="lines",
        line=dict(color="Red", width=1, dash="solid"),
        name="Oversold"
    ))

    fig.add_trace(go.Scatter(
        x=[filtered_data.index.min(), filtered_data.index.max()],
        y=[80, 80],
        mode="lines",
        line=dict(color="Green", width=1, dash="solid"),
        name="Overbought"
    ))

    fig.update_layout(
        title='Money Flow Index (MFI)',
        xaxis_title='Date',
        yaxis_title='MFI',
        xaxis_rangeslider_visible=True,
        showlegend=True
    )

    fig.show()