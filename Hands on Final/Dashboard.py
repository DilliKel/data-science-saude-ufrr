# Importação das bibliotecas
import streamlit as st
import pandas as pd
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostRegressor
from st_on_hover_tabs import on_hover_tabs
import matplotlib.pyplot as plt

# Função para atualizar o LabelEncoder
def atualizar_label_encoder(le, novas_classes):
    # Adicionar novas classes ao encoder
    for classe in novas_classes:
        if classe not in le.classes_:
            le.classes_ = np.append(le.classes_, classe)
    return le

# Configurações iniciais
st.set_page_config(layout="wide")

st.header("Dados e Predição IMC Nacional - SISVAN")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

# Barra lateral com navegação
data = pd.read_csv('dataset_IMC_final.csv')
data["ano"] = pd.to_numeric(data["ano"], errors="coerce")
data.dropna(subset=["ano"], inplace=True)
data["ano"] = data["ano"].astype(int)

z_scores = np.abs(stats.zscore(data['imc']))
data = data[z_scores < 3]  # Keep rows where Z-score is less than 3

# Filtrar diretamente no próprio df
mask = data["ano"].between(2008, 2023)

# Calcular o IQR nos dados filtrados
Q1 = data.loc[mask, "imc"].quantile(0.25)
Q3 = data.loc[mask, "imc"].quantile(0.75)
IQR = Q3 - Q1

# Definir limites para detectar outliers
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

# Aplicar as modificações diretamente no df, removendo os outliers
data = data.loc[(~mask) | ((data["imc"] >= limite_inferior) & (data["imc"] <= limite_superior))]

with st.sidebar:
    tabs = on_hover_tabs(tabName=['Inicial', 'Target'], 
                         iconName=['dashboard', 'economy'], default_choice=0)

# Função para ajustar altura
def ajustar_altura(valor):
    return valor / 100 if valor > 10 else valor

data['altura'] = data['altura'].apply(ajustar_altura)

# Limpeza e codificação de variáveis categóricas
mapeamento_escolaridade = {
    "Classe alfabetizada - ca": "Alfabetização",
    "Alfabetização para adultos (mobral, etc)": "Alfabetização",
    "Creche": "Alfabetização",
    "Pré-escola (exceto ca)": "Alfabetização",
    "Ensino fundamental 1ª a 4ª séries": "Fundamental",
    "Ensino fundamental 5ª a 8ª séries": "Fundamental",
    "Ensino fundamental completo": "Fundamental",
    "Ensino fundamental especial": "Fundamental",
    "Ensino médio, médio2º ciclo (científico,técnico e etc)": "Médio",
    "Superior, aperfeiçoamento, especialização, mestrado, doutorado": "Superior"
}

data["escolaridade"] = data["escolaridade"].replace(mapeamento_escolaridade)

# Preparar os dados para o modelo
X = data[['idade', 'sexo', 'peso', 'altura', 'escolaridade', 'raca_cor', 'sigla_uf']]
y = data['imc']

label_encoders = {}
for col in ['sexo', 'raca_cor', 'escolaridade', 'sigla_uf']:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo
ada_model = AdaBoostRegressor(n_estimators=100, random_state=42)
ada_model.fit(X_train, y_train)

# Função para calcular o IMC
def calcular_imc(peso, altura):
    return peso / (altura ** 2)

# Frequência total de mulheres e homens em cada estado
proportion = data.groupby(["sigla_uf_nome", "sexo"]).size().reset_index(name="count")

# Definir faixas etárias com limites claros
bins = [0, 18, 25, 40, 60, float('inf')]  # Faixas etárias
labels = ["0-18", "19-25", "26-40", "41-60", ">60"]

# Atribuir cada participante a uma faixa etária
data["faixa_etaria"] = pd.cut(data["idade"], bins=bins, labels=labels, right=False)

# Calcular o IMC médio por faixa etária
imc_por_faixa = data.groupby("faixa_etaria")["imc"].mean().reset_index()

# Convertendo coluna ano em float e tirando os valores nulos
data["ano"] = pd.to_numeric(data["ano"], errors='coerce')
data.dropna(subset=["ano"], inplace=True)

