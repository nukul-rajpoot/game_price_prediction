import zstandard
import json
from datetime import datetime
import csv
import os
import logging
import sys
from config import ITEMS, FILTERED_DATA_DIRECTORY, MENTION_DATA_DIRECTORY

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
            chunk = read_and_decode(reader, 2**27, (2**29) * 2)
            if not chunk:
                break
            lines = (buffer + chunk).split("\n")
            for line in lines[:-1]:
                yield line.strip(), file_handle.tell()
            buffer = lines[-1]
        reader.close()

def count_mentions(text, words):
    return sum(text.lower().count(word.lower()) for word in words)

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
            comment = json.loads(line)
            date = datetime.utcfromtimestamp(int(comment['created_utc'])).strftime('%Y-%m-%d')
            mentions = count_mentions(comment['body'], words)
            
            if date in data:
                data[date] += mentions
            else:
                data[date] = mentions
                
        except json.JSONDecodeError:
            bad_lines += 1
            log.warning(f"Error decoding JSON from line: {line}")
        except KeyError as e:
            bad_lines += 1
            log.warning(f"KeyError: {e} - Skipping this comment")

    log.info(f"Complete : {total_lines:,} : {bad_lines:,}")

    # Write data to CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['date', 'num_mentions'])
        for date, mentions in sorted(data.items()):
            writer.writerow([date, mentions])

    log.info(f"Mention counts have been saved to {output_file}")

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
            process_file(input_file, output_file, ITEMS)
