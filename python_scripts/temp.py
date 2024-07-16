import pandas as pd
from api_calls import fetch_item_from_api, fetch_daily_cookie, fetch_items
from calculate_metrics import calculate_price_percentage_change, calculate_volume, calculate_market_cap, calculate_market_cap_jupyter

hash_item_list = pd.read_csv('/Users/soham/Desktop/gpp pear/game_price_prediction/data/Item_lists/hashed_items.csv')
hash_item_list["market_hash_name"]
dailyCookie = fetch_daily_cookie()

for index,item in hash_item_list.iterrows():
    if index == 12:
        break
    substring = item["market_hash_name"].split("'")[1]
    bro= fetch_item_from_api(substring, dailyCookie)
    print(substring)
    