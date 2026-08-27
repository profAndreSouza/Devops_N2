"""
Tarefa 37: Gerador de Relatórios Automatizado
Módulo: Tópicos Especiais
Aluno Responsável: Vitor Fazano

Instruções para o Aluno (Vitor Fazano):
1. Utilize o DataFrame `df` recebido como parâmetro de entrada.
2. Objetivo: Gerar um relatório automatizado de resumo estatístico e diagnóstico do dataset.
3. Desenvolva sua lógica utilizando Python, Pandas, Scikit-learn, Plotly, etc.
4. Retorne um dicionário no formato exato:
   {
       "title": "Tarefa 37 - Gerador de Relatórios Automatizado",
       "description": "Explicação breve do que seu código realizou.",
       "metrics": {"Métrica 1": valor1, "Métrica 2": valor2},
       "tables": [df_resultado.to_html(classes="table table-striped")],
       "plots": [figura_plotly.to_json()]
   }
"""

def run_feature(df, params=None):
    params = params or {}
    
    # TODO (Vitor Fazano): Desenvolva aqui a lógica da sua funcionalidade.
import pandas as pd
import plotly.express as px


def run_feature(df, params=None):

    params = params or {}

    # ==========================================================
    # Validação do DataFrame
    # ==========================================================

    if df is None or not isinstance(df, pd.DataFrame):
        return {
            "title": "Tarefa 37 - Gerador de Relatórios Automatizado",
            "description": "Não foi possível gerar o relatório porque o parâmetro informado não é um DataFrame válido.",
            "metrics": {
                "Aluno Responsável": "Vitor Fazano",
                "Status": "Erro"
            },
            "tables": [],
            "plots": []
        }

    # ==========================================================
    # Informações gerais do dataset
    # ==========================================================

    total_linhas = len(df)
    total_colunas = len(df.columns)

    valores_nulos = int(df.isnull().sum().sum())
    registros_duplicados = int(df.duplicated().sum())

    colunas_numericas = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    colunas_categoricas = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    # ==========================================================
    # Percentual de valores ausentes
    # ==========================================================

    percentual_nulos = 0

    if total_linhas > 0 and total_colunas > 0:
        percentual_nulos = round(
            (valores_nulos / (total_linhas * total_colunas)) * 100,
            2
        )

    # ==========================================================
    # Tabela de diagnóstico das colunas
    # ==========================================================

    diagnostico = pd.DataFrame({
        "Coluna": df.columns,
        "Tipo": [str(df[col].dtype) for col in df.columns],
        "Valores Nulos": [
            int(df[col].isnull().sum())
            for col in df.columns
        ],
        "% Nulos": [
            round(
                (df[col].isnull().sum() / total_linhas) * 100,
                2
            ) if total_linhas > 0 else 0
            for col in df.columns
        ],
        "Valores Únicos": [
            int(df[col].nunique(dropna=True))
            for col in df.columns
        ]
    })

    # ==========================================================
    # Estatísticas das colunas numéricas
    # ==========================================================

    if colunas_numericas:

        estatisticas = df[colunas_numericas].describe().T.reset_index()

        estatisticas = estatisticas.rename(
            columns={
                "index": "Coluna",
                "count": "Quantidade",
                "mean": "Média",
                "std": "Desvio Padrão",
                "min": "Mínimo",
                "25%": "Q1",
                "50%": "Mediana",
                "75%": "Q3",
                "max": "Máximo"
            }
        )

        estatisticas = estatisticas.round(2)

    else:

        estatisticas = pd.DataFrame({
            "Informação": [
                "O dataset não possui colunas numéricas."
            ]
        })

    # ==========================================================
    # Gráfico de valores ausentes
    # ==========================================================

    nulos_por_coluna = (
        df.isnull()
        .sum()
        .reset_index()
    )

    nulos_por_coluna.columns = [
        "Coluna",
        "Valores Ausentes"
    ]

    nulos_por_coluna = nulos_por_coluna[
        nulos_por_coluna["Valores Ausentes"] > 0
    ]

    plots = []

    if not nulos_por_coluna.empty:

        fig_nulos = px.bar(
            nulos_por_coluna,
            x="Coluna",
            y="Valores Ausentes",
            title="Valores Ausentes por Coluna",
            labels={
                "Coluna": "Coluna",
                "Valores Ausentes": "Quantidade"
            }
        )

        plots.append(fig_nulos.to_json())

    # ==========================================================
    # Gráfico de distribuição
    # ==========================================================

    if colunas_numericas:

        coluna_plot = colunas_numericas[0]

        fig_distribuicao = px.histogram(
            df,
            x=coluna_plot,
            title=f"Distribuição da variável: {coluna_plot}",
            labels={
                coluna_plot: coluna_plot
            }
        )

        plots.append(fig_distribuicao.to_json())

    # ==========================================================
    # Métricas do relatório
    # ==========================================================

    metricas = {
        "Total de Linhas": total_linhas,
        "Total de Colunas": total_colunas,
        "Valores Ausentes": valores_nulos,
        "Percentual de Valores Ausentes": percentual_nulos,
        "Registros Duplicados": registros_duplicados,
        "Colunas Numéricas": len(colunas_numericas),
        "Colunas Categóricas": len(colunas_categoricas)
    }

    # ==========================================================
    # Retorno padrão solicitado pela tarefa
    # ==========================================================

    return {
        "title": "Tarefa 37 - Gerador de Relatórios Automatizado",

        "description": (
            "O código realizou uma análise automatizada do DataFrame, "
            "identificando informações gerais do dataset, valores ausentes, "
            "registros duplicados, tipos de dados, quantidade de variáveis "
            "numéricas e categóricas, além de gerar estatísticas descritivas "
            "e visualizações para auxiliar no diagnóstico dos dados."
        ),

        "metrics": metricas,

        "tables": [
            diagnostico.to_html(
                classes="table table-striped",
                index=False
            ),
            estatisticas.to_html(
                classes="table table-striped",
                index=False
            )
        ],

        "plots": plots
    }
    
   
