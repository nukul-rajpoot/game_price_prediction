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




#Reads CSGO_Item_list file and returns it
def read_CSGO_item_list():
    item_list = pd.read_csv('./data/Item_lists/CSGO_Item_List.csv')

    return item_list




def generate_CSGO_hashed_item_list():
    # Calls read_item_list function
    item_list = read_CSGO_item_list()
    #Creates dataframe to store output
    hashed_items = pd.DataFrame(columns =("market_hash_name", "hash"))

    #for loop which goes through each row in dataframe iteratively
    for index, row in item_list.iterrows():
    #Cuts row to what we need
        substring = row["data"].split("'")[7]
    #Hashes each substring into 8 digits
        hash_substring = int(hashlib.sha256(substring.encode('utf-8')).hexdigest(), 16) 
    #Adds item name and hash into respective columns
        hashed_items.loc[index] = ["'" + str(substring)+ "'"] + [ str(hash_substring)]
    print(hashed_items)
    #Saves to CSV
    hashed_items.to_csv('./data/Item_lists/hashed_items.csv', index=False)
