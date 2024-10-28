import zstandard
import json
from datetime import datetime
import csv
import os
import logging
import sys
from config import ITEMS, FILTERED_DATA_DIRECTORY, POLARITY_DATA_DIRECTORY, INPUT_COMPRESSED
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 
!!! ONLY use filter_file for this !!!
- Takes ./data/reddit_data/filtered_data 
- Calculates polarity scores for each post/comment
- Saves as numeric for time-series plotting in ./data/reddit_data/polarity_data
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 


# Configuration settings
# Set input to INPUT_COMPRESSED to use full reddit data
input_directory = INPUT_COMPRESSED
#input_directory = FILTERED_DATA_DIRECTORY
output_directory = POLARITY_DATA_DIRECTORY

# Set up logging
log = logging.getLogger("bot")
log.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
log_str_handler = logging.StreamHandler()
log_str_handler.setFormatter(log_formatter)
log.addHandler(log_str_handler)

def read_and_decode(reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0):
    chunk = reader.read(chunk_size)
    bytes_read += chunk_size
    if previous_chunk is not None:
        chunk = previous_chunk + chunk
    try:
        return chunk.decode()
    except UnicodeDecodeError:
        if bytes_read > max_window_size:
            raise UnicodeError(f"Unable to decode frame after reading {bytes_read:,} bytes")
        log.info(f"Decoding error with {bytes_read:,} bytes, reading another chunk")
        return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)

def read_lines_zst(file_name):
    with open(file_name, 'rb') as file_handle:
        buffer = ''
        reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
        while True:
            chunk = read_and_decode(reader, 2**27, (2**29) * 2)
            if not chunk:
                break
            lines = (buffer + chunk).split("\n")
            for line in lines[:-1]:
                yield line.strip(), file_handle.tell()
            buffer = lines[-1]
        reader.close()

def get_text_content(item):
    """Extract text content from either a comment or post."""
    if 'body' in item:  # It's a comment
        return item['body']
    else:  # It's a post
        text = item['title']  # Title is always present
        if item['selftext']:  # Add selftext if not empty
            text += '\n' + item['selftext']
        return text

def get_sentiment_scores(text, analyzer):
    """Calculate VADER sentiment scores for the given text."""
    return analyzer.polarity_scores(text)

def process_file(input_file, output_file):
    analyzer = SentimentIntensityAnalyzer()  # Create once per file
    total_lines = 0
    bad_lines = 0
    file_size = os.stat(input_file).st_size

    # Open output file immediately to write as we go
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['date', 'compound', 'pos', 'neu', 'neg'])  # Header row

        for line, file_bytes_processed in read_lines_zst(input_file):
            total_lines += 1
            if total_lines % 100000 == 0:
                log.info(f"Processed {total_lines:,} lines : {bad_lines:,} bad lines : {file_bytes_processed:,}:{(file_bytes_processed / file_size) * 100:.0f}%")

            try:
                item = json.loads(line)
                date = datetime.fromtimestamp(int(item['created_utc'])).strftime('%Y-%m-%d')
                
                # Get text content and sentiment scores
                text = get_text_content(item)
                scores = get_sentiment_scores(text, analyzer)
                
                # Write the scores immediately
                writer.writerow([
                    date,
                    scores['compound'],
                    scores['pos'],
                    scores['neu'],
                    scores['neg']
                ])
                    
            except json.JSONDecodeError:
                bad_lines += 1
                log.warning(f"Error decoding JSON from line: {line}")
            except KeyError as e:
                bad_lines += 1
                log.warning(f"KeyError: {e} - Skipping this comment")

    log.info(f"Complete : {total_lines:,} : {bad_lines:,}")
    log.info(f"Sentiment scores have been saved to {output_file}")

if __name__ == "__main__":
    log.info(f"Counting mentions of the words: {', '.join(ITEMS)}")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for file_name in os.listdir(input_directory):
        if file_name.endswith('.zst'):
            input_file = os.path.join(input_directory, file_name)
            output_file_name = os.path.splitext(file_name)[0] + '.csv'
            output_file = os.path.join(output_directory, output_file_name)
            log.info(f"Processing file: {input_file}")
            process_file(input_file, output_file)
