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

# # for windowpros
#game_price_prediction_path = os.path.abspath(os.path.join(cwd, '..', '..'))

# # for ma:c
GAME_PRICE_PREDICTION_PATH = os.path.abspath(os.path.join(cwd))

sys.path.insert(0, os.path.abspath(GAME_PRICE_PREDICTION_PATH))

from python_scripts.utilities.api_calls import sanitize_filename

# input the skibbity item's name here :P  NOTE: ITEMS = [] for mispelled items
ITEM = "Glove Case"
ITEM_SANITIZED = sanitize_filename(ITEM)
ITEMS = [
    "Glove Case", "Golve Cace", "Golve Cse", "Golve Casse", "Golve Kase", "Golve Caes", "Golve Cas", "Golve Cease", "Golve Casa", "Golve Case", "Golve Casw",
    "Glov Cace", "Glov Cse", "Glov Casse", "Glov Kase", "Glov Caes", "Glov Cas", "Glov Cease", "Glov Casa", "Glov Case", "Glov Casw",
    "Glowe Cace", "Glowe Cse", "Glowe Casse", "Glowe Kase", "Glowe Caes", "Glowe Cas", "Glowe Cease", "Glowe Casa", "Glowe Case", "Glowe Casw", "Glove box"
    ]

# For filter_file               |    NOTE: (input: compressed -> output: filtered_data (MS) )
INPUT_COMPRESSED = os.path.join(GAME_PRICE_PREDICTION_PATH, 'data', 'Reddit_data', 'compressed_data')
FILTERED_DATA_DIRECTORY = os.path.join(GAME_PRICE_PREDICTION_PATH, 'data', 'Reddit_data', 'filtered_data', f'{ITEM_SANITIZED}_filtered')

# for mention_counter           |   NOTE:  (input: filtered_data (MS) -> output: mention_data (MS))
MENTION_DATA_DIRECTORY = os.path.join(GAME_PRICE_PREDICTION_PATH, 'data', 'Reddit_data', 'mention_data', f'{ITEM_SANITIZED}_mentions')

# mention_data_combiner         |   NOTE:  (input: mention_data (MS) -> output: mention_ALL)  - directories N/A for this.
ALL_MENTIONS_FILENAME = f'{ITEM_SANITIZED}_all_mentions.csv'
ALL_MENTIONS_DATA = os.path.join(GAME_PRICE_PREDICTION_PATH, 'data', 'Reddit_data', 'mention_all', ALL_MENTIONS_FILENAME)

# For vader_polarity            |    NOTE: (input: filtered -> output: polarity_data)
POLARITY_FOLDER_NAME = f'{ITEM_SANITIZED}_polarity'
POLARITY_DATA_DIRECTORY = os.path.join(GAME_PRICE_PREDICTION_PATH, 'data', 'Reddit_data', 'polarity_data', POLARITY_FOLDER_NAME)
OUTPUT_POLARITY_FORMAT = "csv"

# note: if it handles mispelled ITEMS=[], then denoted as MS
# print(ITEMS)