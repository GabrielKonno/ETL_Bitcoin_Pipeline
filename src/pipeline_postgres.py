import os
import requests
import argparse
import time
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Float, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from urllib.parse import quote_plus # para adequar a senha ao UTC-8

# Carrega o .env
load_dotenv()

# Config Banco de Dados PostgresSQL
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

encoded_password = quote_plus(POSTGRES_PASSWORD) # adequado para senha

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{encoded_password}" # adequado para senha
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}" # adequado para senha
)

# Cria Engine e Sessão
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Definição do modelo da tabela
Base = declarative_base()

class BitcoinPreco(Base):
    __tablename__="bitcoin_precos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float, nullable=False)
    criptomoeda = Column(String(50), nullable=False)
    moeda = Column(String(10), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

def criar_tabela():
    """Cria a tabela no banco de dados, se não existir."""
    Base.metadata.create_all(engine)
    print("Tabela criada/verificada com sucesso!")

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
            "valor": preco,
            "criptomoeda": criptomoeda,
            "moeda": moeda,
            "timestamp": timestamp
        }
        return dados_tratados
    
    except (KeyError, ValueError, TypeError) as e:
        print(f"Erro ao processar os dados: {e}")
        return None
    
def salvar_dados_postgres(dados):
    """Salva os dados no PostgreSQL"""
    session = Session()
    try:
        novo_registro = BitcoinPreco(**dados)
        session.add(novo_registro)
        session.commit()
        print("✅ Dados salvos no PostgreSQL!")
    except Exception as e:
        session.rollback()  # Desfaz a transação em caso de erro
        print(f"❌ Erro ao salvar no PostgreSQL: {e}")
    finally:
        session.close()  # Fecha a conexão corretamente

def executar_pipeline(moeda):
    
    dados_json = extrair_dados_bitcoin(moeda.upper())

    if dados_json:
        # Tratar dados
        dados_tratados = tratar_dados_bitcoin(dados_json)
        if dados_tratados:
            print("✅ Dados Extraídos e Tratados com Sucesso!")
            print("Dados Tratados:", dados_tratados)
            # Armazenar dados no PostgreSQL
            salvar_dados_postgres(dados_tratados)

if __name__ == "__main__":
    # Parser extrair dados bitcoin
    parser = argparse.ArgumentParser(description="Extrai o preço do Bitcoin na moeda desejada.")
    parser.add_argument("--moeda", type=str, default="USD", help="Moeda desejada (USD, EUR, BRL, etc.)")

    args = parser.parse_args()

    # Cria ou verifica a tabela no banco de dados
    criar_tabela()

    print("Começando processo de coleta a cada 15 segundos (CTRL+C para interromper)")
    while True:
        try:
            executar_pipeline(args.moeda)
            time.sleep(15)
        except KeyboardInterrupt:
            print("\nProcesso interrompido pelo usuário. Finalizando...")
            break
        except Exception as e:
            print(f"Erro durante a execução: {e}")
            time.sleep(15)
# Escolha de moeda é apenas para estudo. Esta api só coleta valor em dólar.
# "python extracao_api.py --moeda BRL" executa o código direto no terminal