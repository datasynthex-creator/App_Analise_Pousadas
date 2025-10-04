# analise_dados_pousada.py
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# ==============================
# CONFIGURAÇÕES INICIAIS
# ==============================
st.set_page_config(page_title="Análise de Dados - Pousada", layout="wide")

st.title("📊 Análise de Dados da Pousada")

# ==============================
# IMPORTAR BASE DE DADOS
# ==============================
uploaded_file = st.file_uploader("📂 Envie o arquivo de reservas (Excel)", type=["xlsx"])

if uploaded_file is not None:
    Relatorio = pd.read_excel(uploaded_file)

    st.subheader("📋 Pré-visualização dos Dados")
    st.write(Relatorio.head())

    # Criando colunas de Mês e Ano
    Relatorio['MÊS'] = Relatorio['Check-in'].dt.month
    Relatorio['ANO'] = Relatorio['Check-in'].dt.year

    # ==============================
    # ANÁLISES DESCRITIVAS
    # ==============================
    st.subheader("💰 Receita Total")
    total_de_receitas = Relatorio['Valor'].sum()
    st.metric(label="Receita Total", value=f"R$ {total_de_receitas:,.2f}")

    # Receita por mês e ano
    Receitas_por_mes_e_ano = Relatorio.groupby(['MÊS', 'ANO'])['Valor'].sum().unstack()

    fig, ax = plt.subplots(figsize=(8, 4))
    Receitas_por_mes_e_ano.plot(kind='line', ax=ax, marker='o')
    ax.set_title('Receita Bruta por Mês e Ano')
    ax.set_xlabel('Mês')
    ax.set_ylabel('Receita Bruta')
    ax.set_xticks(range(1, 13))
    ax.legend(title='Ano')
    ax.grid(True)
    st.pyplot(fig)

    # ==============================
    # DIÁRIAS POR MÊS E ANO
    # ==============================
    st.subheader("📅 Diárias por Mês e Ano")
    diarias_por_mes_e_ano = Relatorio.groupby(['MÊS', 'ANO'])['Quantidade diarias '].sum().unstack()

    fig, ax = plt.subplots(figsize=(8, 4))
    diarias_por_mes_e_ano.plot(kind='line', ax=ax, marker='o')
    ax.set_title('Diárias por Mês e Ano')
    ax.set_xlabel('Mês')
    ax.set_ylabel('Quantidade de Diárias')
    ax.set_xticks(range(1, 13))
    ax.legend(title='Ano')
    ax.grid(True)
    st.pyplot(fig)

    # ==============================
    # RECEITA POR ACOMODAÇÃO
    # ==============================
    st.subheader("🏨 Receita por Tipo de Quarto")
    Receitas_por_acomodacao = Relatorio.groupby('Tipo de quarto')['Valor'].sum().sort_values(ascending=False)

    st.bar_chart(Receitas_por_acomodacao)

    # ==============================
    # ANÁLISE DIAGNÓSTICA
    # ==============================
    st.subheader("📊 Análise Diagnóstica")

    # Boxplot Receita
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(x=Relatorio['Valor'], ax=ax)
    ax.set_title('Boxplot - Receita Bruta')
    st.pyplot(fig)

    # Boxplot Diárias
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(x=Relatorio['Quantidade diarias '], ax=ax)
    ax.set_title('Boxplot - Quantidade de Diárias')
    st.pyplot(fig)


    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(x='Quantidade diarias ', y='Valor', data=Relatorio,
                ci=None, scatter_kws={'color':'blue'}, line_kws={'color':'red'}, ax=ax)
    ax.set_title('Correlação entre Diárias e Receita Bruta')
    st.pyplot(fig)

else:

    st.warning("👆 Por favor, envie o arquivo **BD_Reservas.xlsx** para começar a análise.")
    st.stop()  # garante que nada abaixo seja executado antes do upload
