"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
!!! Configuration settings for sentimental analysis !!!
NOTE: sets word to analyse universally through the folowing:
> filter_file
> mention_counter
> mention_data_combiner
> vader_polarity
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 

import os,sys
cwd = os.getcwd()
print(cwd)

GAME_PRICE_PREDICTION_PATH = os.environ.get('GAME_PRICE_PREDICTION_PATH', '')

sys.path.insert(0, os.path.abspath(GAME_PRICE_PREDICTION_PATH))

from python_scripts.utilities.api_calls import sanitize_filename

# input the skibbity item's name here :P  NOTE: ITEMS = [] for mispelled items
#ITEM = "ALL DATA"
ITEM = "M4A1-S | Golden Coil (Factory New)"
ITEM_SANITIZED = sanitize_filename(ITEM)
ITEMS = [
    "M4A1-S | Golden Coil", "Golden Coil", "GoldenCoil", "M4A1-S", "M4A1S", 
    "M4A1 S", "M4A1-S Golden Coil", "M4A1S GoldenCoil", 
    "Golden Coil M4A1-S", "GoldenCoil M4A1-S", "Golden Coil M4A1S", 
    "GoldenCoil M4A1S", "M4A1S Golden Coil", "GoldenCoil M4A1 S",
    "M4AI-S", "M4AIS", "Golden Coi", "Golden Cool", "GoldenCoil M4AIS", 
    "M4A1-S Golden Coi", "M4A1-S Goldon Coil", "M4A1S Goldon Coil"
]

# For filter_file               |    NOTE: (input: compressed -> output: filtered_data (MS) )
INPUT_COMPRESSED = os.path.join(GAME_PRICE_PREDICTION_PATH, 'data', 'reddit_data', 'compressed_data')
FILTERED_DATA_DIRECTORY = os.path.join(GAME_PRICE_PREDICTION_PATH, 'data', 'reddit_data', 'filtered_data', f'{ITEM_SANITIZED}_filtered')

# for mention_counter           |   NOTE:  (input: filtered_data (MS) -> output: mention_data (MS))
MENTION_DATA_DIRECTORY = os.path.join(GAME_PRICE_PREDICTION_PATH, 'data', 'reddit_data', 'mention_data', f'{ITEM_SANITIZED}_mentions')

# mention_data_combiner         |   NOTE:  (input: mention_data (MS) -> output: mention_ALL)  - directories N/A for this.
ALL_MENTIONS_FILENAME = f'{ITEM_SANITIZED}_all_mentions.csv'
ALL_MENTIONS_DATA = os.path.join(GAME_PRICE_PREDICTION_PATH, 'data', 'reddit_data', 'mention_all', ALL_MENTIONS_FILENAME)

# For vader_polarity            |    NOTE: (input: filtered -> output: polarity_data)
POLARITY_FOLDER_NAME = f'{ITEM_SANITIZED}_polarity'
POLARITY_DATA_DIRECTORY = os.path.join(GAME_PRICE_PREDICTION_PATH, 'data', 'reddit_data', 'polarity_data', POLARITY_FOLDER_NAME)

ALL_POLARITY_FILENAME = f'{ITEM_SANITIZED}_all_polarity.csv'
ALL_POLARITY_DATA = os.path.join(GAME_PRICE_PREDICTION_PATH, 'data', 'reddit_data', 'polarity_all', ALL_POLARITY_FILENAME)
# note: if it handles mispelled ITEMS=[], then denoted as MS
# print(ITEMS)