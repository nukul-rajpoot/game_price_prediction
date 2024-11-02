import time
import zstandard
import json
from datetime import datetime
import csv
import os
import logging
import sys
import multiprocessing
from functools import partial
import pickle
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

# Initialize global analyzer for multiprocessing
global_analyzer = None

def init_worker():
    """Initializer for each worker process to set up SentimentIntensityAnalyzer once."""
    global global_analyzer
    global_analyzer = SentimentIntensityAnalyzer()

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

def get_text_content(entry):
    """
    Extract text content from either a comment or post.
    Comments have: body
    Link posts have: title
    Self posts have: title + selftext
    """
    # Return body for comments
    if 'body' in entry:
        return entry['body']
    
    # For posts, combine title and selftext
    title = entry.get('title', '')
    selftext = entry.get('selftext', '')
    
    # Combine title and selftext, ensuring both are strings
    if not isinstance(selftext, str):
        selftext = ''
    if not isinstance(title, str):
        title = ''
    return f"{title}\n{selftext}"

def get_sentiment_scores(text, analyzer):
    """Calculate VADER sentiment scores for the given text."""
    return analyzer.polarity_scores(text)

def get_file_position_map(checkpoint_file):
    """Load or create a map of processed file positions."""
    try:
        with open(checkpoint_file, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

def save_checkpoint(checkpoint_file, position_map):
    """Save the current processing position."""
    # Write to temporary file first, then rename for atomic operation
    temp_file = checkpoint_file + '.tmp'
    with open(temp_file, 'wb') as f:
        pickle.dump(position_map, f)
    os.replace(temp_file, checkpoint_file)  # atomic operation

def producer(input_file, lines_queue, num_workers):
    """Read and decompress the input file, enqueue lines for processing."""
    try:
        for line, _ in read_lines_zst(input_file):
            lines_queue.put(line)
    finally:
        # Send sentinel values to indicate completion
        for _ in range(num_workers):
            lines_queue.put(None)

def consumer(lines_queue, results_queue):
    """Process lines from the queue and enqueue the results."""
    analyzer = SentimentIntensityAnalyzer()
    while True:
        line = lines_queue.get()
        if line is None:
            break  # No more data
        try:
            entry = json.loads(line)
            date = datetime.fromtimestamp(int(entry['created_utc'])).strftime('%Y-%m-%d')
            text = get_text_content(entry)
            scores = get_sentiment_scores(text, analyzer)
            results_queue.put([
                date,
                scores['compound'],
                scores['pos'],
                scores['neu'],
                scores['neg']
            ])
        except (json.JSONDecodeError, KeyError) as e:
            log.warning(f"Error processing line ({type(e).__name__}): {str(e)}")
            continue

def saver(output_file, results_queue, num_workers):
    """Write processed results from the queue to the CSV file."""
    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        while True:
            result = results_queue.get()
            if result == 'DONE':
                break
            writer.writerow(result)

def process_file(input_file, output_file):
    checkpoint_file = f"{output_file}.checkpoint"
    position_map = get_file_position_map(checkpoint_file)
    
    # Skip if file is already completed
    if position_map.get(input_file, {}).get('completed', False):
        log.info(f"Skipping completed file: {input_file}")
        return
    
    file_size = os.stat(input_file).st_size
    num_workers = multiprocessing.cpu_count()
    
    # Initialize output file if starting fresh
    if input_file not in position_map:
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['date', 'compound', 'pos', 'neu', 'neg'])
    
    lines_queue = multiprocessing.Queue(maxsize=10000)
    results_queue = multiprocessing.Queue(maxsize=10000)
    
    # Start saver process
    saver_process = multiprocessing.Process(target=saver, args=(output_file, results_queue, num_workers))
    saver_process.start()
    
    # Start consumer processes
    consumers = []
    for _ in range(num_workers):
        p = multiprocessing.Process(target=consumer, args=(lines_queue, results_queue))
        p.start()
        consumers.append(p)
    
    # Start producer
    producer_process = multiprocessing.Process(target=producer, args=(input_file, lines_queue, num_workers))
    producer_process.start()
    
    # Wait for producer to finish
    producer_process.join()
    
    # Wait for consumers to finish
    for p in consumers:
        p.join()
    
    # Signal saver to finish
    results_queue.put('DONE')
    saver_process.join()
    
    # Mark file as completed
    position_map[input_file] = {'completed': True}
    save_checkpoint(checkpoint_file, position_map)
    
    log.info(f"Sentiment scores have been saved to {output_file}")

if __name__ == "__main__":
    start_time = time.time()
    log.info(f"Calculating sentiment scores for: {', '.join(ITEMS)}")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for file_name in os.listdir(input_directory):
        if file_name.endswith('.zst'):
            input_file = os.path.join(input_directory, file_name)
            output_file_name = os.path.splitext(file_name)[0] + '.csv'
            output_file = os.path.join(output_directory, output_file_name)
            log.info(f"Processing file: {input_file}")
            process_file(input_file, output_file)
    end_time = time.time()
    print(f"Total time taken: {(end_time - start_time)/60:.2f} minutes")

