#!/usr/bin/env python
# coding: utf-8

# ### Get data from Steam Community Market API and save to csv

# In[4]:


# Obtaining the data + inputting items seeking for

import re
import requests
import pandas as pd

dailyCookie = "76561199704981720%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTcwQl8yNDkzRTBDMF80QkU4NSIsICJzdWIiOiAiNzY1NjExOTk3MDQ5ODE3MjAiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MTk4NDY2NDQsICJuYmYiOiAxNzExMTE5ODczLCAiaWF0IjogMTcxOTc1OTg3MywgImp0aSI6ICIwRjJEXzI0QTRFNzRCX0U5NjIxIiwgIm9hdCI6IDE3MTgzNjI3ODYsICJydF9leHAiOiAxNzM2NjE4ODA2LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiODEuMTA1LjIwMS41NyIsICJpcF9jb25maXJtZXIiOiAiOTAuMTk3Ljc5LjEzMyIgfQ.XTBcOgyeTtivY6OjqSHRcovN2l0vg4PY7I1wyYy2xIPpcLDDxSMRPG_3W_qEDliAZDG6qNhk1uZOnmNfdfGNBg"
items = ["Glove Case Key", "Officer Jacques Beltram | Gendarmerie Nationale", "Kilowatt Case", "AK-47 | Blue Laminate (Factory New)", "Glove Case"]
#Use for non-aggregated data
def fetch_item_from_api(item):
    # get historical price data of item from API
    url = "https://steamcommunity.com/market/pricehistory/"
    params = {
        'country': 'US',
        'currency': '1',
        'appid': '730',
        'market_hash_name': item
    }
    cookies = {'steamLoginSecure': dailyCookie}

    response = requests.get(url, params=params, cookies=cookies)
    jsonData = response.json()

    # print error message if request failed
    if response.status_code != 200:
        print(f"Failed to fetch data for {item}. Status code: {response.status_code}")
        return None

    # convert and clean data to dataframe object
    price_history = jsonData['prices']
    price_history_df = pd.DataFrame(price_history, columns=['date', 'price_usd', 'volume'])
    price_history_df['date'] = pd.to_datetime(price_history_df['date'].str[0:-4], format='%b %d %Y %H')
    price_history_df['volume'] = pd.to_numeric(price_history_df['volume'])
    price_history_df.set_index('date', inplace=True)
   
    return price_history_df
#Use for aggregated data
def fetch_item_to_df(item):
    price_history_df = fetch_item_from_api(item)
    grouped_current_item = price_history_df.groupby(pd.Grouper(freq='D')).agg({
    'price_usd':'median',
    'volume':'sum'
    })
    return grouped_current_item

def sanitize_filename(filename):
    """Sanitizes the filename to ensure it is valid for most operating systems."""
    filename = re.sub(r'[\\/*?:"<>|]', '_', filename)  # Replace disallowed characters with underscore
    filename = re.sub(r'\s+', '_', filename)  # Replace spaces with underscores
    return filename

def save_item_to_csv(item):
    csvData = './data/'+ sanitize_filename(item) +'.csv'
    fetch_item_to_df(item).to_csv(csvData, index=True)
    

#0     Nov 29 2016 01: +0      2.017   5261 - original format
## fetch and save data in items to csv - Uncomment this when checking new item or updating previous datasets

# for index, item in enumerate(items):
#     save_item_to_csv(item)






# ### Item Verification

# In[5]:


# Call the method (From Get Data notebook) to get current_item dataframe

from matplotlib import pyplot as plt

current_item = fetch_item_to_df(items[4])
non_aggregated_item = fetch_item_from_api(items[4])
# shows what current item is, note: Array item stats with 0.
print(items[4])
print(current_item.tail())
print(non_aggregated_item.tail())


# ### Plotly start & end date

# In[6]:


START_DATE = current_item.index[0]
END_DATE = current_item.index[-1]
print(current_item)
print(START_DATE)
print(END_DATE)


# ### Historic Price (0)  

