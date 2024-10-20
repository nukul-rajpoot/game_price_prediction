import json
import pandas as pd

"""
NOTE: CLEANS reddit raw file data -> here are the PARAMTERS WE KEEP

body: Actual comment text
created_utc: Timestamp of comment creation (in UTC)
link_id: ID of the post containing this comment
parent_id: ID of parent comment or post
retrieved_on: When the data was collected
score: Net upvotes (upvotes minus downvotes)
subreddit: Name of the subreddit
subreddit_id: Unique identifier for the subreddit
"""

params_to_keep = ['body', 'created_utc', 'link_id', 'parent_id', 'retrieved_on', 'score', 'subreddit', 'subreddit_id']

# Read data, clean data, write to df 
cleaned_data = []
with open('./data/reddit_data/RAOfCSGO_comments', 'r') as file:
    for line in file:
        comment = json.loads(line)
        cleaned_comment = {param: comment[param] for param in params_to_keep}
        cleaned_data.append(cleaned_comment)

df = pd.DataFrame(cleaned_data)

## save to either CSV or JSON
# df.to_csv('./data/reddit_data/CLEANED_RAOfCSGO_comments.csv', index=False)
df.to_json('./data/reddit_data/CLEANED_RAOfCSGO_comments.json', orient='records', lines=True)