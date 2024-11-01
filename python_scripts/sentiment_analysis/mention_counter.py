import time
import zstandard
import orjson
from datetime import datetime
import csv
import os
import logging
import sys
from config import ITEMS, FILTERED_DATA_DIRECTORY, MENTION_DATA_DIRECTORY
from multiprocessing import Pool

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 
!!! ONLY use filter_file for this !!!
- Takes ./data/reddit_data/filtered_data 
- Counts mentions of ITEM  
- Saves as numeric for time-series plotting in ./data/reddit_data/mention_data
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 


# Configuration settings
input_directory = FILTERED_DATA_DIRECTORY
output_directory = MENTION_DATA_DIRECTORY

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
            chunk = read_and_decode(reader, 2**25, (2**27) * 2)
            if not chunk:
                break
            lines = (buffer + chunk).split("\n")
            for line in lines[:-1]:
                yield line.strip(), file_handle.tell()
            buffer = lines[-1]
        reader.close()

def count_mentions(text, words):
    return sum(text.lower().count(word.lower()) for word in words)

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

def process_file(input_file, output_file, words):
    data = {}
    file_size = os.stat(input_file).st_size
    total_lines = 0
    bad_lines = 0

    for line, file_bytes_processed in read_lines_zst(input_file):
        total_lines += 1
        if total_lines % 100000 == 0:
            log.info(f"Processed {total_lines:,} lines : {bad_lines:,} bad lines : {file_bytes_processed:,}:{(file_bytes_processed / file_size) * 100:.0f}%")

        try:
            entry = orjson.loads(line)
            date = datetime.fromtimestamp(int(entry['created_utc'])).strftime('%Y-%m-%d')
            text = get_text_content(entry)
            mentions = count_mentions(text, words)
            if date in data:
                data[date] += mentions
            else:
                data[date] = mentions
                
        except orjson.JSONDecodeError:
            bad_lines += 1
            log.warning(f"Error decoding JSON from line: {line}")
        except KeyError as e:
            bad_lines += 1
            log.warning(f"KeyError: {e} - Skipping this entry")

    log.info(f"Complete : {total_lines:,} : {bad_lines:,}")

    # Write data to CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['date', 'num_mentions'])
        for date, mentions in sorted(data.items()):
            writer.writerow([date, mentions])

    log.info(f"Mention counts have been saved to {output_file}")

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

    # Create a multiprocessing pool with a number of processes equal to the CPU count
    with Pool(8) as pool:
        pool.starmap(
            process_file,
            [
                (
                    f[0],
                    f[1],
                    ITEMS,
                )
                for f in input_files_sorted
            ],
        )

    log.info("All files have been processed.")

if __name__ == "__main__":
    start_time = time.time()
    
    log.info(f"Counting mentions of the words: {', '.join(ITEMS)}")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

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
    print(f"Total time taken: {(end_time - start_time)/60:.2f} minutes")