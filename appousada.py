# analise_dados_pousada_fast.py
# -*- coding: utf-8 -*-

import streamlit as st

# ==============================
# CONFIGURAÇÕES INICIAIS
# ==============================
st.set_page_config(page_title="Análise de Dados - Pousada", layout="wide")
st.title("📊 Análise de Dados da Pousada")

# ==============================
# UPLOADER DE ARQUIVO
# ==============================
uploaded_file = st.file_uploader("📂 Envie o arquivo de reservas (Excel)", type=["xlsx"])

if uploaded_file is not None:
    # ==============================
    # IMPORTAR BIBLIOTECAS PESADAS SÓ QUANDO NECESSÁRIO
    # ==============================
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    # ==============================
    # CARREGAR DADOS
    # ==============================
    @st.cache_data
    def carregar_dados(file):
        df = pd.read_excel(file)
        df['MÊS'] = df['Check-in'].dt.month
        df['ANO'] = df['Check-in'].dt.year
        return df

    Relatorio = carregar_dados(uploaded_file)

    st.subheader("📋 Pré-visualização dos Dados")
    st.write(Relatorio.head())

    # ==============================
    # ANÁLISES DESCRITIVAS
    # ==============================
    st.subheader("💰 Receita Total")
    total_de_receitas = Relatorio['Valor'].sum()
    st.metric(label="Receita Total", value=f"R$ {total_de_receitas:,.2f}")

    # Receita por mês e ano
    Receitas_por_mes_e_ano = Relatorio.groupby(['MÊS', 'ANO'])['Valor'].sum().unstack()

    st.subheader("📈 Receita Bruta por Mês e Ano")
    st.line_chart(Receitas_por_mes_e_ano)

    # Diárias por mês e ano
    diarias_por_mes_e_ano = Relatorio.groupby(['MÊS', 'ANO'])['Quantidade diarias '].sum().unstack()
    st.subheader("📅 Diárias por Mês e Ano")
    st.line_chart(diarias_por_mes_e_ano)

    # Receita por tipo de quarto
    st.subheader("🏨 Receita por Tipo de Quarto")
    Receitas_por_acomodacao = Relatorio.groupby('Tipo de quarto')['Valor'].sum().sort_values(ascending=False)
    st.bar_chart(Receitas_por_acomodacao)

    # ==============================
    # ANÁLISE DIAGNÓSTICA
    # ==============================
    st.subheader("📊 Análise Diagnóstica")

    # Boxplots usando Matplotlib/Seaborn
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(x=Relatorio['Valor'], ax=ax)
    ax.set_title('Boxplot - Receita Bruta')
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(x=Relatorio['Quantidade diarias '], ax=ax)
    ax.set_title('Boxplot - Quantidade de Diárias')
    st.pyplot(fig)

    # Scatter com regressão
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(x='Quantidade diarias ', y='Valor', data=Relatorio,
                ci=None, scatter_kws={'color':'blue'}, line_kws={'color':'red'}, ax=ax)
    ax.set_title('Correlação entre Diárias e Receita Bruta')
    st.pyplot(fig)

else:
    st.warning("👆 Por favor, envie o arquivo **BD_Reservas.xlsx** para começar a análise.")
    st.stop()
