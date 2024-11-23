import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

from bokeh.plotting import figure, show
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, Span
from bokeh.io import output_notebook

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Função para baixar o histórico de preços dos últimos 5 anos e formatar o DataFrame
def obter_historico_precos(tickers, benchmark='IBOVESPA', periodo='5y'):
    lista_dfs = []  # Lista para armazenar os DataFrames de cada ticker

    for ticker in tickers:
        ticker_formatado = f"{ticker}.SA"  # Formatar ticker para B3
        print(f"Baixando dados para: {ticker_formatado}")

        # Baixando o histórico de preços
        dados = yf.download(ticker_formatado, period=periodo)

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

# Função para calcular MACD
def calcular_macd(df, preco_coluna, periodo_longo=26, periodo_curto=12, periodo_sinal=9):
    # Calcula a média móvel exponencial curta (EMA12)
    df['EMA_Curta'] = df[preco_coluna].ewm(span=periodo_curto, adjust=False).mean()

    # Calcula a média móvel exponencial longa (EMA26)
    df['EMA_Longa'] = df[preco_coluna].ewm(span=periodo_longo, adjust=False).mean()

    # Calcula a linha MACD (diferença entre a EMA curta e a EMA longa)
    df['macdim'] = df['EMA_Curta'] - df['EMA_Longa']

    # Calcula a linha de sinal (EMA de 9 períodos da linha MACD)
    df['macdis'] = df['macdim'].ewm(span=periodo_sinal, adjust=False).mean()

    # Calcula o histograma (diferença entre a linha MACD e a linha de sinal)
    df['macdh'] = df['macdim'] - df['macdis']

    # Remove as colunas intermediárias usadas para o cálculo (opcional)
    df.drop(['EMA_Curta', 'EMA_Longa'], axis=1, inplace=True)

    return df

# Função para calcular Bandas de Bollinger (atualizada)
def calcular_bollinger(df, preco_coluna, nome_ticker_coluna, periodo=20, num_std=2):
    # Calcula a média móvel e o desvio padrão
    df['bbm'] = df.groupby(nome_ticker_coluna)[preco_coluna].transform(lambda x: x.rolling(window=periodo).mean())
    df['Desvio_Padrao'] = df.groupby(nome_ticker_coluna)[preco_coluna].transform(lambda x: x.rolling(window=periodo).std())

    # Calcula as bandas superior e inferior
    df['bbs'] = df['bbm'] + num_std * df['Desvio_Padrao']
    df['bbi'] = df['bbm'] - num_std * df['Desvio_Padrao']

    # Adiciona a coluna 'bbl' como a banda inferior (igual a 'bbi')
    df['bbl'] = df['bbi']

    # Remove colunas intermediárias usadas no cálculo (opcional)
    df.drop(['Desvio_Padrao'], axis=1, inplace=True)

    return df

# Função para calcular RSI (atualizada)
def calcular_rsi(df, preco_coluna, nome_ticker_coluna, periodo=14):
    # Calcula a variação de preço
    df['Variacao'] = df[preco_coluna].diff()

    # Calcula os ganhos e perdas
    df['Ganho'] = df['Variacao'].clip(lower=0)
    df['Perda'] = -df['Variacao'].clip(upper=0)

    # Calcula a média móvel dos ganhos e perdas
    df['Ganho_Medio'] = df.groupby(nome_ticker_coluna)['Ganho'].transform(lambda x: x.rolling(window=periodo).mean())
    df['Perda_Medio'] = df.groupby(nome_ticker_coluna)['Perda'].transform(lambda x: x.rolling(window=periodo).mean())

    # Calcula o RSI
    df['RS'] = df['Ganho_Medio'] / df['Perda_Medio']
    df['rsi'] = 100 - (100 / (1 + df['RS']))

    # Adiciona as colunas de sobrecompra e sobrevenda
    df['rsicom'] = 70
    df['rsivem'] = 30  # Corrigido para 'rsivem'

    # Adiciona 'scom' e 'sven'
    df['scom'] = 70  # Sobrecompra
    df['sven'] = 30  # Sobrevenda

    # Remove colunas intermediárias usadas para o cálculo (opcional)
    df.drop(['Variacao', 'Ganho', 'Perda', 'Ganho_Medio', 'Perda_Medio', 'RS'], axis=1, inplace=True)

    return df


output_notebook()  # Para visualizar em notebooks


