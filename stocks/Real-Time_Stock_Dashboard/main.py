import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import yfinance as yf
from datetime import datetime, timedelta

# Initialize the Dash app with Bootstrap stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Real-Time Stock Market Dashboard"), className="mb-2")
    ]),
    dbc.Row([
        dbc.Col(dbc.Input(id='stock-ticker', type='text', placeholder='Enter stock ticker', value='AAPL'), width=3),
        dbc.Col(dcc.Dropdown(
            id='timeframe',
            options=[
                {'label': '1 Day', 'value': '1d'},
                {'label': '1 Week', 'value': '1wk'},
                {'label': '1 Month', 'value': '1mo'},
                {'label': '1 Year', 'value': '1y'},  # Added 1 Year option
            ],
            value='1d'
        ), width=3)
    ], className="mb-2"),
    dbc.Row([
        dbc.Col(dcc.Graph(id='stock-graph'), width=12),
        dbc.Col(dcc.Markdown(id='error-message', style={'color': 'red'}), width=12)  # Added Markdown for error message
    ])
])


# Define the callback to update the graph based on user input
@app.callback(
    [Output('stock-graph', 'figure'),
     Output('error-message', 'children')],
    [Input('stock-ticker', 'value'),
     Input('timeframe', 'value')]
)
def update_graph(ticker, timeframe):
    if not ticker:
        print("No ticker provided")
        return go.Figure(), "Please enter a stock ticker."

    # Determine the start and end dates based on the selected timeframe
    end_date = datetime.now()
    if timeframe == '1d':
        start_date = end_date - timedelta(days=1)
        interval = '1m'
    elif timeframe == '1wk':
        start_date = end_date - timedelta(weeks=1)
        interval = '1h'
    elif timeframe == '1mo':
        start_date = end_date - timedelta(days=30)
        interval = '1d'
    elif timeframe == '1y':  # Handle 1 Year timeframe
        start_date = end_date - timedelta(days=365)
        interval = '1d'
    else:
        start_date = end_date - timedelta(days=30)
        interval = '1d'

    print(f"Fetching data for ticker: {ticker}, timeframe: {timeframe}, interval: {interval}")
    df = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    print(f"Data fetched:\n{df.head()}")

    # Flatten multi-index columns and remove ticker symbol
    df.columns = [col[0] for col in df.columns]
    print(f"Columns after renaming: {df.columns}")

    if df.empty or 'Close' not in df.columns:
        print("DataFrame is empty or 'Close' column not found")
        return go.Figure(), f"Symbol '{ticker}' does not exist or no data available."

    # Create the figure with the stock price data
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close'))
    fig.update_layout(title=f'Stock Price for {ticker}', xaxis_title='Time', yaxis_title='Price')

    return fig, ""


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
