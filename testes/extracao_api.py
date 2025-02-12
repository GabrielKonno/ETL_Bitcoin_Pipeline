import requests
import argparse
from datetime import datetime

def extrair_dados_bitcoin(moeda="USD"):
    """Obtém o preço atual do Bitcoin via API da Coinbase"""

    try:
        url = f"https://api.coinbase.com/v2/prices/spot?currency={moeda}" # URL dinâmica
        resposta = requests.get(url, timeout=5) # Define um timeout de 5 segundos
        resposta.raise_for_status() # Lança um erro se a resposta não for 200 (OK)
        dados = resposta.json()

        preco = float(dados['data']['amount'])
        criptomoeda = dados['data']['base']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "preço": preco,
            "criptomoeda": criptomoeda,
            "moeda": moeda,
            "timestamp": timestamp
        }
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados: {resposta.status_code}")
        return None
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrai o preço do Bitcoin na moeda desejada.")
    parser.add_argument("--moeda", type=str, default="USD", help="Moeda desejada (USD, EUR, BRL, etc.)")

    args = parser.parse_args()

    dados = extrair_dados_bitcoin(args.moeda.upper())

    if dados:
        print("✅ Dados Extraídos com Sucesso!")
        print(dados)

# Escolha de moeda é apenas para estudo. Esta api só coleta valor em dólar.
# "python testes/extracao_api.py --moeda BRL" executa o código direto no terminal