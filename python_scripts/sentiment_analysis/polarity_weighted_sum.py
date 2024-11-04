import os
import pandas as pd
import numpy as np
from config import ITEM, POLARITY_DATA_DIRECTORY, ALL_POLARITY_DATA

# Directory containing the polarity data CSV files
input_file = POLARITY_DATA_DIRECTORY
output_file = ALL_POLARITY_DATA

# Add this flag at the top with the imports
USE_WEIGHTING = True  # Set to False to disable weighting

# Define sentiment metrics list before the if/else block
sentiment_metrics = ['compound', 'pos', 'neu', 'neg']

# 1. Combine all CSV files
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

# 2. Calculate weighted sentiment for each individual post/comment
if USE_WEIGHTING:
    # Calculate weights
    combined_df['weight'] = np.where(combined_df['score'] <= 0, 0.1, np.log1p(combined_df['score']))
    
    # Calculate weighted sentiments first
    for metric in sentiment_metrics:
        combined_df[f'weighted_{metric}'] = combined_df[metric] * combined_df['weight']
    
    # Group by date and sum the weighted values
    daily_df = combined_df.groupby('date').agg({
        'weight': 'sum',  # Keep this for reference
        'weighted_compound': 'sum',
        'weighted_pos': 'sum',
        'weighted_neu': 'sum',
        'weighted_neg': 'sum'
    }).reset_index()
    
    # Rename columns to remove 'weighted_' prefix
    daily_df = daily_df.rename(columns={
        'weighted_compound': 'compound',
        'weighted_pos': 'pos',
        'weighted_neu': 'neu',
        'weighted_neg': 'neg'
    })

else:
    # Simple mean without weighting
    daily_df = combined_df.groupby('date', as_index=False).agg({
        'compound': 'mean',
        'pos': 'mean',
        'neu': 'mean',
        'neg': 'mean'
    })
    daily_df = daily_df.sort_values('date')

# 5. Save results
final_df = daily_df[['date'] + sentiment_metrics].sort_values('date')
final_df.to_csv(output_file, index=False)
print(f"ALL available polarity scores FOR {ITEM} have been combined into {output_file}")