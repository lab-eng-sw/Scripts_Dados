import json
import requests

def criar_json_formatado(dados):
    # Estrutura a carteira no formato esperado pela API
    carteira_formatada = {
        "assets": dados["assets"],
        "active": True  # Adiciona o campo `active` como esperado na API
    }

    # Converte o dicionário para JSON formatado
    json_formatado = json.dumps(carteira_formatada, indent=4)
    return json_formatado

def enviar_dados_api(dados_json, url):
    headers = {'Content-Type': 'application/json'}
    response = requests.patch(url, data=dados_json, headers=headers)

    if response.status_code == 200 or response.status_code == 201:
        print("Dados enviados com sucesso!")
    else:
        print(f"Falha ao enviar dados: {response.status_code} - {response.text}")

# Dados das carteiras
w1 = [
    {"ticker": "PETR4", "quantity": 30},
    {"ticker": "VALE3", "quantity": 12},
    {"ticker": "ITUB4", "quantity": 25}
]

w2 = [
    {"ticker": "BBDC4", "quantity": 23},
    {"ticker": "ABEV3", "quantity": 52},
    {"ticker": "JBSS3", "quantity": 81}
]

w3 = [
    {"ticker": "GGBR4", "quantity": 27},
    {"ticker": "ITUB4", "quantity": 42},
    {"ticker": "ABEV3", "quantity": 51}
]

w4 = [
    {"ticker": "ITUB4", "quantity": 89},
    {"ticker": "BBDC4", "quantity": 62},
    {"ticker": "GGBR4", "quantity": 54}
]

data1 = {"assets": w1}
data2 = {"assets": w2}
data3 = {"assets": w3}
data4 = {"assets": w4}

# Criar JSON formatado para cada carteira
json_formatado1 = criar_json_formatado(data1)
json_formatado2 = criar_json_formatado(data2)
json_formatado3 = criar_json_formatado(data3)
json_formatado3 = criar_json_formatado(data4)

# URL da API
url_api_1 = "https://finance-api-silk-five.vercel.app/wallet/5"  # Substitua pelo URL real da sua API
url_api_2 = "https://finance-api-silk-five.vercel.app/wallet/2"  # Substitua pelo URL real da sua API
url_api_3 = "https://finance-api-silk-five.vercel.app/wallet/3"  # Substitua pelo URL real da sua API
url_api_4 = "https://finance-api-silk-five.vercel.app/wallet/4"  # Substitua pelo URL real da sua API


# Enviar dados para a API
#enviar_dados_api(json_formatado1, url_api_1)
#enviar_dados_api(json_formatado2, url_api_2)
#enviar_dados_api(json_formatado3, url_api_3)
#enviar_dados_api(json_formatado1, url_api_4)