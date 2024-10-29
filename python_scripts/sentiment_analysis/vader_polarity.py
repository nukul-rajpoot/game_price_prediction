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
input_directory = INPUT_COMPRESSED
# input_directory = FILTERED_DATA_DIRECTORY
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

def process_chunk(chunk_info, output_file):
    """Process a specific chunk of the input file."""
    chunk_id, total_chunks, input_file = chunk_info
    analyzer = SentimentIntensityAnalyzer()
    results = []
    total_lines = 0
    bad_lines = 0
    
    for line_num, (line, _) in enumerate(read_lines_zst(input_file)):
        # Distribute lines across chunks
        if line_num % total_chunks != chunk_id:
            continue
            
        total_lines += 1
        if total_lines % 10000 == 0:
            log.info(f"Chunk {chunk_id}: Processed {total_lines:,} lines")

        try:
            entry = json.loads(line)
            date = datetime.fromtimestamp(int(entry['created_utc'])).strftime('%Y-%m-%d')
            text = get_text_content(entry)
            scores = get_sentiment_scores(text, analyzer)
            
            results.append([
                date,
                scores['compound'],
                scores['pos'],
                scores['neu'],
                scores['neg']
            ])
                
        except (json.JSONDecodeError, KeyError) as e:
            bad_lines += 1
            log.warning(f"Error processing line ({type(e).__name__}): {str(e)}")
            continue

    return total_lines, bad_lines, results

def process_file(input_file, output_file):
    checkpoint_file = f"{output_file}.checkpoint"
    position_map = get_file_position_map(checkpoint_file)
    
    # Skip if file is already completed
    if position_map.get(input_file, {}).get('completed', False):
        log.info(f"Skipping completed file: {input_file}")
        return
    
    file_size = os.stat(input_file).st_size
    num_cores = multiprocessing.cpu_count()
    
    # Create chunks based on core count instead of file size
    chunks = [(i, num_cores, input_file) for i in range(num_cores)]
    
    # Initialize output file if starting fresh
    if input_file not in position_map:
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['date', 'compound', 'pos', 'neu', 'neg'])
    
    # Process chunks in parallel
    try:
        with multiprocessing.Pool(num_cores) as pool:
            process_chunk_partial = partial(process_chunk, output_file=output_file)
            results = pool.map(process_chunk_partial, chunks)
            
        # Aggregate results
        total_lines = sum(r[0] for r in results)
        total_bad_lines = sum(r[1] for r in results)
        
        # Write all results to file after processing is complete
        with open(output_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for _, _, chunk_results in results:
                for row in chunk_results:
                    writer.writerow(row)
        
        # Mark file as completed
        position_map[input_file] = {'completed': True}
        save_checkpoint(checkpoint_file, position_map)
        
        log.info(f"Complete : {total_lines:,} : {total_bad_lines:,}")
        log.info(f"Sentiment scores have been saved to {output_file}")
        
    except Exception as e:
        log.error(f"Error processing file {input_file}: {str(e)}")
        # Save progress even if there's an error
        save_checkpoint(checkpoint_file, position_map)
        raise

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

