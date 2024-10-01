import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 
- Takes data from mention_data and polarity_data
- Plots it sexily
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 

# Load data
mentions_df = pd.read_csv('./data/Reddit_data/mention_ALL/key_from_ALL.csv')
polarity_df = pd.read_csv('./data/Reddit_data/polarity_data/key_from_csgo_comments.csv')

# Preprocess data
mentions_df['date'] = pd.to_datetime(mentions_df['date'])
polarity_df['date'] = pd.to_datetime(polarity_df['date'])

# Calculate average polarity score for each day
polarity_df['compound'] = polarity_df['compound'].astype(float)
daily_polarity = polarity_df.groupby('date')['compound'].mean().reset_index()

# Merge mentions and daily polarity data
merged_df = pd.merge(mentions_df, daily_polarity, on='date', how='outer').sort_values('date')
merged_df = merged_df.fillna(method='ffill')

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=merged_df['date'], y=merged_df['num_mentions'], name="Mentions", line=dict(color='blue')),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=merged_df['date'], y=merged_df['compound'], name="Average Polarity", line=dict(color='red')),
    secondary_y=True,
)

# Update layout for better readability
fig.update_layout(
    title_text="Mentions and Average Polarity Over Time for 'Key' in CS:GO Comments",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=50, r=50, t=80, b=50),
)

# Update y-axes
fig.update_yaxes(title_text="Number of Mentions", secondary_y=False, gridcolor='lightgrey')
fig.update_yaxes(title_text="Average Polarity (Compound Score)", secondary_y=True, gridcolor='lightgrey')

# Update x-axis
fig.update_xaxes(title_text="Date", gridcolor='lightgrey')

# Show the figure
fig.show()

# Save as HTML
fig.write_html("mentions_and_polarity_chart.html")