# Função principal
def main(tickers):
    # Obter o histórico de preços dos últimos 5 anos e salvar no DataFrame
    historico_precos = obter_historico_precos(tickers)
    historico_precos = calcular_macd(historico_precos, 'price')
    historico_precos = calcular_bollinger(historico_precos, 'price', 'ticker')
    historico_precos = calcular_rsi(historico_precos, 'price', 'ticker')
    historico_precos = historico_precos.replace(np.nan, 0)
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

# Remover fuso horário da coluna de datas
historico_precos['date'] = pd.to_datetime(historico_precos['date']).dt.tz_localize(None)

# Definir a data limite e filtrar
data_limite = pd.to_datetime('2024-09-15')
historico_precos = historico_precos[historico_precos['date'] > data_limite]

# Preencher as colunas obrigatórias com valores padrão, se necessário
colunas_obrigatorias = [
    "pl", "rsivem", "rsicom", "scom", "sven",
    "bbi", "bbs", "bbm", "bbl", "macdim", "macdis", "macdh", "rsi"
]

for coluna in colunas_obrigatorias:
    if coluna not in historico_precos.columns:
        historico_precos[coluna] = 0  # Adiciona a coluna com valor padrão se não existir
    else:
        historico_precos[coluna] = pd.to_numeric(historico_precos[coluna], errors="coerce").fillna(0)  # Preenche valores nulos com 0

# Garantir que as colunas estão preenchidas corretamente
historico_precos["pl"] = 0
historico_precos["rsivem"] = historico_precos["rsivem"].fillna(0)
historico_precos["rsicom"] = historico_precos["rsicom"].fillna(0)
historico_precos["scom"] = historico_precos["scom"].fillna(0)
historico_precos["sven"] = historico_precos["sven"].fillna(0)
historico_precos["bbl"] = historico_precos["bbl"].fillna(0)

# Verificar se ainda existem valores nulos no DataFrame
nulos = historico_precos.isnull().sum()
if nulos.any():
    print("Colunas com valores nulos:")
    print(nulos[nulos > 0])
    raise ValueError("Existem valores nulos em colunas obrigatórias!")

# Verificar os tipos de dados das colunas
print("Tipos de dados das colunas:")
print(historico_precos.dtypes)

# Exibir uma amostra dos dados tratados
print("Amostra dos dados tratados:")
print(historico_precos.head())

# Connection string fornecida para conectar ao banco de dados
conn_string = "postgresql://finance-api_owner:s6wc1tNPBDJS@ep-red-lab-a4y556ty.us-east-1.aws.neon.tech/finance-api?sslmode=require"

# Função para inserir dados de um DataFrame na tabela Asset (atualizada)
def inserir_dados_asset(df, conn_string):
    # Criar engine de conexão usando a connection string fornecida
    engine = create_engine(conn_string)

    # Conectar ao banco de dados com um contexto de transação que faz commit automaticamente
    with engine.begin() as conn:  # Usando begin para garantir o commit
        # Criar a query de inserção para a tabela Asset
        query = text("""
            INSERT INTO "Asset" (
                "ticker", "assetName", "date", "price", "volume",
                "dailyVariation", "benchmark", "type", "macdim", "macdis",
                "macdh", "bbm", "bbs", "bbi", "bbl", "rsi", "rsicom", "rsivem",
                "scom", "sven", "pl"
            )
            VALUES (
                :ticker, :assetName, :date, :price, :volume,
                :dailyVariation, :benchmark, :type, :macdim, :macdis,
                :macdh, :bbm, :bbs, :bbi, :bbl, :rsi, :rsicom, :rsivem,
                :scom, :sven, :pl
            )
        """)

        # Iterar sobre as linhas do DataFrame e inserir os dados
        for _, row in df.iterrows():
            conn.execute(query, {
                "ticker": row["ticker"],
                "assetName": row["assetName"],
                "date": row["date"],
                "price": row["price"],
                "volume": row["volume"],
                "dailyVariation": row["dailyVariation"],
                "benchmark": row["benchmark"],
                "type": row["type"],
                "macdim": row["macdim"],
                "macdis": row["macdis"],
                "macdh": row["macdh"],
                "bbm": row["bbm"],
                "bbs": row["bbs"],
                "bbi": row["bbi"],
                "bbl": row["bbl"],
                "rsi": row["rsi"],
                "rsicom": row["rsicom"],
                "rsivem": row["rsivem"],
                "scom": row["scom"],
                "sven": row["sven"],
                "pl": row["pl"]
            })
        print("Dados do DataFrame inseridos na tabela Asset.")

# Inserir os dados na tabela Asset
inserir_dados_asset(historico_precos, conn_string)