import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout='wide')

df = pd.read_csv('./healph_data_mocked.csv')


bins = [18, 30, 40, 50, 60, 70, 80, 90]
labels = ['18-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-90']
df['Faixa_Etaria'] = pd.cut(df['Idade'], bins=bins, labels=labels, right=False)

# Adicionar a opção "Todas as Faixas Etárias" no início da lista
faixas_etarias_opcoes = ['Todas as Faixas Etárias'] + sorted(df['Faixa_Etaria'].unique().tolist())

# Configuração do título do dashboard
st.title("Dashboard de Saúde dos Pacientes")

# Filtro de faixa etária
faixa_etaria = st.selectbox("Selecione a Faixa Etária:", options=faixas_etarias_opcoes)

# Aplicando o filtro de faixa etária
if faixa_etaria == 'Todas as Faixas Etárias':
    df_filtrado = df
else:
    df_filtrado = df[df['Faixa_Etaria'] == faixa_etaria]

# Primeira linha de gráficos (3 colunas)
col1, col2, col3 = st.columns(3)

with col1:
    fig1 = px.scatter(df_filtrado, x='Idade', y='Pressao_Arterial', color='Diabetes',
                      title="Idade vs Pressão Arterial (Colorido por Diabetes)",
                      labels={'Pressao_Arterial': 'Pressão Arterial', 'Idade': 'Idade'},
                      hover_data=['Genero'],
                      color_discrete_map={'Sim': 'red', 'Não': 'blue'})
    st.plotly_chart(fig1)

with col2:
    fig2 = px.histogram(df_filtrado, x='IMC', color='Genero', barmode='overlay',
                        title="Distribuição de IMC por Gênero",
                        labels={'IMC': 'Índice de Massa Corporal (IMC)', 'Genero': 'Gênero'})
    st.plotly_chart(fig2)

with col3:
    fig3 = px.histogram(df_filtrado, x='Faixa_Etaria', color='Fumante', barmode='group',
                        title="Fumantes por Faixa Etária",
                        labels={'Faixa_Etaria': 'Faixa Etária', 'Fumante': 'Fumante'})
    st.plotly_chart(fig3)

# Segunda linha de gráficos (3 colunas)
col4, col5, col6 = st.columns(3)

with col4:
    fig4 = px.box(df_filtrado, x='Diabetes', y='Nivel_Colesterol', color='Diabetes',
                  title="Nível de Colesterol por Uso de Medicação",
                  labels={'Nivel_Colesterol': 'Nível de Colesterol', 'Medicacao': 'Uso de Medicação'},
                  color_discrete_map={'Sim': 'red', 'Não': 'blue'})
    st.plotly_chart(fig4)
    
with col5:
    # Gráfico de dispersão para Idade vs Pressão Arterial, colorido por Diabetes
    fig5 = px.scatter(df_filtrado, x='Idade', y='Nivel_Colesterol', color='Fumante',
                      size ='Atividade_Fisica', hover_data='ID_Paciente',
                      title="Idade vs Nivel de Colesterol (Colorido por Fumante e pontos escalados por Atividade física)",
                      labels={'Nivel_Colesterol': 'Nivel de Colesterol', 'Idade': 'Idade'},
                      color_discrete_map={'Sim': 'red', 'Não': 'blue'})
                      #hover_data=['Genero'])
    st.plotly_chart(fig5)