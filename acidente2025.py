import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


def carregar_dados(caminho_arquivo):
    caminho_arquivo = os.path.join(os.getcwd(), caminho_arquivo)

    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError("Arquivo não encontrado.")

    df = pd.read_csv(caminho_arquivo, sep=';', encoding='ISO-8859-1', low_memory=False)
    df.replace(['NA', 'N/A', 'NaN', 'nan', 'NULL', 'null', 'na', ''], np.nan, inplace=True)

    if df.empty:
        raise ValueError("O arquivo de dados está vazio.")
    
    print(df.columns)

    return df

def tratar_dados(df):
    colunas_categoricas = ['sexo', 'estado_fisico', 'tipo_veiculo']

    for coluna in colunas_categoricas:
        df[coluna] = df[coluna].fillna('Não informado')

    df['data_inversa'] = pd.to_datetime(df['data_inversa'], format='%Y-%m-%d', errors='coerce')

    return df

def gerar_insights(df):
    print("Total de Acidentes:", len(df))
    
    print("\nTipos de Veículo com mais acidentes:")
    print(df['tipo_veiculo'].value_counts())

    print("\nEstados com mais acidentes:")
    print(df['uf'].value_counts())
    
    df['mes'] = df['data_inversa'].dt.month
    print("\nMeses mais críticos:")
    print(df['mes'].value_counts().sort_values(ascending=False))

    df['ano'] = df['data_inversa'].dt.year
    print("\nAcidentes contabilizados em 2025:")
    print(df['ano'].value_counts().sort_index())

    percentual_obitos = (df[df['mortos'] > 0]['id'].nunique() / df['id'].nunique()) * 100
    print(f"\nPercentual de Acidentes com Óbito: {percentual_obitos:.2f}%")
    
    
    return df


def gerar_graficos(df):
    sns.set(style="whitegrid")

    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, x='tipo_veiculo', order=df['tipo_veiculo'].value_counts().index)
    plt.title('Tipos de Veículo Envolvidos')
    plt.xticks(rotation=45)
    plt.show()

    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, x='uf', order=df['uf'].value_counts().index)
    plt.title('Estados com mais Acidentes')
    plt.xticks(rotation=45)
    plt.show()

    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, x='dia_semana', hue='dia_semana', palette='viridis', legend=False)
    plt.title('Dias com mais Acidentes')
    plt.show()


caminho = 'Arquivos/acidentes2025_todas_causas_tipos.csv'
df = carregar_dados(caminho)
df = tratar_dados(df)
df = gerar_insights(df)
gerar_graficos(df)
