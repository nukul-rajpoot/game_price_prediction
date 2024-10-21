import re
import requests
import pandas as pd
import os
import sys
import csv
sys.path.insert(0, os.path.abspath(''))

import hashlib
from python_scripts.utilities.api_calls import get_item_list

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
        get_item_list_df.to_csv('./data/item_lists/CSGO_Item_List.csv', index=True)
    else:
        print("Failed to retrieve data")

# fetch_CSGO_item_list():

def generate_CSGO_item_list():
    item_list = pd.read_csv('./data/item_lists/CSGO_Item_List.csv')

    # Regular expression patterns
    market_hash_pattern = r"'market_hash_name': '(.*?)', 'border_color'"
    image_pattern = r"'image': '(.*?)',"

    # Extract market_hash_names and image URLs
    market_hash_names = item_list['data'].str.extract(market_hash_pattern, flags=re.DOTALL)
    image_urls = item_list['data'].str.extract(image_pattern, flags=re.DOTALL)

    # Combine the extracted data
    extracted_data = pd.concat([market_hash_names, image_urls], axis=1)
    extracted_data.columns = ['market_hash_name', 'image_url']

    # Remove only the outer single quotes, if present
    extracted_data['market_hash_name'] = extracted_data['market_hash_name'].apply(lambda x: x[1:-1] if x.startswith("'") and x.endswith("'") else x)

    # Sort by market_hash_name
    extracted_data.sort_values('market_hash_name', ascending=True, inplace=True)

    # Save to CSV with quotes
    extracted_data.to_csv('./data/item_lists/market_hash_names.csv', index=False, quoting=csv.QUOTE_ALL)

# generate_CSGO_item_list()