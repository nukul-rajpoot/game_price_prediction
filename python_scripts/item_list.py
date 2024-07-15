import re
import requests
import pandas as pd
import os

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



json_data = get_item_list()
if json_data:

    get_item_list_df = pd.DataFrame(json_data)
    print(get_item_list_df.head)
    get_item_list_df.to_csv('./data/Item_lists/CSGO_Item_List.csv', index=True)
  
else:
    print("Failed to retrieve data")

