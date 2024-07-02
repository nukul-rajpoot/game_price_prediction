from matplotlib import pyplot as plt
from api_calls import fetch_item_from_api, fetch_item_to_df
from make_graphs import plot_historic_price

dailyCookie = "REDACTED"
items = ["Glove Case Key", "Officer Jacques Beltram | Gendarmerie Nationale", "Kilowatt Case", "AK-47 | Blue Laminate (Factory New)", "Glove Case"]

def fetch_df_to_webapp(item = "Glove Case"):
    current_item = fetch_item_to_df(item, dailyCookie)
    non_aggregated_item = fetch_item_from_api(item, dailyCookie)
    return current_item, non_aggregated_item

# START_DATE = current_item.index[0]
# END_DATE = current_item.index[-1]