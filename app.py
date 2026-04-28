import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard TI", layout="wide")

st.title("📊 Dashboard de Performance - Equipa TI")

uploaded_file = st.file_uploader("Carregar Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Filtros
    st.sidebar.header("Filtros")
    tecnicos = st.sidebar.multiselect(
        "Selecionar Técnico",
        df["Tecnico"].unique(),
        default=df["Tecnico"].unique()
    )

    df_filtered = df[df["Tecnico"].isin(tecnicos)]

    # KPIs
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Tickets", int(df_filtered["Tickets"].sum()))
    col2.metric("Tempo Médio", round(df_filtered["Tempo"].mean(), 2))
    col3.metric("SLA Médio", round(df_filtered["SLA"].mean(), 2))
    col4.metric("Score Médio", round(df_filtered["Score_Final"].mean(), 1))

    st.divider()

    # Ranking
    df_sorted = df_filtered.sort_values("Score_Final", ascending=True)

    fig_score = px.bar(
        df_sorted,
        x="Score_Final",
        y="Tecnico",
        orientation="h",
        color="Score_Final",
        color_continuous_scale="RdYlGn",
        title="🏆 Ranking de Performance"
    )

    st.plotly_chart(fig_score, use_container_width=True)

    # Breakdown de métricas
    col1, col2 = st.columns(2)

    fig_tickets = px.bar(df_filtered, x="Tecnico", y="Tickets", title="Tickets por Técnico")
    fig_sla = px.line(df_filtered, x="Tecnico", y="SLA", markers=True, title="SLA por Técnico")

    col1.plotly_chart(fig_tickets, use_container_width=True)
    col2.plotly_chart(fig_sla, use_container_width=True)

    # Radar chart (muito bom para performance individual)
    tecnico_selected = st.selectbox("Selecionar técnico para análise detalhada", df_filtered["Tecnico"])

    df_tecnico = df_filtered[df_filtered["Tecnico"] == tecnico_selected]

    radar_data = pd.DataFrame({
        "Metric": ["Tickets", "Tempo", "SLA", "Reabertos", "Docs"],
        "Score": [
            df_tecnico["Score_Tickets"].values[0],
            df_tecnico["Score_Tempo"].values[0],
            df_tecnico["Score_SLA"].values[0],
            df_tecnico["Score_Reabertos"].values[0],
            df_tecnico["Score_Docs"].values[0],
        ]
    })

    fig_radar = px.line_polar(
        radar_data,
        r="Score",
        theta="Metric",
        line_close=True,
        title=f"📡 Performance Detalhada - {tecnico_selected}"
    )

    st.plotly_chart(fig_radar, use_container_width=True)

    # Tabela
    st.subheader("📋 Dados Completos")
    st.dataframe(df_filtered, use_container_width=True)

else:
    st.info("Carrega um ficheiro Excel para começar.")
