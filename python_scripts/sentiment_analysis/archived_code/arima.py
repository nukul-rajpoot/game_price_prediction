# Assuming 'volume' is your target series
model = auto_arima(df['volume'], seasonal=False, trace=True)
print(model.summary())

# Define the model based on chosen (p, d, q)
p, d, q = model.order
model = ARIMA(df['volume'], order=(p, d, q))

# Fit the model
model_fit = model.fit()
print(model_fit.summary())
model_fit.plot_diagnostics(figsize=(10, 8))