# In[7]:


# > Historic Price (Basic)

import plotly.graph_objects as go
import pandas as pd
from ipywidgets import interact, DatePicker
import numpy as np

# renames current item to df
df = current_item.copy()

# Function to update the graph based on the selected date range
def update_graph(start_date, end_date):
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


# Creating interactive widgets for date selection
start_date_picker = DatePicker(description='Start Date', value=START_DATE)
end_date_picker = DatePicker(description='End Date', value=END_DATE)

# Display the interactive widget
interact(update_graph, start_date=start_date_picker, end_date=end_date_picker)





# ### Volume Indicatior (1)

# In[8]:


# > Volume Indicatior (1)

import plotly.graph_objects as go
import pandas as pd
from ipywidgets import interact, DatePicker
import numpy as np

# renames current item to df
df = current_item.copy()

# Function to update the graph based on the selected date range
def update_graph_1(start_date, end_date):
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


# Creating interactive widgets for date selection
start_date_picker = DatePicker(description='Start Date', value=START_DATE)
end_date_picker = DatePicker(description='End Date', value=END_DATE)

# Display the interactive widget
interact(update_graph_1, start_date=start_date_picker, end_date=end_date_picker)



# ### Moving Averages (2)

# In[9]:


# # SIMPLE Moving Average (SMA)                            
#  | Part of Moving Averages (2) block


import plotly.graph_objects as go
import pandas as pd
from ipywidgets import interact, DatePicker
import numpy as np

# renames current item to df
df = current_item.copy()

# calculates the 7-day moving average. 
# change window = to change period for average.
df['smoothened_price'] = df['price_usd'].rolling(window=2).mean()

# Function to update the graph based on the selected date range
def update_graph_2(start_date, end_date):
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


# Creating interactive widgets for date selection
start_date_picker = DatePicker(description='Start Date', value=START_DATE)
end_date_picker = DatePicker(description='End Date', value=END_DATE)

# Display the interactive widget
interact(update_graph_2, start_date=start_date_picker, end_date=end_date_picker)


# In[10]:


# SIMPLE Moving Average (SMA) -  CANDLESTICK  
# | Part of Moving Averages (2) block

# NOTE: this produces candlesticks based on (specified time frame e.g. Weekly) data


import plotly.graph_objects as go
import pandas as pd
from ipywidgets import interact, DatePicker
import numpy as np

# renames current item to df
df = current_item.copy()

# Resample the data to weekly timeframe
# NOTE: Range can be altered: 'W' (week), 'M' (Month), '2D' (2 Days)
new_data = df.resample('M').agg({
   'price_usd': ['max', 'min', 'mean', 'median'],
   'volume': 'sum'
})


# Slices the multi-level columns and renames
new_data.columns = ['high', 'low', 'mean','median', 'volume']
# print(new_data.head(10))

# Function to update the graph based on the selected date range
def update_graph_sma(start_date, end_date):


   mask = (new_data.index >= pd.to_datetime(start_date)) & (new_data.index <= pd.to_datetime(end_date))
   filtered_data = new_data.loc[mask]

   
   # Creating the candlestick chart
   fig = go.Figure(data=[go.Candlestick(x=filtered_data.index,
                                        open=filtered_data['mean'],
                                        high=filtered_data['high'],
                                        low=filtered_data['low'],
                                        close=filtered_data['median'],
                                        name='Candlestick')])
   


   # Formatting
   fig.update_layout(
       title='SMA - Candlestick',
       xaxis_title='Date',
       yaxis_title='Price USD',
       yaxis=dict(
           title='Price USD',
           titlefont_size=16,
           tickfont_size=14,
       ),
       
       showlegend=True
   )

   fig.show()


# Creating interactive widgets for date selection
start_date_picker = DatePicker(description='Start Date', value=START_DATE)
end_date_picker = DatePicker(description='End Date', value=END_DATE)

# Display the interactive widget
interact(update_graph_sma, start_date=start_date_picker, end_date=end_date_picker)


