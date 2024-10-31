import time
import zstandard
import os
import json
import sys
import csv
from datetime import datetime
import logging.handlers
from config import ITEM, ITEMS, INPUT_COMPRESSED, FILTERED_DATA_DIRECTORY
from multiprocessing import Pool

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
!!! THIS IS THE ONLY FILE TO DEAL WITH compressed_data !!!
- reads ALL compressed_data, saves to filtered_data based on [ITEM]
- i.e. filters for keyword: [ITEM] from config
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 


# put the path to the input file, or a folder of files to process all of
input_file = INPUT_COMPRESSED
# FILTERING
### !!! DO NOT CHANGE field -
# set to author because we handle the text content in get_text_content()
### !!! DO NOT CHANGE field -
field = "author"  # This can be any non-None value since we're using get_text_content
values = ITEMS

input_file_name = os.path.basename(input_file)
input_file_base = os.path.splitext(input_file_name)[0]  

# for saving 
output_file = FILTERED_DATA_DIRECTORY

# the format to output in, pick from the following options
#   zst: same as the input, a zstandard compressed ndjson file. Can be read by the other scripts in the repo
#   txt: an ndjson file, which is a text file with a separate json object on each line. Can be opened by any text editor
#   csv: a comma separated value file. Can be opened by a text editor or excel
# WARNING READ THIS: if you use txt or csv output on a large input file without filtering out most of the rows, the resulting file will be extremely large. Usually about 7 times as large as the compressed input file
# output_format = "zst"
# override the above format and output only this field into a text file, one per line. Useful if you want to make a list of authors or ids. See the examples below
# any field that's in the dump is supported, but useful ones are
#   author: the username of the author
#   id: the id of the submission or comment
#   link_id: only for comments, the fullname of the submission the comment is associated with
#   parent_id: only for comments, the fullname of the parent of the comment. Either another comment or the submission if it's top level
single_field = None
# the fields in the file are different depending on whether it has comments or submissions. If we're writing a csv, we need to know which fields to write.
# set this to true to write out to the log every time there's a bad line, set to false if you're expecting only some of the lines to match the key
write_bad_lines = False

# only output items between these two dates
from_date = datetime.strptime("2005-01-01", "%Y-%m-%d")
to_date = datetime.strptime("2030-12-31", "%Y-%m-%d")

# the field to filter on, the values to filter with and whether it should be an exact match
# some examples:
#
# return only objects where the author is u/watchful1 or u/spez
# field = "author"
# values = ["watchful1","spez"]
# exact_match = True
#
# return only objects where the title contains either "stonk" or "moon"
# field = "title"
# values = ["stonk","moon"]
# exact_match = False
#
# return only objects where the body contains either "stonk" or "moon". For submissions the body is in the "selftext" field, for comments it's in the "body" field
# field = "selftext"
# values = ["stonk","moon"]
# exact_match = False
#
#
# filter a submission file and then get a file with all the comments only in those submissions. This is a multi step process
# add your submission filters and set the output file name to something unique
# input_file = "redditdev_submissions.zst"
# output_file = "filtered_submissions"
output_format = "zst"
# field = "author"
# values = ["watchful1"]
#
# run the script, this will result in a file called "filtered_submissions.csv" that contains only submissions by u/watchful1
# now we'll run the script again with the same input and filters, but set the output to single field. Be sure to change the output file to a new name, but don't change any of the other inputs
# output_file = "submission_ids"
# single_field = "id"
#
# run the script again, this will result in a file called "submission_ids.txt" that has an id on each line
# now we'll remove all the other filters and update the script to input from the comments file, and use the submission ids list we created before. And change the output name again so we don't override anything
# input_file = "redditdev_comments.zst"
# output_file = "filtered_comments"
# single_field = None  # resetting this back so it's not used
# field = "link_id"  # in the comment object, this is the field that contains the submission id
# values_file = "submission_ids.txt"
# exact_match = False  # the link_id field has a prefix on it, so we can't do an exact match
#
# run the script one last time and now you have a file called "filtered_comments.csv" that only has comments from your submissions above
# if you want only top level comments instead of all comments, you can set field to "parent_id" instead of "link_id"

# if you have a long list of values, you can put them in a file and put the filename here. If set this overrides the value list above
# if this list is very large, it could greatly slow down the process
values_file = None
exact_match = False


# sets up logging to the console as well as a file
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
    output_list.append(str(obj['score']))
    output_list.append(datetime.fromtimestamp(int(obj['created_utc'])).strftime("%Y-%m-%d"))
    if is_submission:
        output_list.append(obj['title'])
    output_list.append(f"u/{obj['author']}")
    output_list.append(f"https://www.reddit.com{obj['permalink']}")
    if is_submission:
        if obj['is_self']:
            if 'selftext' in obj:
                output_list.append(obj['selftext'])
            else:
                output_list.append("")
        else:
            output_list.append(obj['url'])
    else:
        output_list.append(obj['body'])
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
            chunk = read_and_decode(reader, 2**25, (2**27) * 2)

            if not chunk:
                break
            lines = (buffer + chunk).split("\n")

            for line in lines[:-1]:
                yield line.strip(), file_handle.tell()

            buffer = lines[-1]

        reader.close()

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

def process_file(input_file, output_file, output_format, field, values, from_date, to_date, single_field, exact_match):
    output_path = f"{output_file}.{output_format}"
    is_submission = "submission" in input_file
    log.info(f"Input: {input_file} : Output: {output_path} : Is submission {is_submission}")
    writer = None

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if output_format == "zst":
        handle = zstandard.ZstdCompressor().stream_writer(open(output_path, 'wb'))
    elif output_format == "txt":
        handle = open(output_path, 'w', encoding='UTF-8')
    elif output_format == "csv":
        handle = open(output_path, 'w', encoding='UTF-8', newline='')
        writer = csv.writer(handle)
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
            created = datetime.fromtimestamp(int(obj['created_utc']))

            if created < from_date:
                continue
            if created > to_date:
                continue
            
            if field is not None:
                text_content = get_text_content(obj).lower()
                matched = False
                for value in values:
                    if exact_match:
                        if value == text_content:
                            matched = True
                            break
                    else:
                        if value in text_content:
                            matched = True
                            break
                if not matched:
                    continue

            matched_lines += 1
            if output_format == "zst":
                write_line_zst(handle, line)
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
    with Pool(processes=os.cpu_count()) as pool:
        pool.starmap(
            process_file,
            [
                (
                    f[0],
                    f[1],
                    output_format,
                    field,
                    values,
                    from_date,
                    to_date,
                    single_field,
                    exact_match,
                )
                for f in input_files_sorted
            ],
        )

    log.info("All files have been processed.")

if __name__ == "__main__":
    start_time = time.time()

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
    parallel_process_files(input_files)
    
    end_time = time.time()
    print(f"Total time taken: {(end_time - start_time)/60:.2f} minutes")