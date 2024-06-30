from matplotlib import pyplot as plt
from api_calls import fetch_item_from_api, fetch_item_to_df
from make_graphs import plot_historic_price

dailyCookie = "REDACTED"
items = ["Glove Case Key", "Officer Jacques Beltram | Gendarmerie Nationale", "Kilowatt Case", "AK-47 | Blue Laminate (Factory New)", "Glove Case"]

current_item = fetch_item_to_df(items[4], dailyCookie)
non_aggregated_item = fetch_item_from_api(items[4], dailyCookie)
# shows what current item is, note: Array item stats with 0.
# print(items[4])
# print(current_item.tail())
# print(non_aggregated_item.tail())

START_DATE = current_item.index[0]
END_DATE = current_item.index[-1]