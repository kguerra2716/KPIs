import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="SaaS KPI Dashboard", layout="wide")

# --- SIMULAÇÃO DE DADOS ---
@st.cache_data
def get_data():
    dates = pd.date_range(start="2023-01-01", end="2023-12-01", freq='MS')
    regions = ['Norte', 'Sul', 'Leste', 'Oeste']
    data = []
    for date in dates:
        for region in regions:
            mrr = np.random.uniform(50000, 100000)
            churn = np.random.uniform(2, 7)
            cac = np.random.uniform(200, 500)
            conv_rate = np.random.uniform(5, 15)
            data.append([date, region, mrr, churn, cac, conv_rate])
    
    return pd.DataFrame(data, columns=['Data', 'Região', 'MRR', 'Churn Rate', 'CAC', 'Taxa de Conversão'])

df = get_data()

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("Filtros")
regiao_filter = st.sidebar.multiselect("Selecione a Região", options=df["Região"].unique(), default=df["Região"].unique())
periodo_filter = st.sidebar.slider("Período", min_value=df["Data"].min().to_pydatetime(), max_value=df["Data"].max().to_pydatetime(), value=(df["Data"].min().to_pydatetime(), df["Data"].max().to_pydatetime()))

df_filtered = df[(df["Região"].isin(regiao_filter)) & (df["Data"] >= periodo_filter[0]) & (df["Data"] <= periodo_filter[1])]

# --- DASHBOARD PRINCIPAL ---
st.title("🚀 SaaS Business Intelligence Dashboard")

# Métricas em Colunas
m1, m2, m3, m4 = st.columns(4)
m1.metric("Receita Recorrente (MRR)", f"R$ {df_filtered['MRR'].sum():,.2f}")
m2.metric("Churn Médio", f"{df_filtered['Churn Rate'].mean():.2f}%", delta="-0.5%", delta_color="inverse")
m3.metric("CAC Médio", f"R$ {df_filtered['CAC'].mean():.2f}")
m4.metric("Conversão", f"{df_filtered['Taxa de Conversão'].mean():.2f}%")

# Gráficos
c1, c2 = st.columns(2)

with c1:
    fig_mrr = px.line(df_filtered, x="Data", y="MRR", color="Região", title="Tendência de MRR por Região")
    st.plotly_chart(fig_mrr, use_container_width=True)

with c2:
    fig_churn = px.bar(df_filtered, x="Região", y="Churn Rate", title="Churn Rate por Região", color="Região")
    st.plotly_chart(fig_churn, use_container_width=True)
