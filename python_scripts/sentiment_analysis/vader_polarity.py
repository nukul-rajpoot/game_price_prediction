import time
import zstandard
import json
from datetime import datetime
import csv
import os
import logging
import sys
from config import ITEMS, FILTERED_DATA_DIRECTORY, POLARITY_DATA_DIRECTORY, INPUT_COMPRESSED
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from multiprocessing import Pool
import orjson

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 
Parallel version of vader_polarity.py using file-level parallelization

!!! ONLY use filter_file for this !!!
- Takes ./data/reddit_data/filtered_data 
- Calculates polarity scores for each post/comment
- Saves as numeric for time-series plotting in ./data/reddit_data/polarity_data
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 

# Configuration settings
# input_directory = INPUT_COMPRESSED
input_directory = FILTERED_DATA_DIRECTORY
output_directory = POLARITY_DATA_DIRECTORY

# Set up logging
log = logging.getLogger("bot")
log.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
log_str_handler = logging.StreamHandler()
log_str_handler.setFormatter(log_formatter)
log.addHandler(log_str_handler)

def get_text_content(obj):
    """
    Extract text content from either a comment or post.
    Comments have: body
    Link posts have: title
    Self posts have: title + selftext
    """
    # Return body for comments
    if 'body' in obj:
        return obj['body']
    
    # For posts, combine title and selftext
    title = obj.get('title', '')
    selftext = obj.get('selftext', '')
    
    # Combine title and selftext, ensuring both are strings
    if not isinstance(selftext, str):
        selftext = ''
    if not isinstance(title, str):
        title = ''
    return f"{title}\n{selftext}"

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
            chunk = read_and_decode(reader, 2**25, (2**27) * 2)
            if not chunk:
                break
            lines = (buffer + chunk).split("\n")
            for line in lines[:-1]:
                yield line.strip(), file_handle.tell()
            buffer = lines[-1]
        reader.close()

def get_sentiment_scores(text, analyzer):
    """Calculate VADER sentiment scores for the given text."""
    return analyzer.polarity_scores(text)

def process_file(input_file, output_file):
    """Process a single file with sentiment analysis."""
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    total_lines = 0
    bad_lines = 0
    file_size = os.stat(input_file).st_size

    # Open output file immediately to write as we go
    with open(output_file, 'w', newline='') as csvfile:
        analyzer = SentimentIntensityAnalyzer()
        writer = csv.writer(csvfile)
        writer.writerow(['date', 'score', 'compound', 'pos', 'neu', 'neg'])  # Added 'score' to header

        for line, file_bytes_processed in read_lines_zst(input_file):
            total_lines += 1
            if total_lines % 100000 == 0:
                log.info(f"Processed {total_lines:,} lines : {bad_lines:,} bad lines : {file_bytes_processed:,}:{(file_bytes_processed / file_size) * 100:.0f}%")

            try:
                comment = orjson.loads(line)
                date = datetime.fromtimestamp(int(comment['created_utc'])).strftime('%Y-%m-%d')
                text = get_text_content(comment)
                score = comment.get('score', 1)  # Get score, default to 0 if not present
                # Get sentiment scores
                scores = get_sentiment_scores(text, analyzer)
                
                # Write the scores immediately
                writer.writerow([
                    date,
                    score,
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

def parallel_process_files(input_files):
    """
    Processes files in parallel by sorting them in descending order of size,
    ensuring that the largest files are processed first.
    """
    # Sort input_files by descending size
    input_files_sorted = sorted(
        input_files, key=lambda x: os.path.getsize(x[0]), reverse=True
    )

    log.info(
        f"Processing {len(input_files_sorted)} files sorted by size (largest first)."
    )

    # Create a multiprocessing pool with one less process than CPU count
    with Pool(processes=max(1, os.cpu_count() - 1)) as pool:
        pool.starmap(
            process_file,
            [
                (f[0], f[1])
                for f in input_files_sorted
            ],
        )

    log.info("All files have been processed.")

if __name__ == "__main__":
    start_time = time.time()
    log.info(f"Processing sentiment for mentions of: {', '.join(ITEMS)}")
    
    # Prepare list of input/output file pairs
    input_files = []
    for file_name in os.listdir(input_directory):
        if file_name.endswith('.zst'):
            input_file = os.path.join(input_directory, file_name)
            output_file_name = os.path.splitext(file_name)[0] + '.csv'
            output_file = os.path.join(output_directory, output_file_name)
            input_files.append((input_file, output_file))
    
    log.info(f"Processing {len(input_files)} files")
    parallel_process_files(input_files)
    
    end_time = time.time()
    print(f"Total processing time: {(end_time - start_time)/60:.2f} minutes")