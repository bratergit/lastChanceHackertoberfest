import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

# Função para carregar os dados da ação
def carregar_dados(acao, periodo):
    df = yf.download(acao, period=periodo, interval="1m")
    return df

# Função para plotar o gráfico
def plotar_grafico(df, intervalo):
    st.write(f"Gráfico para o intervalo de {intervalo}")
    fig, ax = plt.subplots()
    ax.plot(df['Close'], label="Preço de Fechamento")
    ax.set_xlabel('Data')
    ax.set_ylabel('Preço (R$)')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Função principal do Streamlit
def main():
    st.title('Análise de Ativos - Ações Brasileiras')
    
    acao = st.text_input('Digite o código da ação (ex: PETR4.SA)', 'PETR4.SA')
    
    # Definindo o intervalo do gráfico (15m, 30m, etc.)
    intervalo_input = st.text_input('Digite o intervalo desejado (15m, 30m, 1d, 30d):', '15m')

    # Convertendo o input para o formato correto do Yahoo Finance
    periodo = '1d'
    if intervalo_input.endswith('m'):
        minutos = int(intervalo_input[:-1])
        periodo = f'{minutos//60}d' if minutos >= 60 else '1d'
    elif intervalo_input.endswith('d'):
        periodo = intervalo_input

    # Carregando os dados
    df = carregar_dados(acao, periodo)

    # Exibindo o gráfico
    plotar_grafico(df, intervalo_input)

if __name__ == "__main__":
    main()