# Página Inicial
if tabs == 'Inicial':
    st.title("Página Inicial")
    estados = len(data['sigla_uf'].unique())
    contagem_ano = sorted(data["ano"].unique())

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Abrangência dos dados", f"{estados} Estados")
    with col2:
        st.metric("Período de abrangência", f"{contagem_ano[0]} - {contagem_ano[-1]}")
    with col3:
        st.metric("Quantidade de dados", f"{len(data)} linhas")

    col4, col5 = st.columns(2)

    with col5:
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.subheader("🔍 IMC Médio por Faixa Etária")
        st.markdown("Este gráfico mostra como o IMC médio varia entre diferentes faixas etárias. "
                    "Isso ajuda a identificar quais grupos etários estão mais propensos ao sobrepeso ou desnutrição.")

    
   

    with col4:
        fig = px.bar(
            imc_por_faixa,
            x="faixa_etaria",
            y="imc",
            title="Comparação do IMC Médio entre Faixas Etárias",
            labels={"faixa_etaria": "Faixa Etária", "imc": "IMC Médio"},
            text="imc"  # Exibir os valores no topo das barras
        )

        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig.update_layout(
            xaxis_title="Faixa Etária",
            yaxis_title="IMC Médio",
            showlegend=False
        )

        st.plotly_chart(fig)


    col6, col7 = st.columns(2)

    with col6:
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.subheader("📊 Variação do IMC ao Longo dos Anos")
        st.markdown("A seguir, temos um gráfico de caixa que mostra a distribuição do IMC ano a ano, com os valores extremos removidos para facilitar a visualização.")

    with col7:
        # gráfico
        fig = px.box(
            data,
            x="ano",
            y="imc",
            title="Distribuição do IMC por Ano (2008-2012)",
            width=1000,
            height=500,
            color="ano",  # opcional: adiciona cor por ano
        )

        # Exibir no Streamlit
        st.plotly_chart(fig)

    col8, col9 = st.columns(2)
    with col8:
        imc_medio_ano_sexo = data.groupby(["ano", "sexo"])["imc"].mean().reset_index()
        fig = px.line(imc_medio_ano_sexo, x="ano", y="imc", color="sexo",
             title="Tendência do IMC Médio ao Longo dos Anos por Sexo",
             labels={"ano": "Ano", "imc": "IMC Médio", "sexo": "Sexo"})
        st.plotly_chart(fig)

    with col9:
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.subheader("📈 Aumento do IMC de acordo com os anos")
        st.markdown("A figura a seguir mostra uma tendencia de aumento do IMC tanto do sexo masculino quanto para o feminino no decorrer de 10 anos")


# Página Target (Predição de IMC)
elif tabs == 'Target':
    st.title("Predição de IMC")

    st.markdown("Insira suas informações para calcular seu IMC atual e prever como ele pode estar no futuro.")

    idade_atual = st.slider("📅 Qual sua idade atual?", 0, 100, 25)
    anos_futuros = st.slider("⏩ Em quantos anos você deseja prever seu IMC?", 0, 30, 5)
    idade_futura = idade_atual + anos_futuros

    sexo = st.selectbox('👤 Qual o seu sexo?', ['Masculino', 'Feminino'])
    peso = st.number_input("⚖️ Insira seu peso atual (kg):", min_value=30.0, max_value=300.0, step=0.1)
    altura = st.number_input("📏 Insira sua altura (cm):", min_value=100.0, max_value=250.0, step=0.1)

    if st.button("📊 Calcular e Prever IMC"):
        imc_atual = calcular_imc(peso, altura / 100)
        st.info(f"💡 Seu IMC atual é aproximadamente **{imc_atual:.2f}**")

        # Mapeamento de entrada para os encoders
        if sexo not in label_encoders['sexo'].classes_:
            label_encoders['sexo'].classes_ = np.append(label_encoders['sexo'].classes_, sexo)
        
        sexo_encoded = label_encoders['sexo'].transform([sexo])[0]

        # Usar categorias fixas para escolaridade, raça e UF
        escolaridade_padrao = 'Médio'
        label_encoders['escolaridade'] = atualizar_label_encoder(label_encoders['escolaridade'], [escolaridade_padrao])
        escolaridade_encoded = label_encoders['escolaridade'].transform([escolaridade_padrao])[0]

        raca_padrao = label_encoders['raca_cor'].transform(['Parda'])[0]
        uf_padrao = label_encoders['sigla_uf'].transform(['RR'])[0]

        # Continuando com o restante do código como estava
        entrada = pd.DataFrame([[idade_futura, sexo_encoded, peso, altura / 100, escolaridade_encoded, raca_padrao, uf_padrao]], columns=X.columns)
        imc_previsto = ada_model.predict(entrada)[0]

        st.success(f"📈 Seu IMC previsto para daqui a {anos_futuros} anos é: **{imc_previsto:.2f}**")

        # Gráfico comparativo
        comparativo = pd.DataFrame({
            'Tipo': ['Atual', f'Previsto (+{anos_futuros} anos)'],
            'IMC': [imc_atual, imc_previsto]
        })

        fig_comp = px.bar(
            comparativo,
            x='Tipo',
            y='IMC',
            color='Tipo',
            text='IMC',
            title="📊 Comparação entre IMC Atual e Futuro",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig_comp.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_comp.update_layout(showlegend=False, yaxis_title="IMC")

        st.plotly_chart(fig_comp)
