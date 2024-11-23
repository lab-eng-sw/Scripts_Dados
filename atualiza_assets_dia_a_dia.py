import yfinance as yf
import pandas as pd

def obter_historico_precos(tickers, benchmark='IBOVESPA'):
    lista_dfs = []  # Lista para armazenar os DataFrames de cada ticker

    for ticker in tickers:
        ticker_formatado = f"{ticker}.SA"  # Formatar ticker para B3
        print(f"Baixando dados para: {ticker_formatado}")

        # Baixando o histórico de preços do último dia
        dados = yf.download(ticker_formatado, period='1d', interval='1d')

        if not dados.empty:
            # Obter a descrição da empresa usando yfinance
            empresa = yf.Ticker(ticker_formatado)
            info_empresa = empresa.info
            area_atuacao = info_empresa.get('sector', 'N/A')  # Extraindo o setor da empresa
            nome_empresa = info_empresa.get('shortName', 'N/A')  # Extraindo o nome da empresa

            # Calcular a variação diária (%)
            dados['dailyVariation'] = dados['Adj Close'].pct_change() * 100

            # Corrigir caso o índice 'dados.index' seja multi-dimensional ou errado
            dados = dados.reset_index()  # Redefinir o índice para garantir que 'Date' seja uma coluna

            # Criar um DataFrame com as colunas necessárias
            df = pd.DataFrame({
                'ticker': [ticker] * len(dados),  # Repetindo o nome do ticker para cada linha
                'assetName': [nome_empresa] * len(dados),  # Repetindo o nome da empresa
                'date': dados['Date'],  # Usando a data da coluna redefinida
                'price': dados['Adj Close'].values.flatten(),  # Garantindo que Adj Close seja 1D
                'volume': dados['Volume'].values.flatten(),  # Garantindo que Volume seja 1D
                'dailyVariation': dados['dailyVariation'].values.flatten(),  # Garantindo que Variação Diária seja 1D
                'benchmark': [benchmark] * len(dados),  # Repetindo o benchmark
                'type': [area_atuacao] * len(dados)  # Repetindo o setor da empresa
            })

            # Adicionar o DataFrame formatado à lista
            lista_dfs.append(df)

    # Concatenar todos os DataFrames da lista em um único DataFrame
    historico_completo = pd.concat(lista_dfs, ignore_index=True)

    return historico_completo

# Função principal
def main(tickers):
    # Obter o histórico de preços dos últimos 5 anos e salvar no DataFrame
    historico_precos = obter_historico_precos(tickers)

    return historico_precos  # Retornar o DataFrame para uso posterior

# Lista de tickers da B3
tickers_b3 = [
    'PETR4',  # Petrobras PN
    'VALE3',  # Vale ON
    'ITUB4',  # Itaú Unibanco PN
    'BBDC4',  # Bradesco PN
    'BBAS3',  # Banco do Brasil ON
    'ABEV3',  # Ambev ON
    'JBSS3',  # JBS ON
    'ELET3',  # Eletrobras ON
    'WEGE3',  # WEG ON
    'GGBR4'   # Gerdau PN
]

# Executar a função principal
historico_precos = main(tickers_b3)