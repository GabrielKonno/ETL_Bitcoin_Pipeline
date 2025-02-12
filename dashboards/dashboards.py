import os
import pandas as pd
import streamlit as st
import plotly.express as px
import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus # para adequar a senha ao UTC-8

# Carrega o .env
load_dotenv()

# Config Padrão Banco de Dados
# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
# POSTGRES_DB = os.getenv("POSTGRES_DB")

# DATABASE_URL = (
    # f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    # f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
# )

# Config Adaptada Banco de Dados PostgresSQL
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

# Criar conexão com o banco
engine = create_engine(DATABASE_URL)

# ============================== #
#      Layout do Dashboard
# ============================== #
st.set_page_config(
    page_title="📊 Dashboard Bitcoin",
    page_icon="📈",
    layout="wide"
)

st.title("📊 Análise do Preço do Bitcoin")

# Função para Carregar os Dados
@st.cache_data(ttl=600)
def carregar_dados():
    """Busca os dados do PostgreSQL"""
    query = "SELECT * FROM bitcoin_precos ORDER BY timestamp DESC;"
    df = pd.read_sql(query, con=engine)
    df["timestamp"] = pd.to_datetime(df["timestamp"])  # Converter para datetime
    return df

df = carregar_dados()

# ============================== #
#          Sidebar - Filtros
# ============================== #
st.sidebar.header("Filtros 🔍")

# Filtro interativo de Timestamp utilizando slider (data e hora)
min_timestamp = df["timestamp"].min().to_pydatetime()
max_timestamp = df["timestamp"].max().to_pydatetime()

timestamp_selecionado = st.sidebar.slider(
    "Selecione o intervalo de tempo",
    min_value=min_timestamp,
    max_value=max_timestamp,
    value=(min_timestamp, max_timestamp),
    format="YYYY-MM-DD HH:mm"
)
# Filtrar os dados com base no timestamp selecionado
df_filtrado = df[(df["timestamp"] >= timestamp_selecionado[0]) & (df["timestamp"] <= timestamp_selecionado[1])]
df_filtrado = df_filtrado.sort_values("timestamp")

# Opção para selecionar o tipo de visualização do gráfico
tipo_visualizacao = st.sidebar.radio(
    "Tipo de Visualização",
    ("Preço Absoluto", "Variação Percentual")
)

# Slider para definir a janela da Média Móvel (número de períodos)
window_size = st.sidebar.slider("Janela da Média Móvel (número de períodos)", min_value=1, max_value=30, value=7)

# ============================== #
#          Criação dos Gráficos
# ============================== #
if tipo_visualizacao == "Preço Absoluto":
    # Gráfico de Preço Absoluto
    st.subheader("📈 Evolução do Preço do Bitcoin")
    fig = px.line(
        df_filtrado,
        x="timestamp",
        y="valor",
        title="Evolução do Preço do Bitcoin",
        labels={"valor": "Preço (USD)", "timestamp": "Data"},
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Cálculo e Gráfico da Média Móvel para o preço
    df_filtrado["Média Móvel"] = df_filtrado["valor"].rolling(window=window_size).mean()
    st.subheader(f"📊 Preço vs Média Móvel de {window_size} Períodos")
    fig2 = px.line(
        df_filtrado,
        x="timestamp",
        y=["valor", "Média Móvel"],
        title=f"Preço do Bitcoin vs Média Móvel de {window_size} Períodos",
        labels={"value": "Preço (USD)", "timestamp": "Data"},
        template="plotly_dark"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Estatísticas Resumidas (Preço Absoluto)
    st.sidebar.subheader("📊 Estatísticas (Preço Absoluto)")
    st.sidebar.metric("Preço Mínimo", f"$ {df_filtrado['valor'].min():,.2f}")
    st.sidebar.metric("Preço Máximo", f"$ {df_filtrado['valor'].max():,.2f}")
    st.sidebar.metric("Preço Médio", f"$ {df_filtrado['valor'].mean():,.2f}")
    
else:
    # Cálculo da Variação Percentual em relação ao primeiro valor do período filtrado
    df_filtrado["Variação (%)"] = df_filtrado["valor"] / df_filtrado["valor"].iloc[0] * 100
    # Cálculo da Média Móvel da Variação Percentual
    df_filtrado["Média Móvel (%)"] = df_filtrado["Variação (%)"].rolling(window=window_size).mean()
    
    # Gráfico da Variação Percentual
    st.subheader("📈 Variação Percentual do Preço do Bitcoin")
    fig = px.line(
        df_filtrado,
        x="timestamp",
        y="Variação (%)",
        title="Variação Percentual do Preço do Bitcoin",
        labels={"Variação (%)": "Variação (%)", "timestamp": "Data"},
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico da Média Móvel da Variação Percentual
    st.subheader(f"📊 Variação Percentual vs Média Móvel de {window_size} Períodos")
    fig2 = px.line(
        df_filtrado,
        x="timestamp",
        y=["Variação (%)", "Média Móvel (%)"],
        title=f"Variação Percentual do Preço do Bitcoin vs Média Móvel de {window_size} Períodos",
        labels={"value": "Variação (%)", "timestamp": "Data"},
        template="plotly_dark"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Estatísticas Resumidas (Variação Percentual)
    st.sidebar.subheader("📊 Estatísticas (Variação Percentual)")
    st.sidebar.metric("Variação Mínima (%)", f"{df_filtrado['Variação (%)'].min():,.2f}%")
    st.sidebar.metric("Variação Máxima (%)", f"{df_filtrado['Variação (%)'].max():,.2f}%")
    st.sidebar.metric("Variação Média (%)", f"{df_filtrado['Variação (%)'].mean():,.2f}%")

# ============================== #
#         Exibição dos Dados
# ============================== #
st.subheader("📋 Tabela de Dados")
st.dataframe(df_filtrado)

# Rodapé
st.markdown("---")
st.text("Criado por Gabriel Konno Carrozza 🚀")