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
GAME_PRICE_PREDICTION_PATH = os.path.abspath(os.path.join(cwd, '..', '..'))

# # for ma:c
#GAME_PRICE_PREDICTION_PATH = os.path.abspath(os.path.join(cwd))

sys.path.insert(0, os.path.abspath(GAME_PRICE_PREDICTION_PATH))

from python_scripts.utilities.api_calls import sanitize_filename

# input the skibbity item's name here :P  NOTE: ITEMS = [] for mispelled items
ITEM = "Redline"
ITEM_SANITIZED = sanitize_filename(ITEM)
ITEMS = [
    "Redline", "Redlne", "Redlien", "Redlin", "Radline", "Ridline", "Redliine", "Redliin", "Redlline", "Reddline", "Redine",
    "Reedline", "Reldine", "Redliene", "Redliune", "Redeln", "Redlene", "Reeline", "Redln", "Reddln", "Redilne",
    "Redlien", "Redliune", "Redlienn", "Redeline", "Redllinne", "Redlinne", "Radlien", "Ridelin", "Redllin", "Reeliene",
    "Ak47 Redline", "Ak-47 Redline", "Ak47 Redlne", "Ak-47 Redlne", "Ak-47 Redlin", "Ak47 Radline", "Ak-47 Ridline", "Ak-47 Redliine", "Ak47 Redlline", "Ak47 Reddline",
    "Ak-47 Redine", "Ak47 Reedline", "Ak-47 Reldine", "Ak-47 Redliene", "Ak47 Redeln", "Ak-47 Redlene", "Ak47 Redliun", "Ak-47 Redillne", "Ak47 Redelne", "Ak-47 Redlline",
    "AK Redline", "AK Redlne", "AK Redlin", "AK Radline", "AK Ridline", "AK Redine", "AK Reedline", "AK Redlline", "AK Reddline", "AK Redln"
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