"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
!!! Configuration settings for sentimental analysis !!!
NOTE: sets word to analyse universally through the folowing:
> filter_file
> mention_counter
> mention_data_combiner
> vader_polarity
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 
# input the skibbity item's name here :P  NOTE: ITEMS = [] for mispelled items
ITEM = "Glove Case"
ITEMS = [
    "Glove Case", "Golve Cace", "Golve Cse", "Golve Casse", "Golve Kase", "Golve Caes", "Golve Cas", "Golve Cease", "Golve Casa", "Golve Case", "Golve Casw",
    "Glov Cace", "Glov Cse", "Glov Casse", "Glov Kase", "Glov Caes", "Glov Cas", "Glov Cease", "Glov Casa", "Glov Case", "Glov Casw",
    "Glowe Cace", "Glowe Cse", "Glowe Casse", "Glowe Kase", "Glowe Caes", "Glowe Cas", "Glowe Cease", "Glowe Casa", "Glowe Case", "Glowe Casw", "Glove box"
    ]

# For filter_file               |    NOTE: (input: compressed -> output: filtered_data (MS) )
INPUT_COMPRESSED = './data/Reddit_data/compressed_data'
FILTERED_DATA_DIRECTORY = f'./data/Reddit_data/filtered_data/{ITEM}_from_compressed_data'

# for mention_counter           |   NOTE:  (input: filtered_data (MS) -> output: mention_data (MS))
MENTION_DATA_DIRECTORY = f'./data/Reddit_data/mention_data/{ITEM}_from_compressed_data'

# mention_data_combiner         |   NOTE:  (input: mention_data (MS) -> output: mention_ALL)  - directories N/A for this.

# For vader_polarity            |    NOTE: (input: filtered -> output: polarity_data)
POLARITY_DATA_DIRECTORY = f'./data/Reddit_data/polarity_data/{ITEM}'
OUTPUT_POLARITY_FORMAT = "csv"

# note: if it handles mispelled ITEMS=[], then denoted as MS
# print(ITEMS)