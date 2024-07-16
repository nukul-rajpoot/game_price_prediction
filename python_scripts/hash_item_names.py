import re
import requests
import pandas as pd
import os
import hashlib


#Reads CSGO_Item_list file and returns it
def read_item_list():
    item_list = pd.read_csv('/Users/soham/Desktop/gpp pear/game_price_prediction/data/Item_lists/CSGO_Item_List.csv')

    return item_list
# Calls read_item_list function
item_list = read_item_list()
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