# In[11]:


#CANDLESTICK BUT WITH FIRST AND LAST INSTEAD OF MEAN AND MEDIAN

import plotly.graph_objects as go
import pandas as pd
from ipywidgets import interact, DatePicker
import numpy as np

# renames current item to df
df = current_item.copy()

# Resample the data to weekly timeframe
# NOTE: Range can be altered: 'W' (week), 'M' (Month), '2D' (2 Days)
new_data = df.resample('w').agg({
    'price_usd': ['max', 'min', 'first', 'last'],
    'volume': 'sum'
})


# Slices the multi-level columns and renames
new_data.columns = ['high', 'low', 'open', 'close' ,'volume']


# Function to update the graph based on the selected date range
def update_graph(start_date, end_date):
 

    mask = (new_data.index >= pd.to_datetime(start_date)) & (new_data.index <= pd.to_datetime(end_date))
    filtered_data = new_data.loc[mask]

    
    # Creating the candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=filtered_data.index,
                                         open=filtered_data['open'],
                                         high=filtered_data['high'],
                                         low=filtered_data['low'],
                                         close=filtered_data['close'],
                                         name='Candlestick')])
    


    # Formatting
    fig.update_layout(
        title='SMA - Candlestick',
        xaxis_title='Date',
        yaxis_title='Price USD',
        yaxis=dict(
            title='Price USD',
            titlefont_size=16,
            tickfont_size=14,
        ),
        
        showlegend=True
    )

    fig.show()




# Creating interactive widgets for date selection
start_date_picker = DatePicker(description='Start Date', value=START_DATE)
end_date_picker = DatePicker(description='End Date', value=END_DATE)

# Display the interactive widget

interact(update_graph, start_date=start_date_picker, end_date=end_date_picker)


# ### Exponential Moving Average

# In[12]:


# Exponential Moving Average (EMA)  
# | Part of Moving Averages (2) block

import plotly.graph_objects as go
import pandas as pd
from ipywidgets import interact, DatePicker
import numpy as np

# renames current item to df
df = current_item.copy()

# change span = to change smoothing factor/span for average.
df['smoothened_price'] = df['price_usd'].ewm(span=2, adjust=False).mean()
# Function to update the graph based on the selected date range
def update_graph_ema(start_date, end_date):
   # Filtering the data based on the date range
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

# Creating interactive widgets for date selection
start_date_picker = DatePicker(description='Start Date', value=START_DATE)
end_date_picker = DatePicker(description='End Date', value=END_DATE)

# Display the interactive widget
interact(update_graph_ema, start_date=start_date_picker, end_date=end_date_picker)


# ## Regression modelling

# ### OLS / Linear regression (3.1)

# In[13]:


# Linear Regression (3.1)

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
import pandas as pd
from ipywidgets import interact, DatePicker
import numpy as np

df = current_item.copy()

df['date_ordinal'] = df.index.map(pd.Timestamp.toordinal)
X = df['date_ordinal'].values.reshape(-1, 1)
y = df['price_usd'].values


# train test split (first 80% train, last 20% test)
split_point = int(len(X) * 0.80)  
X_train, X_test = X[:split_point], X[split_point:]
y_train, y_test = y[:split_point], y[split_point:]


# intialize the model (like initialising a variable)
model_lr = LinearRegression()
model_lr.fit(X, y)

# make predictions
y_pred = model_lr.predict(X)


