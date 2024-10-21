from rapidfuzz import fuzz
from rapidfuzz import process
import json
import csv
import pandas as pd

"""
NOTE: Mainly redundant. might be some useful stuff here.
"""


df = pd.read_csv('data/item_lists/accepted_items.csv')
df['item_name'].to_csv('output.csv',index=False)
# # Load the json file
# with open('data/reddit_data/RAOfCSGO_comments.json') as f:
#     data = json.load(f)

# # Extract the comment bodies
# comments = []

# for post in data:
#     for comment in post['comments']:
#         comments.append(comment['body'])

# # Create a DataFrame
# df = pd.DataFrame(comments, columns=['body'])

# search_word = 'None'
# threshold = 80

# def fuzzy_word_in_text(text,word,threshold):
#     # Find the most similar word
#     words=text.split()
#     result = process.extract(search_word, df['body'], limit=1)
#     if result[0][1] > threshold:
#         return result[0][0]
#     else:
#         return 'No match found'

# matching_rows = pd.DataFrame(columns=df.columns)
# # Go through each row of the DataFrame
# for index, row in df.iterrows():
#     if fuzzy_word_in_text(row['body'], search_word, threshold):
#         matching_rows = matching_rows._append(row, ignore_index=True)

# # Display the DataFrame with matching rows
# print(f"Rows containing '{search_word}' (with fuzzy matching):")
# print(matching_rows)

# # Save the matching rows to a CSV file
# output_file = 'matching_rows.csv'
# matching_rows.to_csv(output_file, index=False)
# print(f"Matching rows have been saved to {output_file}")