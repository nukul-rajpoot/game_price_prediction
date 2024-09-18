import pandas as pd
import json
from datetime import datetime
import csv

# Input file path
input_file = './data/Reddit_data/filtered_data/hi_from_csgo_comments.txt'

# Output file path
output_file = './data/Reddit_data/mention_data/hi_from_csgo_comments.csv'

# Function to count mentions in a text
def count_mentions(text):
    return text.lower().count('hi')

# Read the input file and process each line
data = {}
with open(input_file, 'r') as file:
    for line in file:
        try:
            comment = json.loads(line)
            date = datetime.utcfromtimestamp(int(comment['created_utc'])).strftime('%Y-%m-%d')
            mentions = count_mentions(comment['body'])
            
            if date in data:
                data[date] += mentions
            else:
                data[date] = mentions
                
        except json.JSONDecodeError:
            print(f"Error decoding JSON from line: {line}")
        except KeyError as e:
            print(f"KeyError: {e} - Skipping this comment")

# Convert the data to a DataFrame
df = pd.DataFrame(list(data.items()), columns=['date', 'num_mentions'])

# Sort by date
df = df.sort_values('date')

# Save to CSV
df.to_csv(output_file, index=False)

print(f"Mention counts have been saved to {output_file}")
