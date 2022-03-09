import streamlit as st
from joblib import load
import pandas as pd
from utils import Transformador

#Cor de fundo do listbox
st.markdown(
    '<style>div[role="listbox"] ul{background-color: #006400;</style>',
    unsafe_allow_html=True)


def validar_dados(dict_respostas):
    if dict_respostas['Anos_empregado'] != 0 and dict_respostas['Anos_desempregado'] != 0:
        st.warning('Por favor preencher somente anos empregado ou anos desempregado')
        return False
    
    return True

def avaliar_mau(dict_respostas):
    modelo = load('objetos/modelo.joblib')
    features = load('objetos/features.joblib')

    if dict_respostas['Anos_desempregado'] > 0:
        dict_respostas['Anos_empregado'] = \
            dict_respostas['Anos_desempregado'] * -1

    respostas_clientes = []

    for coluna in features:
        respostas_clientes.append(dict_respostas[coluna])

    df_novo_cliente = pd.DataFrame(data=[respostas_clientes], columns=features)
    mau = modelo.predict(df_novo_cliente)[0]

    return mau


st.image('imgs/bytebank_logo.png')
st.write('# Simulador de Avaliação de Crédito')


my_expander1 = st.expander('Trabalho')

my_expander2 = st.expander('Pessoal')

my_expander3 = st.expander('Familia')

dict_respostas = {}
lista_campos = load('objetos/lista_campos.joblib')

#Trabalho
with my_expander1:
    col1_form, col2_form = st.columns(2)
    
    dict_respostas['Categoria_de_renda'] = col1_form.selectbox(
        'Qual a categoria de renda?', lista_campos['Categoria_de_renda'],
    )

    dict_respostas['Rendimento_Anual'] = col1_form.slider(
        'Qual o salário mensal?', help='Valor ajustável com a seta',
        min_value=0, max_value=35000, step=500
        
    ) * 12

    dict_respostas['Anos_empregado'] = col1_form.slider(
        'Quantos anos empregado?', min_value=0, max_value=50                       
    )

    dict_respostas['Ocupacao'] = col2_form.selectbox(
        'Qual a sua ocupação?', lista_campos['Ocupacao']
    )

    dict_respostas['Tem_telefone_trabalho'] = 1 if col2_form.selectbox(
        'Tem telefone no trabalho?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Anos_desempregado'] = col2_form.slider(
        'Quantos anos dempregado?', min_value=0, max_value=50                       
    )
    

#Pessoal  
with my_expander2:
    col1_form, col2_form = st.columns(2)
 
    dict_respostas['Grau_Escolaridade'] = col1_form.selectbox(
        'Qual o grau de escolaridade?', lista_campos['Grau_Escolaridade']
    )

    dict_respostas['Idade'] = col2_form.slider('Qual sua idade?',
        min_value=0, max_value=100, step=1
    )

    dict_respostas['Estado_Civil'] = col1_form.selectbox(
        'Qual o estado civil?', lista_campos['Estado_Civil']
    )

    dict_respostas['Tem_email'] = 1 if col1_form.selectbox(
        'Possui E-mail?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Tem_Carro'] = 1 if col2_form.selectbox(
        'Tem Carro?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Tem_telefone_fixo'] = 1 if col2_form.selectbox( 
        'Possui telefone fixo', ['Sim', 'Não']) == 'Sim' else 0



#Familia
with my_expander3:
    col1_form, col2_form = st.columns(2)
    dict_respostas['Qtd_Filhos'] = col1_form.slider('Quantos Filhos?', 
        min_value=0, max_value=10)

    dict_respostas['Tamanho_Familia'] = col1_form.slider(
        'Quantas pessoas moram com você?', min_value=1, max_value=10)
    
    dict_respostas['Tem_Casa_Propria'] = 1 if col2_form.selectbox( 
        'Possui casa própria?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Moradia'] = col2_form.selectbox( 
        'Qual o tipo de moradia?', lista_campos['Moradia']
    )
    

if st.button('Avaliar crédito') and validar_dados(dict_respostas):
    if avaliar_mau(dict_respostas):
        st.error('Crédito Negado')

    else:
        st.success('Crédito Aprovado')