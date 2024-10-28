import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import concurrent.futures
import plotly.graph_objects as go
import streamlit.components.v1 as components

def get_stock_data(ticker, period, interval):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period, interval=interval)
        return ticker, data
    except Exception as e:
        print(f"Erro ao obter dados para {ticker}: {e}")
        return ticker, None

def check_golden_cross(df, short_ma, long_ma):
    if len(df) >= long_ma:
        df[f'SMA{short_ma}'] = df['Close'].rolling(window=short_ma).mean()
        df[f'SMA{long_ma}'] = df['Close'].rolling(window=long_ma).mean()
        
        if len(df[f'SMA{short_ma}'].dropna()) > 0 and len(df[f'SMA{long_ma}'].dropna()) > 0:
            return df[f'SMA{short_ma}'].iloc[-2] < df[f'SMA{long_ma}'].iloc[-2] and \
                   df[f'SMA{short_ma}'].iloc[-1] > df[f'SMA{long_ma}'].iloc[-1]
    return False

def calculate_macd(df, short_period=12, long_period=26, signal_period=9):
    df['EMA12'] = df['Close'].ewm(span=short_period, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=long_period, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()
    df['Hist'] = df['MACD'] - df['Signal']
    
    # Sinal de compra/venda baseado no MACD
    df['MACD_Signal'] = np.where(df['MACD'] > df['Signal'], 'Compra', 'Venda')

    return df

def get_all_stocks():
    bovespa_tickers = [
        "RAIL3.SA", "ABEV3.SA", "AZUL4.SA", "BBAS3.SA", 
        "BBDC4.SA", "BRFS3.SA", "B3SA3.SA", "CIEL3.SA", "CMIG4.SA", 
        "CPLE6.SA", "CSAN3.SA", "CSNA3.SA", "CYRE3.SA", "ELET3.SA", 
        "EMBR3.SA", "EQTL3.SA", "GGBR4.SA", "PRIO3.SA", "HYPE3.SA", 
        "ITSA4.SA", "ITUB4.SA", "JBSS3.SA", "LREN3.SA", "MGLU3.SA", 
        "MRVE3.SA", "MULT3.SA", "NTCO3.SA", "PETR3.SA", "PETR4.SA", 
        "RENT3.SA", "SBSP3.SA", "TIMS3.SA", "TOTS3.SA", "UGPA3.SA", 
        "USIM5.SA", "VALE3.SA", "WEGE3.SA", "RADL3.SA", "BBSE3.SA", 
        "KLBN11.SA", "BPAC11.SA", "AZUL4.SA", "SUZB3.SA", "VBBR3.SA", 
        "HAPV3.SA", "RRRP3.SA", "RDOR3.SA", "ASAI3.SA", "GMAT3.SA"
    ]
    
    return bovespa_tickers

def plot_stock(df, ticker, short_ma, long_ma):
    fig = go.Figure()
    
    # Adiciona o gráfico de candlestick do preço
    fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Preço'))
    
    # Adiciona as médias móveis
    fig.add_trace(go.Scatter(x=df.index, y=df[f'SMA{short_ma}'], name=f'SMA {short_ma}', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df[f'SMA{long_ma}'], name=f'SMA {long_ma}', line=dict(color='red')))
    
    # Adiciona MACD e linha de sinal no eixo secundário
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='green'), yaxis="y2"))
    fig.add_trace(go.Scatter(x=df.index, y=df['Signal'], name='Signal Line', line=dict(color='orange'), yaxis="y2"))
    
    # Ajusta o layout para incluir um eixo y secundário
    fig.update_layout(
        title=f'{ticker} - Análise  e MACD',
        xaxis_rangeslider_visible=False,
        yaxis_title='Preço',
        yaxis2=dict(
            title='MACD',
            overlaying='y',
            side='right',
        )
    )
    
    fig.add_annotation(
        text=f"MACD (12, 26, 9): Sinal é '{df['MACD_Signal'].iloc[-1]}'",
        xref="paper", yref="paper",
        x=0, y=1.1, showarrow=False
    )
    
    return fig

def main():
    # Adiciona o código HTML e JavaScript para o alerta
    alert_script = """
    <script>
        window.onload = function() {
            alert("ATENÇÃO: As informações apresentadas neste site não devem ser consideradas como aconselhamento, recomendação, oferta ou solicitação para comprar ou vender ações, títulos, valores mobiliários ou qualquer outro instrumento financeiro. É importante destacar que investimentos envolvem riscos e é responsabilidade do investidor avaliar cuidadosamente suas opções antes de tomar qualquer decisão de investimento. Os dados fornecidos neste site são apenas para fins informativos, educacionais e não garantem a precisão ou integridade dos dados apresentados. Maiores informações:   https://www.linkedin.com/in/ilha/     ");
        }
    </script>
    """
    
    # Insere o HTML no Streamlit
    components.html(alert_script, height=0)
    
    st.title("Análise e MACD - Ações da Bovespa")
    
    period = st.text_input("Digite o período (exemplo: 1d, 2mo):", value="1d")
    interval = st.selectbox("Escolha o intervalo de tempo:", ["15m", "30m", "60m"])
    short_ma = st.number_input("Média Móvel Curta:", value=50, min_value=1, max_value=100)
    long_ma = st.number_input("Média Móvel Longa:", value=200, min_value=1, max_value=500)
    
    if st.button("Analisar"):
        tickers = get_all_stocks()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(lambda t: get_stock_data(t, period, interval), tickers))
        
        stock_data = {ticker: data for ticker, data in results if data is not None}
        
        golden_cross_stocks = []
        for ticker, df in stock_data.items():
            df = calculate_macd(df)
            if check_golden_cross(df, short_ma, long_ma):
                golden_cross_stocks.append(ticker)
                
        if golden_cross_stocks:
            st.write("Ações dando Sinal:")
            for stock in golden_cross_stocks:
                st.write(stock)
                fig = plot_stock(stock_data[stock], stock, short_ma, long_ma)
                st.plotly_chart(fig)
        else:
            st.write("Nenhuma ação com sinal. ")

if __name__ == "__main__":
    main()

