import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

df = pd.read_csv('./healph_data_mocked.csv')

st.title("Dashboard de Saúde dos Pacientes")

# Gráfico de dispersão para Idade vs Pressão Arterial, colorido por Diabetes
fig1 = px.scatter(df, x='Idade', y='Pressao_Arterial', color='Diabetes',
                  title="Idade vs Pressão Arterial (Colorido por Diabetes)",
                  labels={'Pressao_Arterial': 'Pressão Arterial', 'Idade': 'Idade'},
                  hover_data=['Genero'],
                  color_discrete_map={'Sim': 'red', 'Não': 'blue'})

st.plotly_chart(fig1)

# Gráfico de distribuição para o IMC, segmentado por Gênero
fig2 = px.histogram(df, x='IMC', color='Genero', barmode='overlay',
                    title="Distribuição de IMC por Gênero",
                    labels={'IMC': 'Índice de Massa Corporal (IMC)', 'Genero': 'Gênero'})

st.plotly_chart(fig2)


bins = [18, 30, 40, 50, 60, 70, 80, 90]
labels = ['18-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-90']
df['Faixa_Etaria'] = pd.cut(df['Idade'], bins=bins, labels=labels, right=False)

fig3 = px.histogram(df, x='Faixa_Etaria', color='Fumante', barmode='group',
                    title="Fumantes por Faixa Etária",
                    labels={'Faixa_Etaria': 'Faixa Etária', 'Fumante': 'Fumante'},
                    color_discrete_map={'Sim': 'red', 'Não': 'blue'})

st.plotly_chart(fig3)

# Gráfico de caixas (box plot) para Nível de Colesterol por uso de Medicação
fig4 = px.box(df, x='Diabetes', y='Nivel_Colesterol', color='Diabetes',
              title="Nível de Colesterol - Diabetes",
              labels={'Nivel_Colesterol': 'Nível de Colesterol', 'Diabetes': 'Diabetes'},
              color_discrete_map={'Sim': 'red', 'Não': 'blue'})

st.plotly_chart(fig4)

# Gráfico de dispersão 3D para Pressão Arterial, IMC, e Nível de Atividade Física
fig5 = px.scatter_3d(df, x='Pressao_Arterial', y='IMC', z='Atividade_Fisica', color='Genero',
                     title="Relação entre Pressão Arterial, IMC e Atividade Física",
                     labels={'Pressao_Arterial': 'Pressão Arterial', 'IMC': 'Índice de Massa Corporal', 'Atividade_Fisica': 'Atividade Física (horas/semana)'})

st.plotly_chart(fig5)