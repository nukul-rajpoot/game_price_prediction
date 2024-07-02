# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# import statsmodels.api as sm
# import plotly.graph_objects as go
# import pandas as pd
# from ipywidgets import interact, DatePicker
# import numpy as np
# from make_graphs import plot_weighted_least_squares

# from api_calls import fetch_item_from_api, fetch_item_to_df, fetch_daily_cookie, fetch_items

# #api call and fetching dataframe


# dailyCookie = fetch_daily_cookie()
# items = fetch_items()
# current_item = fetch_item_to_df(items[4], dailyCookie)


# df = current_item.copy()

# # Weights = determine the influence of data points in WLS; using weights of 1,1 yields OLS results (OLS has uniform weightings).

# df['date_ordinal'] = df.index.map(pd.Timestamp.toordinal)
# X = df['date_ordinal'].values.reshape(-1, 1)
# y = df['price_usd'].values

# weights = np.linspace(1, 10, len(X))

# model_wls = sm.WLS(y, sm.add_constant(X), weights=weights).fit()
# y_pred = model_wls.predict(sm.add_constant(X))

# split_point = int(len(X) * 0.80)
# X_train, X_test = X[:split_point], X[split_point:]
# y_train, y_test = y[:split_point], y[split_point:]




# start_date_picker = DatePicker(description='Start Date', value=df.index[0], disabled=False)
# end_date_picker = DatePicker(description='End Date', value=df.index[-1], disabled=False)


# interact(lambda start_date, end_date:
#             plot_weighted_least_squares(df, start_date, end_date, y_pred, split_point, y_test),
#             start_date=start_date_picker, end_date=end_date_picker)

