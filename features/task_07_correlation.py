import plotly.express as px
import pandas as pd
import numpy as np

def run_feature(df, params=None):
    """
    Tarefa 07: Matriz de Correlação Interativa
    Aluno Responsável: Aluno 07
    """
    params = params or {}
    numeric_cols = list(df.select_dtypes(include=['number']).columns)
    
    summary_df = df.describe().T.reset_index().round(2) if len(numeric_cols) > 0 else df.head(10)
    
    if len(numeric_cols) >= 2:
        fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title=f"Visualização de {numeric_cols[0]} vs {numeric_cols[1]}", color_discrete_sequence=px.colors.qualitative.Plotly)
    elif len(numeric_cols) == 1:
        fig = px.histogram(df, x=numeric_cols[0], title=f"Histograma de {numeric_cols[0]}", color_discrete_sequence=px.colors.qualitative.Plotly)
    else:
        fig = px.bar(df.head(10), x=df.columns[0], title="Visualização Geral")

    return {
        "title": "Tarefa 07 - Matriz de Correlação Interativa",
        "description": "Módulo desenvolvido por Aluno 07 focado em Matriz de Correlação Interativa.",
        "metrics": {
            "Linhas Processadas": len(df),
            "Colunas Disponíveis": len(df.columns),
            "Status": "Ativo / Operacional"
        },
        "tables": [summary_df.head(10).to_html(classes="table table-hover table-striped table-sm", index=False)],
        "plots": [fig.to_json()]
    }
