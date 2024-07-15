import re
import requests
import pandas as pd
import os
from api_calls import get_item_list

api_item_list = get_item_list()
if api_item_list:

    get_item_list_df = pd.DataFrame(api_item_list)
    get_item_list_df.to_csv('./data/Item_lists/CSGO_Item_List.csv', index=True)
  
else:
    print("Failed to retrieve data")





