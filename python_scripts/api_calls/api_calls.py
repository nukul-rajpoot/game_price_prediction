"""

!!!!!! WRITE PROPER DOCSTRING !!!!!!
This module provides utility functions for string manipulations. It includes functions to 
transform case, check palindrome status, and count specific characters within a string.

Functions:
- to_upper_case(s): Converts a string to uppercase.
- is_palindrome(s): Checks whether a string is a palindrome.
- char_frequency(s, char): Returns the frequency of a character in a string.

Example usage:
>>> to_upper_case('hello')
'HELLO'
>>> is_palindrome('radar')
True
>>> char_frequency('hello world', 'l')
3
"""
# Obtaining the data + inputting items seeking for

import re
import requests
import pandas as pd 
import os


def fetch_daily_cookie():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cookie_path = os.path.join(script_dir, '..', '..', 'data', 'Cookie.txt')
    with open(cookie_path, 'r') as file:
        dailyCookie = file.read()
    return dailyCookie


def fetch_items():
    items = ["Glove Case Key", "Officer Jacques Beltram | Gendarmerie Nationale", "Kilowatt Case", "AK-47 | Blue Laminate (Factory New)", "Glove Case", "★ StatTrak™ Paracord Knife | Case Hardened (Field-Tested)"]
    return items


#Gets the itemlist from 3rd party api
def get_item_list():
    url = "https://api.steamapis.com/market/items/730?api_key=uJHHr--KdQ-KdymIei9IdHJdMBQ"
   
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


#Use for non-aggregated data
def fetch_item_from_api(item, dailyCookie):
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
    json_data = response.json()
    
    # print error message if request failed
    if response.status_code != 200:
        print(f"Failed to fetch data for {item}. Status code: {response.status_code}")
        return None 
           
    # convert and clean data to dataframe object
    price_history = json_data['prices']
    price_history_df = pd.DataFrame(price_history, columns=['date', 'price_usd', 'volume'])
    price_history_df['date'] = pd.to_datetime(price_history_df['date'].str[0:-4], format='%b %d %Y %H')
    price_history_df['volume'] = pd.to_numeric(price_history_df['volume'])
    price_history_df.set_index('date', inplace=True)
   
    return price_history_df

#Use for aggregated data
def fetch_item_to_df(item, dailyCookie):
    price_history_df = fetch_item_from_api(item, dailyCookie)
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

    
def save_item_to_csv(item, dailyCookie):
    csv_data = './data/Individual_Item_Historic/'+ sanitize_filename(item) +'.csv'
    fetch_item_to_df(item, dailyCookie).to_csv(csv_data, index=True)
    
