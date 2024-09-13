import praw
import os
import json
from datetime import datetime
import time

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id="1B8l7NvXnPDzxCFT_nxaiw",
    client_secret="epIpdp5GPrtvksytt1wB6JnCwBYTLQ",
    user_agent = "windows:SageSentimentAnalysis:v1.0 (by /u/sagecsgocollector)")

# Set the subreddit name
subreddit_name = "csgo"

# Create a directory for output if it doesn't exist
output_dir = "./data/reddit_data"
os.makedirs(output_dir, exist_ok=True)

# Generate a filename with current date and time
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = os.path.join(output_dir, f"{subreddit_name}_posts_{current_time}.json")

# Collect posts
subreddit = reddit.subreddit(subreddit_name)

posts = []
for post in subreddit.new(limit=None):
    try:
        # Collect comments
        post.comments.replace_more(limit=None)  # Expand all comment trees
        comments = []
        for comment in post.comments.list():
            comment_data = {
                "id": comment.id,
                "author": str(comment.author),
                "body": comment.body,
                "score": comment.score,
                "created_utc": comment.created_utc,
                "parent_id": comment.parent_id,
            }
            comments.append(comment_data)

        post_data = {
            "title": post.title,
            "author": str(post.author),  # Convert to string to handle deleted accounts
            "score": post.score,
            "id": post.id,
            "url": post.url,
            "created_utc": post.created_utc,
            "text": post.selftext,
            "num_comments": post.num_comments,
            "upvote_ratio": post.upvote_ratio,
            "is_self": post.is_self,
            "over_18": post.over_18,
            "spoiler": post.spoiler,
            "link_flair_text": post.link_flair_text,
            "comments": comments
        }
        posts.append(post_data)
    except Exception as e:
        print(f"Error processing post {post.id}: {str(e)}")

    # sleep for 1 second every 100 requests
    if len(posts) % 100 == 0:
        print(f"Processed {len(posts)} posts...")
        time.sleep(1) 

    # stop after 1000 posts
    if len(posts) >= 1000:
        print("Reached post limit. Stopping collection.")
        break

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(posts, f, indent=2)

print(f"Collected {len(posts)} posts. Saved to {output_file}")