import pandas as pd
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.regime_switching.markov_autoregression import MarkovAutoregression
from sklearn.preprocessing import StandardScaler


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from python_scripts.api_calls import fetch_daily_cookie, fetch_items, fetch_item_to_df

# API request for the item we are modeling
dailyCookie = fetch_daily_cookie()
items = fetch_items()

# Define item +  cache
df = fetch_item_to_df(items[1], dailyCookie)
print(f"Data for {items[1]} in cache")



""" 
NOTE: Price Movement technique

Most basic form of MCM model. 
Onserved data simply split into “up” and “down” states based on price difference. 

"""

# Splitting into up and down state 
df['diff'] = df['price_usd'].diff()
df['state'] = df['diff'].apply(lambda x: 'up' if x > 0 else 'down')
df['state'].fillna('none', inplace=True)

# Create the next_state column by shifting the state column
df['next_state'] = df['state'].shift(-1)

# Create a crosstab to count transitions
transition_counts = pd.crosstab(df['state'], df['next_state'], dropna=False)
transition_matrix = transition_counts.div(transition_counts.sum(axis=1), axis=0)

# Fill NaN values with 0 (if any) & print Transition matrix
transition_matrix = transition_matrix.fillna(0)
print("Transition Matrix:")
print(transition_matrix)


# Determine current state
current_state = df['state'].iloc[-1]
print(f"Current state: {current_state}")

# Find the most probable next event according to transition matrix and current state
next_state = transition_matrix.loc[current_state].idxmax()
next_state_probability = transition_matrix.loc[current_state, next_state] * 100
info_next_state = f"Most probable next state: {next_state} -- {next_state_probability:.2f}% chance."

print(info_next_state)



# Plot the states with background shading
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df['price_usd'], label='Price USD')

# Highlight 'up' and 'down' states with background shading
for i in range(len(df) - 1):
    if df['state'].iloc[i] == 'up':
        ax.axvspan(df.index[i], df.index[i+1], facecolor='green', alpha=0.3)
    elif df['state'].iloc[i] == 'down':
        ax.axvspan(df.index[i], df.index[i+1], facecolor='red', alpha=0.3)

ax.set_xlabel('Date')
ax.set_ylabel('Price USD')
ax.set_title(f"Price USD and States for {items[1]}")
ax.legend()
plt.show()

