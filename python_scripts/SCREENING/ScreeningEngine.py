import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pandas as pd


from python_scripts.api_calls import fetch_item_from_api, fetch_daily_cookie, fetch_items
from python_scripts.calculate_metrics import calculate_price_percentage_change, calculate_volume, calculate_market_cap, calculate_market_cap_jupyter
from screening_metrics import calculate_screening_metrics

dailyCookie = fetch_daily_cookie()
items = fetch_items()

hash_item_list = pd.read_csv('./data/Item_lists/hashed_items.csv')



def screening_total_items():
    # Load existing screened items if the file exists
    screened_items_file = './data/Item_lists/total_screened_items.csv'
    screened_items_df = pd.read_csv(screened_items_file) if os.path.exists(screened_items_file) else pd.DataFrame()
    screened_item_names = set(screened_items_df['item_name']) if not screened_items_df.empty else set()

    item_data = []

    # Iterate through each item
    for index, item in hash_item_list.iterrows():
        if index == 23000:
            break
        
        item_name = item["market_hash_name"]
        if item_name in screened_item_names:
            continue  # Skip if the item is already screened

        substring = item_name.split("'")[1]
        data = fetch_item_from_api(substring, dailyCookie)
        if data is not None:  # Check if data fetching was successful
            df = pd.DataFrame(data)
            metrics_row = calculate_screening_metrics(df, item_name)
            item_data.append(metrics_row)
            print(f"Item {item_name} processed successfully.")
        else:
            print(f"Error fetching data for item {item_name}.")

        # Append data every 10 items
        if len(item_data) >= 10:
            item_data_df = pd.DataFrame(item_data)
            screened_items_df = pd.concat([screened_items_df, item_data_df], ignore_index=True) if not screened_items_df.empty else item_data_df
            screened_items_df.to_csv(screened_items_file, index=False)
            item_data = []

    # Append any remaining data
    if item_data:
        item_data_df = pd.DataFrame(item_data)
        screened_items_df = pd.concat([screened_items_df, item_data_df], ignore_index=True) if not screened_items_df.empty else item_data_df
        screened_items_df.to_csv(screened_items_file, index=False)

# screening_total_items()



def screening_judgement():
    items_data_df = './data/Item_lists/total_screened_items.csv'
    items_data_df = pd.read_csv(items_data_df)

    # Define the conditions for filtering
    volume_condition = items_data_df['30d_volume_metric'] > 1000
    price_condition = items_data_df['last_30d_average_price'] > 0.5
    
    # Filtered data that meets the criteria
    filtered_data_df = items_data_df[volume_condition & price_condition]
    
    # Data that does not meet the criteria
    rejected_data_df = items_data_df[~(volume_condition & price_condition)].copy()
    
    # Add reasons for rejection
    rejected_data_df.loc[:, 'rejection_reason'] = ''
    rejected_data_df.loc[~volume_condition, 'rejection_reason'] = 'low_volume'
    rejected_data_df.loc[~price_condition, 'rejection_reason'] += ' low_price'
    
    # Selects only item_name and reject_reason and displays into rejected_data_df
    rejected_data_df = rejected_data_df[['item_name', 'rejection_reason']]

    # Save rejected items to a new CSV
    rejected_data_df.to_csv('./data/Item_lists/rejected-items.csv', index=False)

    filtered_data_df = filtered_data_df.sort_values(by='30d_price_%_change', ascending=False)
    
    # Save filtered data to a CSV
    filtered_data_df.to_csv('./data/Item_lists/accepted_items.csv', index=False)

# Call the screening_judgement function
screening_judgement()



