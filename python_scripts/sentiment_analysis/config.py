"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
!!! Configuration settings for sentimental analysis !!!
NOTE: sets word to analyse universally through the folowing:
> filter_file
> mention_counter
> mention_data_combiner
> vader_polarity
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 
# input the skibbity item's name here :P 
ITEM = "redline"

# For filter_file               |    NOTE: (input: compressed -> output: filtered_data)
INPUT_COMPRESSED = './data/Reddit_data/compressed_data'
FILTERED_DATA_DIRECTORY = f'./data/Reddit_data/filtered_data/{ITEM}_from_compressed_data'

# for mention_counter           |   NOTE:  (input: compressed -> output: mention_data)
MENTION_DATA_DIRECTORY = f'./data/Reddit_data/mention_data/{ITEM}_from_compressed_data'

# mention_data_combiner         |   NOTE:  (input: mention_data -> output: mention_ALL)  - directories N/A for this.

# For vader_polarity            |    NOTE: (input: filtered -> output: polarity_data)
POLARITY_DATA_DIRECTORY = f'./data/Reddit_data/polarity_data/{ITEM}'
OUTPUT_POLARITY_FORMAT = "csv"
