import json
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

def process_comments(input_strings):
    # Download VADER lexicon if not already downloaded
    nltk.download('vader_lexicon', quiet=True)

    # Initialize VADER
    sia = SentimentIntensityAnalyzer()

    # Function to perform sentiment analysis
    def analyze_sentiment(text):
        return sia.polarity_scores(text)

    # List to store results
    results = []

    for input_string in input_strings:
        try:
            # Parse the input string to a dictionary
            comment = json.loads(input_string)
            
            # Check if 'body' field exists
            if 'body' in comment:
                # Perform sentiment analysis
                sentiment = analyze_sentiment(comment['body'])
                
                # Create a dictionary with the required fields
                result = {
                    'created_utc': comment.get('created_utc', ''),
                    'body': comment['body'],
                    'negative': sentiment['neg'],
                    'neutral': sentiment['neu'],
                    'positive': sentiment['pos'],
                    'compound': sentiment['compound'],
                    'score': comment.get('score', '')
                }
                
                results.append(result)
            else:
                print(f"Error: 'body' field not found in the comment: {comment.get('id', 'Unknown ID')}")
        except json.JSONDecodeError:
            print("Error: Invalid JSON string. Please check your input.")

    # Create DataFrame
    df = pd.DataFrame(results)
    
    return df

# Example usage
if __name__ == "__main__":
    # List of input strings (you can add more dictionaries here)
    input_strings = [
        '''{"author":"DaPrincePlays","created_utc":"1435003525","removal_reason":null,"gilded":0,"link_id":"t3_3apvc6","score":1,"archived":false,"downs":0,"subreddit_id":"t5_34bq1","retrieved_on":1437264490,"subreddit":"csgogambling","edited":false,"id":"csf481g","name":"t1_csf481g","author_flair_text":null,"body":"When was this made?","author_flair_css_class":null,"controversiality":0,"ups":1,"score_hidden":false,"distinguished":null,"parent_id":"t3_3apvc6"}''',
        '''{"name":"t1_csf75jz","id":"csf75jz","score_hidden":false,"controversiality":0,"author_flair_text":null,"created_utc":"1435008134","subreddit_id":"t5_34bq1","author_flair_css_class":null,"ups":1,"removal_reason":null,"parent_id":"t3_3apvc6","downs":0,"archived":false,"edited":false,"gilded":0,"author":"BhopLife","body":"kek","score":1,"distinguished":null,"subreddit":"csgogambling","retrieved_on":1437266636,"link_id":"t3_3apvc6"}'''
    ]

    # Process the comments
    result_df = process_comments(input_strings)

    # Display the DataFrame
    print(result_df)

    # Optionally, save to CSV
    # result_df.to_csv('sentiment_analysis_results.csv', index=False)
