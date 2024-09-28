import zstandard
import os
import json
import sys
import csv
from datetime import datetime
import logging.handlers
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import pandas as pd
import re
from datetime import datetime

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 
!!! ONLY use filter_file for this !!!
- custom VADER script 
- takes filter_file
- outputs polarity
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 


# config
input_file = r"./data/Reddit_data/filtered_data/key_from_csgo_comments.zst"
output_file = r"./data/Reddit_data/polarity_data/key_from_csgo_comments"
output_format = "csv"


single_field = None
write_bad_lines = False
from_date = datetime.strptime("2005-01-01", "%Y-%m-%d")
to_date = datetime.strptime("2030-12-31", "%Y-%m-%d")
field = "body"
values = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
values_file = None
exact_match = False

# Set up logging
log = logging.getLogger("bot")
log.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
log_str_handler = logging.StreamHandler()
log_str_handler.setFormatter(log_formatter)
log.addHandler(log_str_handler)
if not os.path.exists("logs"):
    os.makedirs("logs")
log_file_handler = logging.handlers.RotatingFileHandler(os.path.join("logs", "bot.log"), maxBytes=1024*1024*16, backupCount=5)
log_file_handler.setFormatter(log_formatter)
log.addHandler(log_file_handler)

# Download VADER lexicon
nltk.download('vader_lexicon', quiet=True)

# Initialize VADER
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    return sia.polarity_scores(text)

def sanitize_text(text):
    """
    Convert multi-line text to a single line by replacing newlines with spaces
    and removing any extra whitespace.
    """
    # Replace newlines with spaces
    text = re.sub(r'\n+', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def write_line_zst(handle, line):
    handle.write(line.encode('utf-8'))
    handle.write("\n".encode('utf-8'))

def write_line_json(handle, obj):
    handle.write(json.dumps(obj))
    handle.write("\n")

def write_line_single(handle, obj, field):
    if field in obj:
        handle.write(obj[field])
    else:
        log.info(f"{field} not in object {obj['id']}")
    handle.write("\n")

def write_line_csv(writer, obj, is_submission):
    output_list = []
    created_utc = obj.get('created_utc', '')
    output_list.append(created_utc)
    
    # Convert UTC to date format
    if created_utc:
        date = datetime.utcfromtimestamp(int(created_utc)).strftime('%Y-%m-%d')
    else:
        date = ''
    output_list.append(date)
    
    # Sanitize the body text
    body = sanitize_text(obj.get('body', ''))
    output_list.append(body)
    sentiment = obj.get('sentiment', {})
    output_list.extend([
        sentiment.get('neg', ''),
        sentiment.get('neu', ''),
        sentiment.get('pos', ''),
        sentiment.get('compound', '')
    ])
    output_list.append(obj.get('score', ''))
    writer.writerow(output_list)

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

def process_file(input_file, output_file, output_format, field, values, from_date, to_date, single_field, exact_match):
    output_path = f"{output_file}.{output_format}"
    is_submission = "submission" in input_file
    log.info(f"Input: {input_file} : Output: {output_path} : Is submission {is_submission}")
    writer = None
    if output_format == "zst":
        handle = zstandard.ZstdCompressor().stream_writer(open(output_path, 'wb'))
    elif output_format == "txt":
        handle = open(output_path, 'w', encoding='UTF-8')
    elif output_format == "csv":
        handle = open(output_path, 'w', encoding='UTF-8', newline='')
        writer = csv.writer(handle)
        writer.writerow(['created_utc', 'date', 'body', 'negative', 'neutral', 'positive', 'compound', 'score'])
    else:
        log.error(f"Unsupported output format {output_format}")
        sys.exit()

    file_size = os.stat(input_file).st_size
    created = None
    matched_lines = 0
    bad_lines = 0
    total_lines = 0
    for line, file_bytes_processed in read_lines_zst(input_file):
        total_lines += 1
        if total_lines % 100000 == 0:
            log.info(f"{created.strftime('%Y-%m-%d %H:%M:%S')} : {total_lines:,} : {matched_lines:,} : {bad_lines:,} : {file_bytes_processed:,}:{(file_bytes_processed / file_size) * 100:.0f}%")

        try:
            obj = json.loads(line)
            created = datetime.utcfromtimestamp(int(obj['created_utc']))

            if created < from_date or created > to_date:
                continue

            if field is not None:
                field_value = sanitize_text(obj[field]).lower()
                matched = False
                for value in values:
                    if (exact_match and value == field_value) or (not exact_match and value in field_value):
                        matched = True
                        break
                if not matched:
                    continue

            # Perform sentiment analysis
            if 'body' in obj:
                # Sanitize the body before sentiment analysis
                sanitized_body = sanitize_text(obj['body'])
                sentiment = analyze_sentiment(sanitized_body)
                obj['sentiment'] = sentiment
                obj['body'] = sanitized_body  # Replace the original body with sanitized version

            matched_lines += 1
            if output_format == "zst":
                write_line_zst(handle, json.dumps(obj))
            elif output_format == "csv":
                write_line_csv(writer, obj, is_submission)
            elif output_format == "txt":
                if single_field is not None:
                    write_line_single(handle, obj, single_field)
                else:
                    write_line_json(handle, obj)
            else:
                log.info(f"Something went wrong, invalid output format {output_format}")
        except (KeyError, json.JSONDecodeError) as err:
            bad_lines += 1
            if write_bad_lines:
                if isinstance(err, KeyError):
                    log.warning(f"Key {field} is not in the object: {err}")
                elif isinstance(err, json.JSONDecodeError):
                    log.warning(f"Line decoding failed: {err}")
                log.warning(line)

    handle.close()
    log.info(f"Complete : {total_lines:,} : {matched_lines:,} : {bad_lines:,}")

if __name__ == "__main__":
    if single_field is not None:
        log.info("Single field output mode, changing output file format to txt")
        output_format = "txt"

    if values_file is not None:
        values = []
        with open(values_file, 'r') as values_handle:
            for value in values_handle:
                values.append(value.strip().lower())
        log.info(f"Loaded {len(values)} from values file {values_file}")
    else:
        values = [value.lower() for value in values]  # convert to lowercase

    log.info(f"Filtering field: {field}")
    if len(values) <= 20:
        log.info(f"On values: {','.join(values)}")
    else:
        log.info(f"On values:")
        for value in values:
            log.info(value)
    log.info(f"Exact match {('on' if exact_match else 'off')}. Single field {single_field}.")
    log.info(f"From date {from_date.strftime('%Y-%m-%d')} to date {to_date.strftime('%Y-%m-%d')}")
    log.info(f"Output format set to {output_format}")

    input_files = []
    if os.path.isdir(input_file):
        if not os.path.exists(output_file):
            os.makedirs(output_file)
        for file in os.listdir(input_file):
            if not os.path.isdir(file) and file.endswith(".zst"):
                input_name = os.path.splitext(os.path.splitext(os.path.basename(file))[0])[0]
                input_files.append((os.path.join(input_file, file), os.path.join(output_file, input_name)))
    else:
        input_files.append((input_file, output_file))
    log.info(f"Processing {len(input_files)} files")
    for file_in, file_out in input_files:
        process_file(file_in, file_out, output_format, field, values, from_date, to_date, single_field, exact_match)
