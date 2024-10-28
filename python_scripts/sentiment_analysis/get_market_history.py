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

        # Simplified retry logic
        for attempt in range(3):  # 3 attempts
            try:
                df = fetch_item_to_df(item_name, dailyCookie)
                if df is not None and not df.empty:
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
                    print(f"Attempt {attempt + 1}/3 failed for {item_name}")
                    if attempt < 2:  # If not the last attempt
                        print("Retrying in 5 seconds...")
                        time.sleep(5)
                    else:
                        print("All attempts failed. Stopping script.")
                        sys.exit(1)  # Stop the script
            except Exception as e:
                print(f"Error on attempt {attempt + 1}/3: {str(e)}")
                if attempt < 2:  # If not the last attempt
                    print("Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print("All attempts failed. Stopping script.")
                    sys.exit(1)  # Stop the script

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
