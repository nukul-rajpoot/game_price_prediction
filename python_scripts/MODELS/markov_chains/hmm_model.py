
import pandas as pd
import numpy as np
from hmmlearn import hmm
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from calculations_mc import discretize_data, map_2d_to_1d, map_1d_to_2d, initialise_hmm, fit_hmm, verify_setup
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from python_scripts.api_calls import get_cookie_from_blob, fetch_items, fetch_item_to_df

# API request for the item we are modeling. 
dailyCookie = get_cookie_from_blob()
items = fetch_items()
df = fetch_item_to_df(items[1], dailyCookie)
print(f"Data for {items[1]} in cache")


"""
MODEL 2
NOTE: HMM Model using Liquidity regime splitting. 
"""


##############################
# Data prep & discretization #
##############################
# Calculate fractional changes for price + volume
df['frac_price'] = df['price_usd'].pct_change()
df['frac_volume'] = df['volume'].pct_change()
df = df.dropna()

# Define the number of points for discretizing, and then using function to do so. 
nFC = 50
nFV = 50

df['disc_frac_price'] = discretize_data(df['frac_price'], nFC)
df['disc_frac_volume'] = discretize_data(df['frac_volume'], nFV)

# Map the 2D discrete space to 1D 
df['disc_combined'] = map_2d_to_1d(df['disc_frac_price'], df['disc_frac_volume'], nFC)

# NOTE: For saving dicretized item dataframe. 
# discrete_df = df[['frac_price', 'frac_volume', 'disc_frac_price', 'disc_frac_volume', 'disc_combined']]
# discrete_df.to_csv('./data/HMM_train/Discrete_df.csv', index=False)

# Prepare the data for HMM
X = df[['disc_combined']].values



#############################
# Hidden Markov Model Setup #
#############################
# HYPERPARAMTERS
n_states = 4
covariance_type = "full"
n_iter = 100
random_state = 42

model = initialise_hmm(X, n_states, covariance_type, n_iter, random_state)
model = fit_hmm(model, X)

#  verify the setup
verify_setup(model, n_states, X)



############
# Training #
############



###########################
# Prediction & Forcasting #
###########################



##################
# Metric Testing #
##################