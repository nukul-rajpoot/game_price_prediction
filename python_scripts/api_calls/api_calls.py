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


def fetch_daily_cookie():
    dailyCookie = "76561199704981720||eyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTRGOV8yNDkzRTBBMF8wNzExRSIsICJzdWIiOiAiNzY1NjExOTk3MDQ5ODE3MjAiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MjAzNjY5NDMsICJuYmYiOiAxNzExNjM5MjMyLCAiaWF0IjogMTcyMDI3OTIzMiwgImp0aSI6ICIwRjJEXzI0QTRFN0ExX0I0Q0RCIiwgIm9hdCI6IDE3MTgyNzM5NjQsICJydF9leHAiOiAxNzIwODM0MTkxLCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiOTAuMTk3Ljc5LjEzMyIsICJpcF9jb25maXJtZXIiOiAiOTAuMTk3Ljc5LjEzMyIgfQ.stG-uCzxvhlZGDGUo3IyBfDLCWlS774y9CrM0dw5-TvxpTYDrAizkGgMXp8eLys2VnE__vCJi-bQNVX3EkPUAw"
    return dailyCookie

def fetch_items():
    items = ["Glove Case Key", "Officer Jacques Beltram | Gendarmerie Nationale", "Kilowatt Case", "AK-47 | Blue Laminate (Factory New)", "Glove Case"]
    return items





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
    csv_data = './data/'+ sanitize_filename(item) +'.csv'
    fetch_item_to_df(item, dailyCookie).to_csv(csv_data, index=True)
    
#0     Nov 29 2016 01: +0      2.017   5261 - original format
