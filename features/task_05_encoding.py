"""
Tarefa 05: Codificação Categórica (One-Hot & Label)
Módulo: Ingestão & Limpeza
Aluno Responsável: Edilaine Paulino Solde

Instruções para o Aluno (Edilaine Paulino Solde):
1. Utilize o DataFrame `df` recebido como parâmetro de entrada.
2. Objetivo: Realizar a codificação de variáveis categóricas usando One-Hot Encoding ou Label Encoding.
3. Desenvolva sua lógica utilizando Python, Pandas, Scikit-learn, Plotly, etc.
4. Retorne um dicionário no formato exato:
   {
       "title": "Tarefa 05 - Codificação Categórica (One-Hot & Label)",
       "description": "Explicação breve do que seu código realizou.",
       "metrics": {"Métrica 1": valor1, "Métrica 2": valor2},
       "tables": [df_resultado.to_html(classes="table table-striped")],
       "plots": [figura_plotly.to_json()]
   }
"""

def run_feature(df, params=None):
    params = params or {}
    
    # TODO (Edilaine Paulino Solde): Desenvolva aqui a lógica da sua funcionalidade.
    
    return {
        "title": "Tarefa 05 - Codificação Categórica (One-Hot & Label)",
        "description": "Atividade aguardando implementação pelo(a) aluno(a) Edilaine Paulino Solde.",
        "metrics": {
            "Aluno Responsável": "Edilaine Paulino Solde",
            "Status": "Pendente de Implementação"
        },
        "tables": [],
        "plots": []
    }
import pandas as pd
import plotly.express as px


def tarefa_05(df):
    """
    Tarefa 05 - Codificação Categórica (One-Hot & Label)

    Realiza One-Hot Encoding nas variáveis categóricas
    do DataFrame recebido.
    """

    # Faz uma cópia para não alterar o DataFrame original
    df_resultado = df.copy()

    # Identifica as colunas categóricas
    colunas_categoricas = df_resultado.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    # Quantidade de colunas antes da codificação
    colunas_antes = df_resultado.shape[1]

    # Aplica One-Hot Encoding
    if colunas_categoricas:
        df_resultado = pd.get_dummies(
            df_resultado,
            columns=colunas_categoricas,
            dtype=int
        )

    # Quantidade de colunas depois da codificação
    colunas_depois = df_resultado.shape[1]

    # Quantidade de novas colunas criadas
    novas_colunas = colunas_depois - colunas_antes

    # Cria gráfico com a quantidade de categorias por variável
    dados_plot = []

    for coluna in colunas_categoricas:
        quantidade = df[coluna].nunique(dropna=True)

        dados_plot.append({
            "Variável": coluna,
            "Quantidade de categorias": quantidade
        })

    if dados_plot:
        df_plot = pd.DataFrame(dados_plot)

        figura = px.bar(
            df_plot,
            x="Variável",
            y="Quantidade de categorias",
            title="Quantidade de categorias por variável"
        )
    else:
        figura = px.bar(
            title="Nenhuma variável categórica encontrada"
        )

    # Retorno no formato solicitado
    return {
        "title": "Tarefa 05 - Codificação Categórica (One-Hot & Label)",
        "description": (
            "O código identificou as variáveis categóricas do DataFrame "
            "e aplicou One-Hot Encoding, transformando cada categoria "
            "em uma nova variável binária. Também foram calculadas "
            "métricas relacionadas à quantidade de colunas antes e "
            "depois da codificação."
        ),
        "metrics": {
            "Colunas antes da codificação": colunas_antes,
            "Colunas depois da codificação": colunas_depois,
            "Novas colunas criadas": novas_colunas,
            "Variáveis categóricas identificadas": len(colunas_categoricas)
        },
        "tables": [
            df_resultado.to_html(
                classes="table table-striped",
                index=False
            )
        ],
        "plots": [
            figura.to_json()
        ]
    }