# import pandas as pd
# from api_calls import fetch_item_from_api, fetch_daily_cookie, fetch_items
# from calculate_metrics import calculate_price_percentage_change, calculate_volume, calculate_market_cap, calculate_market_cap_jupyter

# hash_item_list = pd.read_csv('./data/Item_lists/hashed_items.csv')
# hash_item_list["market_hash_name"]
# dailyCookie = fetch_daily_cookie()

# for index,item in hash_item_list.iterrows():
#     if index == 12:
#         break
#     # substring = item["market_hash_name"].split("'")[1]
#     print(item["market_hash_name"])

import pandas as pd
import regex as re

# Assuming 'df' is your existing DataFrame and it has a column named 'data' which contains the text
# Example DataFrame setup (for demonstration)
data = [
    "{'market_hash_name': \"\"Example fffItem 1', 'border_color': '#123456', other data...}",
    "{'market_hash_name': \"\"Example Item 2', 'border_color': '#654321', other data...}"
]


df = pd.DataFrame(data, columns=['data'])

df['data'] = df['data'].str.replace('""', "'", regex=False)

# Regular expression pattern to find text between the specified markers
pattern = r"'market_hash_name': '(.*?)', 'border_color'"

# Extracting the pattern into a new DataFrame column
df['market_hash_name'] = df['data'].str.extract(pattern, flags=re.DOTALL)

# Creating a new DataFrame with the extracted column
new_df = df[['market_hash_name']]

# Display the new DataFrame
print(new_df)
