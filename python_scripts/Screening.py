import pandas as pd
from api_calls import fetch_item_from_api, fetch_daily_cookie, fetch_items
from calculate_metrics import calculate_price_percentage_change, calculate_volume, calculate_market_cap, calculate_market_cap_jupyter

dailyCookie = fetch_daily_cookie()
items = fetch_items()

def fetch_item_to_df(items, dailyCookie):
    item_data = []

    # Iterate through each item
    for item in items:

        # Fetch data from API
        data = fetch_item_from_api(item, dailyCookie)
        if data is not None:  # Check if data fetching was successful
            df = pd.DataFrame(data)

            # Calculate start_date and end_date
            start_date = df.index[0]
            end_date = df.index[-1]
            last_30d_start = end_date - pd.Timedelta(days=30)
            
            # Calculate price percentage change (lt, 30d)
            latest_price = df['price_usd'].iloc[-1]
            percentage_change = calculate_price_percentage_change(df, start_date, end_date)
            last_30d_percentage_change = calculate_price_percentage_change(df.loc[last_30d_start:end_date], last_30d_start, end_date)
            
            # Calculate the lifetime volume traded (lt, 30d)
            lifetime_volume = calculate_volume(df, start_date, end_date)
            last_30d_volume = calculate_volume(df.loc[last_30d_start:end_date], last_30d_start, end_date)
            
            # Add the 'close' column for market cap calculation
            df['close'] = df['price_usd']
            
            # Calculate market cap (lt, 30d)
            lifetime_market_cap = calculate_market_cap_jupyter(df, start_date, end_date)
            last_30d_market_cap = calculate_market_cap_jupyter(df.loc[last_30d_start:end_date], last_30d_start, end_date)
            
            # Calculate average price (lt, 30d)
            lifetime_average_price = df['price_usd'].mean()
            last_30d_average_price = df.loc[last_30d_start:end_date, 'price_usd'].mean()
            
            # Append the item name + METRICS!
            item_data.append({
                'item_name': item,
                'latest_price': round(latest_price, 1),
                'lifetime_price_%_change': round(percentage_change, 0),
                '30d_price_%_change': round(last_30d_percentage_change, 1),
                'lifetime_volume': round(lifetime_volume, 0),
                '30d_volume_metric': round(last_30d_volume, 0),
                'lifetime_market_cap': round(lifetime_market_cap, 0),
                '30d_market_cap': round(last_30d_market_cap, 0),
                'lifetime_average_price': round(lifetime_average_price, 2),
                'last_30d_average_price': round(last_30d_average_price, 2),
            })
    

    # Convert the list of item data to a DataFrame
    item_data_df = pd.DataFrame(item_data)
    
    # Define the conditions for filtering
    volume_condition = item_data_df['30d_volume_metric'] > 1000
    price_condition = item_data_df['last_30d_average_price'] > 2
    
    # Filtered data that meets the criteria
    filtered_data_df = item_data_df[volume_condition & price_condition]
    
    # Data that does not meet the criteria
    rejected_data_df = item_data_df[~(volume_condition & price_condition)].copy()
    
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
    
    # Save full data to a CSV
    item_data_df.to_csv('./data/Item_lists/total_screened_items.csv', index=False)

# Fetch data, calculate metrics, and write to CSVz
fetch_item_to_df(items, dailyCookie)