def update_graph_3point1v1(start_date, end_date):
    # Filtering the data based on the date range
    mask = (df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))
    filtered_data = df.loc[mask]
    filtered_pred = y_pred[mask]

    # Creating the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_data.index[:split_point], y=filtered_data['price_usd'], mode='lines+markers', name='Price USD'))

     # Add the test set prices
    fig.add_trace(go.Scatter(x=filtered_data.index[split_point:], y=y_test, mode='lines+markers', name='Test Set Data', line=dict(dash='dash')))


    # Add the predicted prices
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_pred, mode='lines', name='Regression Line', line=dict(dash='dot')))

    # Formatting
    fig.update_layout(
        title='Linear Regression ML Model (3.1)',
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


# Creating interactive widgets for date selection
start_date_picker = DatePicker(description='Start Date', value=START_DATE)
end_date_picker = DatePicker(description='End Date', value=END_DATE)

# Display the interactive widget
interact(update_graph_3point1v1, start_date=start_date_picker, end_date=end_date_picker)




# In[14]:


# Linear Regression (3.1) FUTURE MODELLING STRATEGY

# Linear Regression (3.1)

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
import pandas as pd
from ipywidgets import interact, DatePicker
import numpy as np

df = current_item.copy()

df['date_ordinal'] = df.index.map(pd.Timestamp.toordinal)
X = df['date_ordinal'].values.reshape(-1, 1)
y = df['price_usd'].values

# THIS SECTION IS FOR FUTURE PRICE PREDICTION:
future_dates = pd.date_range(start=df.index[-1], end='2025-12-31')
future_dates_ordinal = future_dates.map(pd.Timestamp.toordinal).values.reshape(-1, 1)

# intialize the model (like initialising a variable)
model_lr = LinearRegression()
model_lr.fit(X, y)

# make predictions
y_pred = model_lr.predict(future_dates_ordinal)

# Create a DataFrame for future predictions
future_df = pd.DataFrame(data={'date': future_dates, 'price_usd': y_pred})
future_df.set_index('date', inplace=True)

# Combine df and future_df
combined_df = pd.concat([df, future_df])

def update_graph_3point1v2(start_date, end_date):
    # Filtering the data based on the date range
    mask = (combined_df.index >= pd.to_datetime(start_date)) & (combined_df.index <= pd.to_datetime(end_date))
    filtered_data = combined_df.loc[mask]

    # Creating the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data['price_usd'], mode='lines+markers', name='Price USD'))

    # Add the predicted prices
    fig.add_trace(go.Scatter(x=future_df.index, y=future_df['price_usd'], mode='lines', name='Predicted Price', line=dict(dash='dot')))

    # Formatting
    fig.update_layout(
        title='Linear Regression ML Model (3.1)',
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

# Creating interactive widgets for date selection
start_date_picker = DatePicker(description='Start Date', value=combined_df.index[0], disabled=False)
end_date_picker = DatePicker(description='End Date', value=combined_df.index[-1], disabled=False)

# Display the interactive widget
interact(update_graph_3point1v2, start_date=start_date_picker, end_date=end_date_picker)


# ### WLSR / Weighted Least Squares Estimator (3.2)

# In[15]:


# Weighted Least Squares Estimator (3.2) - 
# Note: this makes OLS (above) redundant since you can adjust weighting to 1 in the 'weight' array

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
import pandas as pd
from ipywidgets import interact, DatePicker
import numpy as np
import statsmodels.api as sm


df = current_item.copy()

# Convert date to ordinal for regression
df['date_ordinal'] = df.index.map(pd.Timestamp.toordinal)
X = df['date_ordinal'].values.reshape(-1, 1)
y = df['price_usd'].values

# Create weights: more recent data points have higher weights
weights = np.linspace(1, 1, len(X))

# Train test split (first 80% train, last 20% test)
split_point = int(len(X) * 0.80)
X_train, X_test = X[:split_point], X[split_point:]
y_train, y_test = y[:split_point], y[split_point:]
weights_train, weights_test = weights[:split_point], weights[split_point:]

# Initialize and fit the WLS model
model_wls = sm.WLS(y, sm.add_constant(X), weights=weights).fit()

get_ipython().system('~')
y_pred = model_wls.predict(sm.add_constant(X))

# Update graph function
def update_graph_3point2(start_date, end_date):
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

# Creating interactive widgets for date selection
start_date_picker = DatePicker(description='Start Date', value=df.index[0], disabled=False)
end_date_picker = DatePicker(description='End Date', value=df.index[-1], disabled=False)

# Display the interactive widget
interact(update_graph_3point2, start_date=start_date_picker, end_date=end_date_picker)


# ## Bollinger Bands (4)

# In[16]:


# # Bollinger Bands - Bolligner Bands currently use the SMA but the chart depicts the historical price                           


import plotly.graph_objects as go
import pandas as pd
from ipywidgets import interact, DatePicker
import numpy as np

# Assuming 'current_item' is your DataFrame with a DateTime index and a 'price_usd' column.
df = current_item.copy()

# Calculate the 20-day moving average. Change window=20 to change the period for the average.
df['smoothened_price'] = df['price_usd'].rolling(window=20).mean()

# Calculate the rolling standard deviation for the 20-day window.
df['std_dev'] = df['price_usd'].rolling(window=20).std()

# Calculate the Bollinger Bands.
df['upper_band'] = df['smoothened_price'] + 2 * df['std_dev']
df['lower_band'] = df['smoothened_price'] - 2 * df['std_dev']

# Function to update the graph based on the selected date range.
def update_graph_4(start_date, end_date):
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

# Creating interactive widgets for date selection.
start_date_picker = DatePicker(description='Start Date', value=START_DATE)
end_date_picker = DatePicker(description='End Date', value=END_DATE)

# Display the interactive widget.
interact(update_graph_4, start_date=start_date_picker, end_date=end_date_picker)


# ## Percentage Change (5)

# In[17]:


# Percentage Change output

from ipywidgets import DatePicker, interact

df_change = current_item.copy()

def update_graph_change(start_date, end_date):
    filtered_data = df_change.loc[start_date:end_date]

    percentage_change = (filtered_data['price_usd'].iloc[-1] - filtered_data['price_usd'].iloc[0]) / filtered_data['price_usd'].iloc[0] * 100
    
    print(f"Percentage change in price_usd from {start_date} to {end_date}: {percentage_change:.2f}%")

start_date_picker_change = DatePicker(description='Start Date', value=START_DATE)
end_date_picker_change = DatePicker(description='End Date', value=END_DATE)

interact(update_graph_change, start_date=start_date_picker_change, end_date=end_date_picker_change)






# ### RSI

# In[18]:


import plotly.graph_objects as go
import pandas as pd
from ipywidgets import interact, DatePicker
import numpy as np

#renames n to df
df = non_aggregated_item.copy()

rsi_data = df.resample('2d').agg({
    'price_usd': ['max', 'min', 'first', 'last'],
    'volume': 'sum'
})

    # Slices the multi-level columns and renames
rsi_data.columns = ['high', 'low', 'open', 'close' ,'volume']

def update_graph(start_date, end_date):
    # Filtering the data based on the date range.
    mask = (rsi_data.index >= pd.to_datetime(start_date)) & (rsi_data.index <= pd.to_datetime(end_date))
    filtered_data = rsi_data.loc[mask]

    # Calculating the daily price change
    rsi_data['price_change'] = rsi_data['close'].diff()
    
    #Separating the positive and negative price changes
    rsi_data['gain'] = rsi_data['price_change'].apply(lambda x: x if x > 0 else 0)
    rsi_data['loss'] = rsi_data['price_change'].apply(lambda x: abs(x) if x < 0 else 0)
  
    #calculate average gain and loss
    rsi_data['avg_gain'] = rsi_data['gain'].rolling(window=14).mean()
    rsi_data['avg_loss'] = rsi_data['loss'].rolling(window=14).mean()
    
    #calculate relative strength
    rsi_data['rs'] = rsi_data['avg_gain'] / rsi_data['avg_loss']
  
    #calculate relative strength index
    rsi_data['rsi'] = 100 - (100 / (1 + rsi_data['rs']))
   
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
# Creating interactive widgets for date selection.
start_date_picker = DatePicker(description='Start Date', value=START_DATE)
end_date_picker = DatePicker(description='End Date', value=END_DATE)

# Display the interactive widget.
interact(update_graph, start_date=start_date_picker, end_date=end_date_picker)


    

