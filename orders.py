import json
import requests

def criar_json_formatado(dados):
    # Estrutura a carteira no formato esperado pela API
    carteira_formatada = {
        "walletId": str(dados["walletId"]),  # Converte o ID para string, conforme esperado
        "assets": dados["assets"],
        "active": True  # Adiciona o campo `active` como esperado na API
    }

    # Converte o dicionário para JSON formatado
    json_formatado = json.dumps(carteira_formatada, indent=4)
    return json_formatado

def enviar_dados_api(dados_json, url):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=dados_json, headers=headers)

    if response.status_code == 200 or response.status_code == 201:
        print("Dados enviados com sucesso!")
    else:
        print(f"Falha ao enviar dados: {response.status_code} - {response.text}")

# Dados das carteiras
w1 = [
    {"ticker": "GGBR4", "quantity": 5}
]
w2 = [
    {"ticker": "ITUB4", "quantity": 7}
]

w3 = [
    {"ticker": "VALE3", "quantity": 11}
]

w4 = [
    {"ticker": "ELET3", "quantity": 13}
]

data1 = {"assets": w1, "walletId": 5}
data2 = {"assets": w2, "walletId": 2}
data3 = {"assets": w3, "walletId": 3}
data4 = {"assets": w4, "walletId": 4}

# Criar JSON formatado para cada carteira
json_formatado1 = criar_json_formatado(data1)
json_formatado2 = criar_json_formatado(data2)
json_formatado3 = criar_json_formatado(data3)
json_formatado4 = criar_json_formatado(data4)

# URL da API

url_api_1 = "https://finance-api-silk-five.vercel.app/order"  
url_api_2 = "https://finance-api-silk-five.vercel.app/order" 
url_api_3 = "https://finance-api-silk-five.vercel.app/order"  
url_api_4 = "https://finance-api-silk-five.vercel.app/order" 

# Enviar dados para a API
enviar_dados_api(json_formatado1, url_api)
enviar_dados_api(json_formatado2, url_api)
enviar_dados_api(json_formatado3, url_api)
enviar_dados_api(json_formatado3, url_api)
