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

def generate_CSGO_item_list():
    api_item_list = get_item_list()
    if api_item_list:

        get_item_list_df = pd.DataFrame(api_item_list)
        get_item_list_df.to_csv('./data/Item_lists/CSGO_Item_List.csv', index=True)
    
    else:
        print("Failed to retrieve data")

# generate_csgo_item_list():

def generate_CSGO_item_list():
    # Calls read_item_list function
    item_list = pd.read_csv('./data/Item_lists/CSGO_Item_List.csv')
    
    # convert "" into ' 
    item_list['data'] = item_list['data'].str.replace('""', "'", regex=False)

    # Regular expression pattern to get market_hash_name values
    pattern = r"'market_hash_name': '(.*?)', 'border_color'"
    market_hash_names = item_list['data'].str.extract(pattern, flags=re.DOTALL)

    # add hash only when needed
    # hash_substring = int(hashlib.sha256(substring.encode('utf-8')).hexdigest(), 16) 
    market_hash_names.to_csv('./data/Item_lists/market_hash_names.csv', index=False, header=False)

# generate_CSGO_item_list()