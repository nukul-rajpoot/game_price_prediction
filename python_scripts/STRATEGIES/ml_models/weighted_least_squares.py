
import statsmodels.api as sm
import pandas as pd
from ipywidgets import interact, DatePicker
import numpy as np
# #api call and fetching dataframe
import sys
import os
current_dir = os.path.abspath(os.curdir)
sys.path.insert(0, current_dir)
from python_scripts.api_calls import fetch_item_to_df, fetch_items, get_cookie_from_blob
from python_scripts.VISUALISATION.make_graphs import plot_weighted_least_squares

dailyCookie = get_cookie_from_blob()
items = fetch_items()

current_item = fetch_item_to_df(items[4], dailyCookie)
#print(items[4])

#print(current_item.tail())
#print(non_aggregated_item.tail())

df = current_item

os. getcwd()

# #dailyCookie = fetch_daily_cookie()
# #items = fetch_items()
# #current_item = fetch_item_to_df(items[4], dailyCookie)


# #df = current_item.copy()

# Weights = determine the influence of data points in WLS; using weights of 1,1 yields OLS results (OLS has uniform weightings).

df['date_ordinal'] = df.index.map(pd.Timestamp.toordinal)

X = df['date_ordinal'].values.reshape(-1, 1)
y = df['price_usd'].values
print((y))
print((X))
weights = np.linspace(1, 10, len(X))

model_wls = sm.WLS(y, sm.add_constant(X), weights=weights).fit()
y_pred = model_wls.predict(sm.add_constant(X))

split_point = int(len(X) * 0.80)
X_train, X_test = X[:split_point], X[split_point:]
y_train, y_test = y[:split_point], y[split_point:]




start_date_picker = DatePicker(description='Start Date', value=df.index[0], disabled=False)
end_date_picker = DatePicker(description='End Date', value=df.index[-1], disabled=False)


interact(lambda start_date, end_date:
            plot_weighted_least_squares(df, start_date, end_date, y_pred, split_point, y_test),
            start_date=start_date_picker, end_date=end_date_picker)

