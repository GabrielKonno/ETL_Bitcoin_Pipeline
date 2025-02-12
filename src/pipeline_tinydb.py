import requests
import argparse
from datetime import datetime
from tinydb import TinyDB

def extrair_dados_bitcoin(moeda="USD"):
    """Obtém o preço atual do Bitcoin via API da Coinbase"""

    try:
        url = f"https://api.coinbase.com/v2/prices/spot?currency={moeda}" # URL dinâmica
        resposta = requests.get(url, timeout=5) # Define um timeout de 5 segundos
        resposta.raise_for_status() # Lança um erro se a resposta não for 200 (OK)
        dados_json = resposta.json()
        return dados_json
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados: {e}")
        return None

def tratar_dados_bitcoin(dados):
    try:

        preco = float(dados['data']['amount'])
        criptomoeda = str(dados['data']['base']).upper()
        moeda = str(dados['data']['currency']).upper()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        dados_tratados = {
            "preço": preco,
            "criptomoeda": criptomoeda,
            "moeda": moeda,
            "timestamp": timestamp
        }
        return dados_tratados
    
    except (KeyError, ValueError, TypeError) as e:
        print(f"Erro ao processar os dados: {e}")
        return None
    
def salvar_dados_tinydb(dados, db_name="bitcoin_dados.json"):
    """Salva os dados no banco NoSQL TinyDB"""
    db = TinyDB(db_name)
    if dados:
        db.insert(dados)
        print("✅ Dados salvos no TinyDB!")
    else:
        print("⚠️ Nenhum dado válido para salvar.")

    
if __name__ == "__main__":
    # Parser extrair dados bitcoin
    parser = argparse.ArgumentParser(description="Extrai o preço do Bitcoin na moeda desejada.")
    parser.add_argument("--moeda", type=str, default="USD", help="Moeda desejada (USD, EUR, BRL, etc.)")

    args = parser.parse_args()

    dados_json = extrair_dados_bitcoin(args.moeda.upper())

    # Tratar dados
    dados_tratados = tratar_dados_bitcoin(dados_json)

    if dados_tratados:
        print("✅ Dados Extraídos e Tratados com Sucesso!")
        print(dados_tratados)

        # Armazenar dados no TinyDB
        salvar_dados_tinydb(dados_tratados)

# Escolha de moeda é apenas para estudo. Esta api só coleta valor em dólar.
# "python extracao_api.py --moeda BRL" executa o código direto no terminal