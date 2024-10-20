import pandas as pd
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', '..')))
sys.path.insert(0, os.path.abspath(''))
from calculations_mc import dtmc_state_split, dtmc_forecast, dtmc_plot_states
# from python_scripts.models.markov_chain_models.calculations_mc import dtmc_state_split, dtmc_forecast, dtmc_plot_states
from python_scripts.utilities.api_calls import get_cookie_from_blob, fetch_items, fetch_item_to_df


# API request for the item we are modeling. Defining item and cache-ing. 
dailyCookie = get_cookie_from_blob()
items = fetch_items()
df = fetch_item_to_df(items[1], dailyCookie)
print(f"Data for {items[1]} in cache")


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MODEL 1
NOTE: Basic 2-state Discrete-Time Markov Chain (DTMC) model. Observed data split into “up” and “down” states based on price dif. 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# calls the state-splitted df, Transition matrix (and current_state)
dtmc_df, dtmc_transition_matrix, dtmc_current_state = dtmc_state_split(df)

# Forecasting for next state. NOTE: info contains current_state, next_state, next_state_probability
dtmc_info = dtmc_forecast(dtmc_transition_matrix, dtmc_current_state)
print(dtmc_info)

# Plots states for primitive visual inspection
fig, ax= dtmc_plot_states(dtmc_df, items[1])
plt.show()
