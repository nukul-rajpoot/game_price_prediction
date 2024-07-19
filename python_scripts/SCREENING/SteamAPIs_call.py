import re
import requests
import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import hashlib
from python_scripts.api_calls import get_item_list

"""
------------------------------------

Calls from SteamAPIs.com and provides full item list of CSGO items 
(~ 22k items)

NOTE: Uses ~20p to run
------------------------------------
"""

def fetch_CSGO_item_list():
    api_item_list = get_item_list()
    if api_item_list:
        get_item_list_df = pd.DataFrame(api_item_list)
        get_item_list_df.to_csv('./data/Item_lists/CSGO_Item_List.csv', index=True)
    else:
        print("Failed to retrieve data")

# fetch_CSGO_item_list():

def generate_CSGO_item_list():
    item_list = pd.read_csv('./data/Item_lists/CSGO_Item_List.csv')

    # double "" in CSGO_Item_List.csv were manually replaced with '
    # Regular expression pattern to get market_hash_name values
    pattern = r"'market_hash_name': '(.*?)', 'border_color'"
    market_hash_names = item_list['data'].str.extract(pattern, flags=re.DOTALL)
    market_hash_names.sort_values(0, ascending=True, inplace=True)

    market_hash_names.to_csv('./data/Item_lists/market_hash_names.csv', index=False, header=False)

generate_CSGO_item_list()