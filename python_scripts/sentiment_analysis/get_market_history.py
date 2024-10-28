import sys
import os
import pandas as pd
import time  # Add this import
import requests

GAME_PRICE_PREDICTION_PATH = os.environ.get('GAME_PRICE_PREDICTION_PATH', '')
sys.path.insert(0, os.path.abspath(GAME_PRICE_PREDICTION_PATH))

from python_scripts.utilities.api_calls import fetch_item_to_df, get_cookie_from_blob

dailyCookie = get_cookie_from_blob()
item_list = pd.read_csv('./data/item_lists/market_hash_names.csv')

def collect_market_history():
    # Load existing processed items if the file exists
    history_file = './data/market_history/total_market_history.csv'
    processed_items_file = './data/market_history/processed_items.csv'
    
    # Create directory if it doesn't exist
    os.makedirs('./data/market_history', exist_ok=True)
    
    # Fix the processed items tracking
    if os.path.exists(processed_items_file):
        processed_items_df = pd.read_csv(processed_items_file)
        processed_items = processed_items_df['item_name'].tolist()
    else:
        processed_items_df = pd.DataFrame(columns=['item_name'])
        processed_items = []

    # Initialize total_history_df
    if os.path.exists(history_file):
        total_history_df = pd.read_csv(history_file)
        total_history_df['date'] = pd.to_datetime(total_history_df['date'])
        total_history_df.set_index('date', inplace=True)
        total_history_df['price_usd'] = pd.to_numeric(total_history_df['price_usd'], errors='coerce')
        total_history_df['volume'] = pd.to_numeric(total_history_df['volume'], errors='coerce')
    else:
        total_history_df = pd.DataFrame()

    # Iterate through each item
    for index, item in item_list.iterrows():
        if index == 23000:
            break
        
        item_name = item["market_hash_name"]
        if item_name in processed_items:
            print(f"{item_name} already processed. Skipping...")
            continue

        # Add retry logic and rate limiting
        max_retries = 3
        retry_delay = 5  # seconds
        
        for attempt in range(max_retries):
            try:
                df = fetch_item_to_df(item_name, dailyCookie)
                if df is not None:
                    if total_history_df.empty:
                        total_history_df = df.copy()
                    else:
                        all_dates = total_history_df.index.union(df.index)
                        total_history_df = total_history_df.reindex(all_dates)
                        df_reindexed = df.reindex(all_dates)
                        
                        total_history_df['price_usd'] = total_history_df['price_usd'].fillna(0) + df_reindexed['price_usd'].fillna(0)
                        total_history_df['volume'] = total_history_df['volume'].fillna(0) + df_reindexed['volume'].fillna(0)
                    
                    processed_items_df = pd.concat([processed_items_df, pd.DataFrame({'item_name': [item_name]})], ignore_index=True)
                    processed_items.append(item_name)
                    print(f"History for {item_name} added to totals successfully.")
                    break
                else:
                    if attempt < max_retries - 1:
                        print(f"Attempt {attempt + 1} failed for {item_name}. Retrying after {retry_delay} seconds...")
                        time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                    else:
                        print(f"Failed to fetch data for {item_name} after {max_retries} attempts.")
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 500:
                    if attempt < max_retries - 1:
                        print(f"HTTP 500 error for {item_name}. Attempt {attempt + 1}. Retrying after {retry_delay} seconds...")
                        time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                        continue
                    else:
                        print(f"Failed to fetch data for {item_name} after {max_retries} attempts due to HTTP 500 errors.")
                else:
                    raise  # Re-raise other HTTP errors
        
        time.sleep(0.5)  # Rate limiting between requests

        # Save progress every 10 items
        if len(processed_items_df) % 10 == 0:
            total_history_df.to_csv(history_file)
            processed_items_df.to_csv(processed_items_file, index=False)

    # Before final save, remove any remaining NaN values
    total_history_df.fillna(0, inplace=True)
    
    # Save final results
    total_history_df.to_csv(history_file)
    processed_items_df.to_csv(processed_items_file, index=False)

collect_market_history()
