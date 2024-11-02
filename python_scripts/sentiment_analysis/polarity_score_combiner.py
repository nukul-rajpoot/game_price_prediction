import os
import pandas as pd
import numpy as np
from config import ITEM, POLARITY_DATA_DIRECTORY, ALL_POLARITY_DATA

# Directory containing the polarity data CSV files
input_file = POLARITY_DATA_DIRECTORY
output_file = ALL_POLARITY_DATA

# 1. Combine all CSV files
dataframes = []

# Iterate over each file in the polarity_data directory
for file_name in os.listdir(input_file):
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_file, file_name)
        df = pd.read_csv(file_path)
        dataframes.append(df)

# Concatenate all dataframes into a single dataframe
# stacks the dataframes on top of each other
combined_df = pd.concat(dataframes, ignore_index=True)

# Convert the 'date' column to datetime
combined_df['date'] = pd.to_datetime(combined_df['date'])

# 2. Calculate weighted sentiment for each individual post/comment
combined_df['weight'] = np.where(combined_df['score'] <= 0, 0.1, np.log1p(combined_df['score']))

# Calculate weighted sentiment scores
sentiment_metrics = ['compound', 'pos', 'neu', 'neg']
for metric in sentiment_metrics:
    combined_df[f'weighted_{metric}'] = combined_df[metric] * combined_df['weight']

# 3. Aggregate all posts/comments by day
daily_df = combined_df.groupby('date').agg({
    'weight': 'sum',
    'weighted_compound': 'sum',
    'weighted_pos': 'sum',
    'weighted_neu': 'sum',
    'weighted_neg': 'sum'
}).reset_index()

# 4. Calculate final daily weighted averages
for metric in sentiment_metrics:
    daily_df[metric] = daily_df[f'weighted_{metric}'] / daily_df['weight']

# 5. Save results
final_df = daily_df[['date'] + sentiment_metrics].sort_values('date')
final_df.to_csv(output_file, index=False)
print(f"ALL available polarity scores FOR {ITEM} have been combined into {output_file}")