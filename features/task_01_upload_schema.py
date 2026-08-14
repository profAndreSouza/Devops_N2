import plotly.express as px
import pandas as pd

def run_feature(df, params=None):
    """
    Tarefa 01: Visualizador de Schema e Tipos de Dados
    Aluno Responsável: Aluno 01
    """
    params = params or {}
    
    # Informações do Schema
    total_rows, total_cols = df.shape
    missing_total = int(df.isnull().sum().sum())
    numeric_cols = list(df.select_dtypes(include=['number']).columns)
    cat_cols = list(df.select_dtypes(include=['object', 'category']).columns)
    
    schema_df = pd.DataFrame({
        "Coluna": df.columns,
        "Tipo de Dado": [str(dtype) for dtype in df.dtypes],
        "Valores Nulos": df.isnull().sum().values,
        "% Nulos": (df.isnull().mean() * 100).round(2).values,
        "Valores Únicos": [df[col].nunique() for col in df.columns]
    })
    
    # Gráfico de Tipos de Dados
    type_counts = pd.Series([str(d) for d in df.dtypes]).value_counts().reset_index()
    type_counts.columns = ["Tipo", "Quantidade"]
    fig = px.pie(type_counts, names="Tipo", values="Quantidade", title="Distribuição de Tipos de Dados", color_discrete_sequence=px.colors.qualitative.Set2)
    
    return {
        "title": "Tarefa 01 - Inspeção de Schema & Tipos de Dados",
        "description": "Análise estrutural das colunas, tipos primitivos e verificação primária de integridade.",
        "metrics": {
            "Total de Linhas": total_rows,
            "Total de Colunas": total_cols,
            "Colunas Numéricas": len(numeric_cols),
            "Colunas Categóricas": len(cat_cols),
            "Valores Ausentes Globais": missing_total
        },
        "tables": [schema_df.to_html(classes="table table-hover table-bordered table-sm", index=False)],
        "plots": [fig.to_json()]
    }
