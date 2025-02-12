# 📊 Projeto de Monitoramento do Preço do Bitcoin

## 📌 Descrição
Este projeto foi feito com objetivo de estudo na área de coleta, processamento, armazenamento e visualização de dados sobre o preço do Bitcoin em tempo real.
A solução combina extração de dados via API (ou Web Scraping, realizado apenas para estudo), armazenamento em banco de dados SQL (e NoSQL - apenas para estudo), e visualização interativa com Streamlit.

## 🛠 Tecnologias Utilizadas
- **Linguagem:** Python 3.12
- **Coleta de Dados:** Requests, Selenium
- **Banco de Dados:** PostgreSQL, TinyDB
- **ORM:** SQLAlchemy
- **Dashboard:** Streamlit, Plotly

## 📂 Estrutura do Repositório
```plaintext
/{projeto_bitcoin}
│── README.md
│── dasboards/
│   │── .env       
│   │── dashboards.py  # Dashboard interativo com Streamlit
│── src/
│   │── pipeline_tinydb.py  # Armazena os dados no TinyDB
│   │── pipeline_postgres.py   # Pipeline ETL para PostgreSQL
│── testes/
│   │── extracao_api.py     # Coleta de dados via API Coinbase
│   │── extracao_selenium.py   # Coleta via Web Scraping (InfoMoney)
│── requirements.txt  # Dependências do projeto
│── LICENSE
```

## Como Executar o Projeto
### 1️⃣ Criar o Ambiente Virtual
```bash
conda create -n cripto_etl python=3.12
conda activate cripto_etl
pip install -r requirements.txt
```
### 2️⃣ Configurar Banco de Dados
Crie um arquivo `.env` na raiz do projeto com as credenciais do PostgreSQL:
```plaintext
POSTGRES_USER=postgres
POSTGRES_PASSWORD=xxxxxx
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=bitcoin_db
```

### 3️⃣ Rodar a Coleta de Dados e Armazenar os Dados

- Para executar o código, 
- **TinyDB (NoSQL leve)**
```bash
python src/pipeline_tinydb.py --moeda USD
```
- **PostgreSQL (Banco Relacional)**
```bash
python src/pipeline_postgres.py --moeda USD
```

### 4️⃣ Foram feitos dois códigos de teste para aprendizado e comparação entre API e Web Scraping:
- Para coletar via API:
```bash
python src/extracao_api.py --moeda USD
```
- Para coletar via Web Scraping:
```bash
python src/extracao_selenium.py
```

### 5️⃣ Executar o Dashboard
```bash
streamlit run src/dashboards.py
```
Acesse no navegador: [http://localhost:8501](http://localhost:8501)

## 📊 Resultados do Projeto
- Coleta automática de 15 em 15 segundos do preço do Bitcoin.
- Evolução do preço do Bitcoin ao longo do tempo.
- Comparativo entre método de extração via API e Web Scraping.
- Médias móveis e variações percentuais do preço.
- Análise interativa via dashboard Streamlit.

## Aprendizados 

- Entendimento da biblioteca Logfire, apesar de não ter utilizado no projeto.
- Aprofundamento no uso de Streamlit, coleta de dados via APIs e Web Scraping.
- Pipeline para tratamento simples após coleta e armazenamento utilizando PostgreSQL e TinyDB.

## 📢 Contato
- Autor: Gabriel Konno Carrozza
- LinkedIn: [linkedin.com/in/gabrielkonno](https://www.linkedin.com/in/gabrielkonno)
- GitHub: [github.com/gabrielkonno](https://github.com/gabrielkonno)

