import os
import pandas as pd
from config import ITEM, POLARITY_DATA_DIRECTORY, ALL_POLARITY_DATA

# Directory containing the polarity data CSV files
input_file = POLARITY_DATA_DIRECTORY
output_file = ALL_POLARITY_DATA

# List to store individual dataframes
dataframes = []

# Iterate over each file in the polarity_data directory
for file_name in os.listdir(input_file):
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_file, file_name)
        df = pd.read_csv(file_path)
        dataframes.append(df)

# Concatenate all dataframes into a single dataframe
combined_df = pd.concat(dataframes, ignore_index=True)

# Convert the 'date' column to datetime
combined_df['date'] = pd.to_datetime(combined_df['date'])

# Group by 'date' and calculate mean for each sentiment score
averaged_df = combined_df.groupby('date', as_index=False).agg({
    'compound': 'mean',
    'pos': 'mean',
    'neu': 'mean',
    'neg': 'mean'
})

# Sort the averaged dataframe by date
averaged_df = averaged_df.sort_values(by='date')

# Save to CSV
averaged_df.to_csv(output_file, index=False)
print(f"ALL available polarity scores FOR {ITEM} have been combined into {output_file}")
