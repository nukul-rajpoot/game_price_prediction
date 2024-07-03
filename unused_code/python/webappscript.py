from matplotlib import pyplot as plt
from api_calls import fetch_item_from_api, fetch_item_to_df
from make_graphs import plot_historic_price

dailyCookie = "76561199704981720%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTcwQl8yNDkzRTBDMF80QkU4NSIsICJzdWIiOiAiNzY1NjExOTk3MDQ5ODE3MjAiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MTk4NDY2NDQsICJuYmYiOiAxNzExMTE5ODczLCAiaWF0IjogMTcxOTc1OTg3MywgImp0aSI6ICIwRjJEXzI0QTRFNzRCX0U5NjIxIiwgIm9hdCI6IDE3MTgzNjI3ODYsICJydF9leHAiOiAxNzM2NjE4ODA2LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiODEuMTA1LjIwMS41NyIsICJpcF9jb25maXJtZXIiOiAiOTAuMTk3Ljc5LjEzMyIgfQ.XTBcOgyeTtivY6OjqSHRcovN2l0vg4PY7I1wyYy2xIPpcLDDxSMRPG_3W_qEDliAZDG6qNhk1uZOnmNfdfGNBg"
items = ["Glove Case Key", "Officer Jacques Beltram | Gendarmerie Nationale", "Kilowatt Case", "AK-47 | Blue Laminate (Factory New)", "Glove Case"]

def fetch_df_to_webapp(item = "Glove Case"):
    current_item = fetch_item_to_df(item, dailyCookie)
    non_aggregated_item = fetch_item_from_api(item, dailyCookie)
    return current_item, non_aggregated_item

def supdog():
    return "supdog"
# START_DATE = current_item.index[0]
# END_DATE = current_item.index[-1]