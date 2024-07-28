import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from python_scripts.api_calls import fetch_daily_cookie, fetch_items, fetch_item_to_df

# API request for the item we are modeling
dailyCookie = fetch_daily_cookie()
items = fetch_items()
df = fetch_item_to_df(items[1], dailyCookie)

# Print the df 
print(f"Data for {items[1]} in cache")

# Splitting into up and down state 
df['diff'] = df['price_usd'].diff()
df['state'] = df['diff'].apply(lambda x: 'up' if x > 0 else 'down')
df['state'].fillna('none', inplace=True)
# print(df.head())

# Create the next_state column by shifting the state column
df['next_state'] = df['state'].shift(-1)

# Create a crosstab to count transitions
transition_counts = pd.crosstab(df['state'], df['next_state'], dropna=False)
transition_matrix = transition_counts.div(transition_counts.sum(axis=1), axis=0)

# Fill NaN values with 0 (if there are any states with no transitions)
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