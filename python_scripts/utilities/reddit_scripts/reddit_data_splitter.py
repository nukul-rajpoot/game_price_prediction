import os
import sys
import zstandard as zstd
import io

GAME_PRICE_PREDICTION_PATH = os.environ.get('GAME_PRICE_PREDICTION_PATH', '')
sys.path.insert(0, os.path.abspath(GAME_PRICE_PREDICTION_PATH))


def split_zst_file(input_file, max_chunk_size_mb):
    """
    Splits a .zst file into smaller chunks of approximately max_chunk_size_mb while preserving lines.

    :param input_file: Path to the input .zst file.
    :param max_chunk_size_mb: Desired maximum size of each chunk in megabytes.
    """
    dctx = zstd.ZstdDecompressor()
    max_chunk_size = max_chunk_size_mb * 1024 * 1024
    base_filename = os.path.splitext(os.path.basename(input_file))[0]
    chunk_number = 0
    current_chunk = []
    current_chunk_size = 0

    output_dir = os.path.join(GAME_PRICE_PREDICTION_PATH, "data/reddit_data/compressed_data")
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, 'rb') as f:
        with dctx.stream_reader(f) as reader:
            text_reader = io.TextIOWrapper(reader, encoding='utf-8')
            for line in text_reader:
                line_size = len(line.encode('utf-8'))
                
                # Check if adding this line would exceed the max chunk size
                if current_chunk_size + line_size > max_chunk_size and current_chunk:
                    write_chunk(base_filename, chunk_number, current_chunk, output_dir)
                    chunk_number += 1
                    current_chunk = []
                    current_chunk_size = 0

                # Add the line to the current chunk
                current_chunk.append(line)
                current_chunk_size += line_size

            # Write the final chunk if there are leftover lines
            if current_chunk:
                write_chunk(base_filename, chunk_number, current_chunk, output_dir)


def write_chunk(base_filename, chunk_number, lines, output_dir):
    """
    Compresses and writes a chunk of lines to a new .zst file.

    :param base_filename: Base name of the original file.
    :param chunk_number: Sequential number of the current chunk.
    :param lines: List of lines to write in the chunk.
    :param output_dir: Directory where the chunk files will be saved.
    """
    output_filename = os.path.join(output_dir, f"{base_filename}_chunk{chunk_number}.zst")
    
    # Compress and write the chunk
    cctx = zstd.ZstdCompressor()
    with cctx.stream_writer(open(output_filename, 'wb')) as writer:
        for line in lines:
            writer.write(line.encode('utf-8'))
    
    print(f"Wrote {output_filename}")


def process_all_files(compressed_data_dir, min_size_mb, max_chunk_size_mb):
    """
    Processes all .zst files in the specified directory that are larger than min_size_mb.

    :param compressed_data_dir: Directory containing .zst files.
    :param min_size_mb: Minimum file size in megabytes to process.
    :param max_chunk_size_mb: Maximum size of each chunk in megabytes.
    """
    min_size_bytes = min_size_mb * 1024 * 1024
    for root, _, files in os.walk(compressed_data_dir):
        for file in files:
            if file.endswith('.zst'):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                if file_size > min_size_bytes:
                    print(f"Processing {file_path} ({file_size / (1024 * 1024):.2f} MB)")
                    split_zst_file(file_path, max_chunk_size_mb)
                else:
                    print(f"Skipping {file_path} (size below {min_size_mb}MB)")


if __name__ == "__main__":
    compressed_data_directory = os.path.join(GAME_PRICE_PREDICTION_PATH, "data/reddit_data/compressed_data")
    process_all_files(compressed_data_dir=compressed_data_directory, min_size_mb=700, max_chunk_size_mb=3000)
