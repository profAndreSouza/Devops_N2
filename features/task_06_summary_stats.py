import pandas as pd
import plotly.express as px


def run_feature(df, params=None):
    params = params or {}

    # Identificar as colunas numéricas
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    # Remover colunas que são apenas identificadores
    numeric_cols = [
        col for col in numeric_cols
        if col not in ["passenger_id", "id"]
    ]

    # Caso não existam variáveis numéricas
    if not numeric_cols:
        return {
            "title": "Tarefa 06 - Estatísticas Descritivas & Perfil",
            "description": (
                "O dataset não possui variáveis numéricas suficientes "
                "para realizar a análise estatística."
            ),
            "metrics": {
                "Quantidade de Linhas": len(df),
                "Quantidade de Colunas": len(df.columns),
                "Variáveis Numéricas": 0,
                "Valores Ausentes": int(df.isna().sum().sum())
            },
            "tables": [],
            "plots": []
        }

    # Calcular estatísticas descritivas
    df_resultado = df[numeric_cols].describe().T

    # Adicionar assimetria
    df_resultado["skewness"] = df[numeric_cols].skew()

    # Adicionar curtose
    df_resultado["kurtosis"] = df[numeric_cols].kurtosis()

    # Arredondar os valores
    df_resultado = df_resultado.round(2)

    # Criar métricas gerais
    metrics = {
        "Quantidade de Linhas": len(df),
        "Quantidade de Colunas": len(df.columns),
        "Variáveis Numéricas": len(numeric_cols),
        "Valores Ausentes": int(df.isna().sum().sum())
    }

    # Criar tabela HTML
    table_html = df_resultado.to_html(
        classes="table table-striped"
    )

    # Criar gráfico
    plots = []

    coluna = numeric_cols[0]

    fig = px.histogram(
        df,
        x=coluna,
        title=f"Distribuição da variável {coluna}"
    )

    plots.append(fig.to_json())

    return {
        "title": "Tarefa 06 - Estatísticas Descritivas & Perfil",

        "description": (
            "Análise estatística descritiva das variáveis numéricas "
            "do dataset, incluindo medidas de tendência central, "
            "dispersão, percentis, assimetria e curtose."
        ),

        "metrics": metrics,

        "tables": [table_html],

        "plots": plots
    }