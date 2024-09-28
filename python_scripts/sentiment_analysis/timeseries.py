
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 
- Takes data from mention_data and polarity_data
- Plots it sexily
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 


def load_data(mention_file, polarity_file):
    mentions = pd.read_csv(./data/Reddit_data/mention_data/key_from_csgo_comments.csv)
    polarity = pd.read_csv()
    return mentions, polarity

def process_data(mentions, polarity):
    # Merge the data if necessary
    # For this example, we'll assume the data is already in the correct format
    return mentions, polarity

def create_plot(mentions, polarity):
    # Create subplot with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add mentions trace
    fig.add_trace(
        go.Scatter(x=mentions['date'], y=mentions['num_mentions'], name="Mentions"),
        secondary_y=False,
    )

    # Add polarity trace
    fig.add_trace(
        go.Scatter(x=polarity['created_utc'], y=polarity['compound'], name="Polarity"),
        secondary_y=True,
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="Number of Mentions", secondary_y=False)
    fig.update_yaxes(title_text="Polarity Score", secondary_y=True)

    # Set title
    fig.update_layout(title_text="Item Mentions and Polarity Over Time")

    return fig

def main():
    mention_file = '../../data/Reddit_data/mention_data/key_from_csgo_comments.csv'
    polarity_file = '../../data/Reddit_data/polarity_data/output.csv'

    mentions, polarity = load_data(mention_file, polarity_file)
    mentions, polarity = process_data(mentions, polarity)
    fig = create_plot(mentions, polarity)

    # Save the plot as an interactive HTML file
    fig.write_html("item_mentions_and_polarity.html")

    # Alternatively, show the plot in a browser
    # fig.show()

if __name__ == "__main__":
    main()
