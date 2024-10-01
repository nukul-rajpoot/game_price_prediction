import os
import pandas as pd

# Directory containing the mention data CSV files
mention_data_directory = './data/Reddit_data/mention_data/redline_from_compressed_data'

# List to store individual dataframes
dataframes = []

# Iterate over each file in the mention_data directory
for file_name in os.listdir(mention_data_directory):
    if file_name.endswith('.csv'):
        file_path = os.path.join(mention_data_directory, file_name)
        df = pd.read_csv(file_path)
        dataframes.append(df)

# Concatenate all dataframes into a single dataframe
combined_df = pd.concat(dataframes, ignore_index=True)

# Convert the 'date' column to datetime
combined_df['date'] = pd.to_datetime(combined_df['date'])

# Group by 'date' and sum the 'num_mentions'
summed_df = combined_df.groupby('date', as_index=False)['num_mentions'].sum()

# Sort the summed dataframe by date
summed_df = summed_df.sort_values(by='date')

# Display the summed dataframe
print(summed_df)

# Save the summed dataframe to a new CSV file if needed
summed_df.to_csv('./data/Reddit_data/mention_ALL/redline_from_ALL.csv', index=False)
