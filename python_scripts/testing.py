# # import pandas as pd
# # from api_calls import fetch_item_from_api, fetch_daily_cookie, fetch_items
# # from calculate_metrics import calculate_price_percentage_change, calculate_volume, calculate_market_cap, calculate_market_cap_jupyter

# # hash_item_list = pd.read_csv('./data/Item_lists/hashed_items.csv')
# # hash_item_list["market_hash_name"]
# # dailyCookie = fetch_daily_cookie()

# # for index,item in hash_item_list.iterrows():
# #     if index == 12:
# #         break
# #     # substring = item["market_hash_name"].split("'")[1]
# #     print(item["market_hash_name"])

# import pandas as pd
# import regex as re

# # Assuming 'df' is your existing DataFrame and it has a column named 'data' which contains the text
# # Example DataFrame setup (for demonstration)
# data = [
#     "{'market_hash_name': 'Example fffItem 1', 'border_color': '#123456'}",
#     "{'nameID': '176185990', 'market_name': ""SG 553 | Ol' Rusty (Well-Worn)"", 'market_hash_name': ""SG 553 | Ol' Rusty (Well-Worn)"", 'border_color': 'D2D2D2', 'image': 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpopb3wflFf1OD3YjoXuY-JhpWYg-7LPr7Vn35cpsF13rCV8N2i2wa2-UtuMGigJdPAdlU_ZFGD_1e-k-znh5K87pnLzyZ9-n5122JB4kk', 'prices': {'latest': 0.03, 'min': 0.03, 'avg': 0.04, 'max': 0.07, 'mean': 0.04, 'median': 0.043, 'safe': 0.04, 'safe_ts': {'last_24h': 0.04, 'last_7d': 0.04, 'last_30d': 0.04, 'last_90d': 0.04}, 'sold': {'last_24h': 42, 'last_7d': 430, 'last_30d': 1917, 'last_90d': 7437, 'avg_daily_volume': 61}, 'unstable': False, 'unstable_reason': False, 'first_seen': 1596754800000}, 'updated_at': 1720580248000}"
# ]

# df = pd.DataFrame(data, columns=['data'])

# df['data'] = df['data'].str.replace('""', "'")
# print(df["data"])

# # Regular expression pattern to find text between the specified markers
# pattern = r"'market_hash_name': '(.*?)', 'border_color'"

# # Extracting the pattern into a new DataFrame column
# df['market_hash_name'] = df['data'].str.extract(pattern, flags=re.DOTALL)

# # Creating a new DataFrame with the extracted column
# new_df = df[['market_hash_name']]

# # Display the new DataFrame
# print(new_df)


# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# import time

# def get_steam_cookies():
#     # Set up Firefox Selenium WebDriver
#     options = Options()
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument('--disable-gpu')
#     options.add_argument("--remote-debugging-port=9222")
#     options.add_argument("--disable-extensions")
    
#     # Specify your GeckoDriver path
#     gecko_path = 'path/to/your/geckodriver'

#     # Use existing Firefox profile
#     profile_path = "C:/Users/Nukul/AppData/Roaming/Mozilla/Firefox/Profiles/nezbuhz8.default-release-1"
#     options.add_argument(f"--profile={profile_path}")

#     driver_path = 'C:/Users/Nukul/Desktop/Code/game_price_prediction/python_scripts/geckodriver.exe'

#     # Create a new instance of the Firefox driver
#     driver = webdriver.Firefox(options=options)
#     # Create a new instance of the Firefox driver

#     # Go to the Steam website
#     driver.get("https://store.steampowered.com/")

#     # Wait for the page to load
#     time.sleep(10)

#     # Retrieve cookies
#     cookies = driver.get_cookies()

#     # Print cookies
#     print(cookies)

#     # Clean up: close the browser window
#     driver.quit()

#     return cookies

# # Call the function to get cookies
# steam_cookies = get_steam_cookies()
# print(steam_cookies)


#================================================================================================

#================================================================================================


