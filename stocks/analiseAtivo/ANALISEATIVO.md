# Análise de Ativos - Ações Brasileiras

Este projeto permite a análise de ações brasileiras com gráficos de diferentes intervalos de tempo, utilizando o Yahoo Finance como fonte de dados.

## Funcionalidades

- A aplicação gera gráficos baseados nos dados da ação inserida (por exemplo, PETR4.SA).
- O usuário pode digitar intervalos como "15m", "30m", "1d", "30d", e o gráfico será atualizado dinamicamente.
- O gráfico mostra o preço de fechamento da ação para o período escolhido.

## Como Rodar

1. Clone este repositório.
   
   ```bash
   git clone https://github.com/adalbertobrant/analiseativo.git

2. Instale as dependências
	```bash
	pip install -r requirements.txt

3. Rode o projeto
	```bash
	streamlit run analiseAtivo.py

4. Acesse a aplicação no seu navegador em http://localhost:8501

## Dependências

- streamlit: Framework para criação de aplicações web interativas em Python.
- yfinance: Biblioteca para acessar dados financeiros do Yahoo Finance.
- matplotlib: Biblioteca para plotar gráficos.

## Contribuição

Sinta-se à vontade para abrir issues e pull requests para melhorar o projeto.


### Instruções Adicionais:

- Ao rodar o projeto, a aplicação abrirá no navegador e permitirá inserir o código da ação e o intervalo desejado.
- O gráfico será automaticamente atualizado com base no intervalo inserido (como 15m para 15 minutos, 1d para um dia, etc.).

Com isso, a aplicação estará pronta para rodar e oferecer uma interface interativa para análise de ações com diferentes intervalos de tempo.


