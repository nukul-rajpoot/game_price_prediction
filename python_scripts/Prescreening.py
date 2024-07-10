from api_calls import fetch_item_from_api, fetch_daily_cookie, fetch_items
from calculate_metrics import calculate_price_percentage_change
import pandas as pd

dailyCookie = fetch_daily_cookie()
items = fetch_items()

def fetch_item_to_df(items, dailyCookie, output_csv='item_data.csv'):
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

            # Calculate price percentage change
            price_change = calculate_price_percentage_change(df, start_date, end_date)



        # Append the item name and metrics calculated
        item_data.append({
            'item_name': item,
            'price_percentage_change': price_change
        })

    # Convert the list of item data to a DataFrame
    item_data_df = pd.DataFrame(item_data)

    # Write the DataFrame to a CSV file
    item_data_df.to_csv(output_csv, index=False)
    print(f"Data written to {output_csv}")

# Fetch data, calculate metrics, and write to CSV
fetch_item_to_df(items, dailyCookie, output_csv='item_data.csv')