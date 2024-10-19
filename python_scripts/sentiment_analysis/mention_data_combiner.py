import os
import pandas as pd
from config import ITEM, MENTION_DATA_DIRECTORY, ALL_MENTIONS_DATA

# Directory containing the mention data CSV files
input_file = MENTION_DATA_DIRECTORY
output_file = ALL_MENTIONS_DATA

# List to store individual dataframes
dataframes = []

# Iterate over each file in the mention_data directory
for file_name in os.listdir(input_file):
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_file, file_name)
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

# Skibbity sigma rizz
summed_df.to_csv(output_file, index=False)
print(f"ALL available mention_data FOR {ITEM} has been combined into {output_file}")
