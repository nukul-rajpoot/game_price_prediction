import pandas as pd
from api_calls import fetch_item_from_api, fetch_daily_cookie, fetch_items
from calculate_metrics import calculate_price_percentage_change, calculate_volume, calculate_market_cap, calculate_market_cap_jupyter
from screening_metrics import calculate_screening_metrics

dailyCookie = fetch_daily_cookie()
items = fetch_items()
hash_item_list = pd.read_csv('./data/Item_lists/hashed_items.csv')



def screening_total_items():
    item_data = []

    # Iterate through each item
   # for index, item in items.iterrows():
    for index,item in hash_item_list.iterrows():
        if index == 20:
            break
        
        substring = item["market_hash_name"].split("'")[1]
        data = fetch_item_from_api(substring, dailyCookie)
        if data is not None:  # Check if data fetching was successful
            df = pd.DataFrame(data)

        metrics_row= calculate_screening_metrics(df,item["market_hash_name"])   
        print(item)
        print(type(item))
        item_data.append(metrics_row)

    # Convert the list of item data to a DataFrame
    item_data_df = pd.DataFrame(item_data)
    
    # Save full data to a CSV
    item_data_df.to_csv('./data/Item_lists/total_screened_items.csv', index=False)

screening_total_items()



def screening_judgement():
    items_data_df = './data/Item_lists/total_screened_items.csv'
    items_data_df = pd.read_csv(items_data_df)

    # Define the conditions for filtering
    volume_condition = items_data_df['30d_volume_metric'] > 1000
    price_condition = items_data_df['last_30d_average_price'] > 2
    
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
    
    # Save filtered data to a CSV
    filtered_data_df.to_csv('./data/Item_lists/accepted_items.csv', index=False)

# Call the screening_judgement function
screening_judgement()
