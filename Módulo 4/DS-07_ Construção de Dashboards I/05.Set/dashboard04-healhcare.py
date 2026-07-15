import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

data = pd.read_csv('healthcare_dataset_pt.csv')

data = data.drop_duplicates()

#ajustando as datas no dataframe
data['Data de Admissão'] = pd.to_datetime(data['Data de Admissão'])
data['Data de Alta'] = pd.to_datetime(data['Data de Alta'])
data['Duração da Estadia'] = (data['Data de Alta'] - data['Data de Admissão']).dt.days

# Calculando estatísticas descritivas da base dados
data['Duração da Estadia'] = (data['Data de Alta'] - data['Data de Admissão']).dt.days
idade_media = data['Idade'].mean().round(2)
genero_frequente = data['Gênero'].mode()[0]
tipo_sanguineo_frequente = data['Tipo Sanguíneo'].mode()[0]
seguro_frequente = data['Provedor de Seguro'].mode()[0]
hospital_frequente = data['Hospital'].mode()[0]
condicao_medica_frequente = data['Condição Médica'].mode()[0]
valor_fatura_medio = data['Valor da Fatura'].mean().round(2)
tipo_admissao_frequente = data['Tipo de Admissão'].mode()[0]
duracao_media_estadia = data['Duração da Estadia'].mean().round(2)

# Layout da página
st.title(":blue[Dashboard de Dados Hospitalares]")
#st.title("_Streamlit_ is :blue[cool] :sunglasses:")

st.subheader("Estatísticas Descritivas dos Pacientes", divider=True)

# Organizando as estatísticas descritivas em colunas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Idade Média dos Pacientes", f"{idade_media} anos")
    st.metric("Gênero Mais Frequente", genero_frequente)
    st.metric("Tipo Sanguíneo Mais Comum", tipo_sanguineo_frequente)

with col2:
    st.metric("Provedor de Seguro Mais Frequente", seguro_frequente)
    st.metric("Hospital Mais Visitado", hospital_frequente)
    st.metric("Condição Médica Frequente", condicao_medica_frequente)

with col3:
    st.metric("Valor Médio de Faturamento", f"R$ {valor_fatura_medio}")
    st.metric("Tipo de Admissão Mais Frequente", tipo_admissao_frequente)
    st.metric("Duração Média da Estadia", f"{duracao_media_estadia} dias")

#mostrando gráficos de análises unilaterais
st.subheader("Análise Visual", divider=True)
col1, col2 = st.columns(2)

with col1:
    gender_counts = data['Gênero'].value_counts()
    labels = gender_counts.index.tolist()
    values = gender_counts.values.tolist()

    colors = ['#1f77b4', '#ff7f0e']

    fig1 = go.Figure(data=[go.Pie(
    labels=labels,
    values=values
    )])

    fig1.update_traces(
        hoverinfo='label+percent',
        textinfo='value',
        textfont_size=20,
        marker=dict(
            colors=colors,
            line=dict(color='#000000', width=2)
        )
    )

    fig1.update_layout(
        title='Distribuição de Gênero',
        autosize=False,
        width=600,
        height=400
    )
    st.plotly_chart(fig1)
    
with col2:
    fig2 = px.histogram(data, x='Condição Médica', color='Tipo de Admissão',
                   color_discrete_sequence=px.colors.qualitative.Plotly,
                   title='Tipo de Admissão por Condição Médica',
                   labels={'Condição Médica': 'Condição Médica', 'Tipo de Admissão': 'Tipo de Admissão'},
                   barmode='group')

    fig2.update_layout(
        xaxis_title='Condição Médica',
        yaxis_title='Contagem',
        width=800,
        height=400
    )
    
    st.plotly_chart(fig2)
    
col1, col2 = st.columns(2)

with col1:
    fig3 = px.box(data, x='Provedor de Seguro', y='Valor da Fatura',
             color='Provedor de Seguro',
             color_discrete_sequence=px.colors.qualitative.Plotly,
             title='Valor da Fatura por Provedor de Seguro')

    fig3.update_layout(
        xaxis_title='Provedor de Seguro',
        yaxis_title='Valor da Fatura',
        width=800,
        height=400
    )

    st.plotly_chart(fig3)
    
with col2:
    hospital_counts = data['Hospital'].value_counts()

    top_10_hospitais = hospital_counts.head(10)

    fig4 = px.bar(top_10_hospitais,
                x=top_10_hospitais.values,
                y=top_10_hospitais.index,
                title='Top 10 Hospitais por Taxa de Admissão',
                labels={'x': 'Número de Admissões', 'y': 'Hospital'},
                orientation='h',
                color=top_10_hospitais.index,
                color_discrete_sequence=px.colors.qualitative.Plotly)

    fig4.update_layout(
        xaxis_title='Número de Admissões',
        yaxis_title='Hospital',
        width=800,
        height=400
    )

    st.plotly_chart(fig4)
    

# Exibindo filtro
st.subheader("Filtragem por Ano", divider=True)

data['Dia de Admissão'] = data['Data de Admissão'].dt.day
data['Mês de Admissão'] = data['Data de Admissão'].dt.month
data['Ano de Admissão'] = data['Data de Admissão'].dt.year

total_revenue_by_hospital = data.groupby('Hospital')['Valor da Fatura'].sum()
top_10_hospitais = total_revenue_by_hospital.nlargest(10).index
dados_filtrados = data[data['Hospital'].isin(top_10_hospitais)]

faturamento_por_ano_e_hospital = dados_filtrados.groupby(['Ano de Admissão', 'Hospital'])['Valor da Fatura'].sum().reset_index()
tabela_pivo = faturamento_por_ano_e_hospital.pivot(index='Ano de Admissão', columns='Hospital', values='Valor da Fatura')

anos_disponiveis = faturamento_por_ano_e_hospital['Ano de Admissão'].unique()
ano_selecionado = st.selectbox("Selecione o Ano", anos_disponiveis)

# Filtrando os dados com base no ano selecionado
faturamento_por_ano = faturamento_por_ano_e_hospital[faturamento_por_ano_e_hospital['Ano de Admissão'] == ano_selecionado]

# Criando o gráfico de pizza atualizado
fig_customized = px.pie(faturamento_por_ano,
             names='Hospital',
             values='Valor da Fatura',
             title=f'Distribuição de Faturamento por Hospital para {ano_selecionado}',
             color_discrete_sequence=px.colors.qualitative.Plotly)

fig_customized.update_layout(
    width=800,
    height=600,
    legend_title='Hospital',
    showlegend=True,
)

st.plotly_chart(fig_customized)