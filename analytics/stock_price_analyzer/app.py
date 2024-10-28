import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Função para calcular as médias móveis
def plot_stock_data(stock_data, ticker):
    stock_data['50_MA'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['200_MA'] = stock_data['Close'].rolling(window=200).mean()

    plt.figure(figsize=(10, 5))
    plt.plot(stock_data.index, stock_data['Close'], label=f'{ticker} Close Price', color='blue')
    plt.plot(stock_data.index, stock_data['50_MA'], label='50-Day MA', color='green', linestyle='--')
    plt.plot(stock_data.index, stock_data['200_MA'], label='200-Day MA', color='red', linestyle='--')

    plt.title(f'{ticker} Stock Price with Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Configuração do layout do Streamlit
st.title('Stock Price Analyzer with Moving Averages')

# Inputs do usuário
ticker = st.text_input('Enter Stock Ticker (e.g., AAPL):', 'AAPL','petr4.sa')
start_date = st.date_input('Start Date', pd.to_datetime('2022-01-01'))
end_date = st.date_input('End Date', pd.to_datetime('today'))

# Validação de entrada
if start_date >= end_date:
    st.error('Error: End date must be later than start date.')

# Coleta de dados da API
try:
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    if not stock_data.empty:
        st.write(f"Showing data for {ticker} from {start_date} to {end_date}")
        st.dataframe(stock_data[['Open', 'Close', 'Volume']])
        plot_stock_data(stock_data, ticker)
    else:
        st.error(f'No data found for {ticker}.')

except Exception as e:
    st.error(f'Error fetching data: {e}')

