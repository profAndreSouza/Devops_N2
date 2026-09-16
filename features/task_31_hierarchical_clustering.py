"""
Tarefa 31: Clustering Hierárquico
Módulo: Clustering
Aluno Responsável: Paulo Alberto Poppes Vieira

Instruções para o Aluno (Paulo Alberto Poppes Vieira):
1. Utilize o DataFrame `df` recebido como parâmetro de entrada.
2. Objetivo: Implementar clustering hierárquico aglomerativo e gerar dendrograma.
3. Desenvolva sua lógica utilizando Python, Pandas, Scikit-learn, Plotly, etc.
4. Retorne um dicionário no formato exato:
   {
       "title": "Tarefa 31 - Clustering Hierárquico",
       "description": "Explicação breve do que seu código realizou.",
       "metrics": {"Métrica 1": valor1, "Métrica 2": valor2},
       "tables": [df_resultado.to_html(classes="table table-striped")],
       "plots": [figura_plotly.to_json()]
   }
"""

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
import plotly.figure_factory as ff


def run_feature(df, params=None):
    params = params or {}
    
    # 1. Tratamento básico: Seleciona apenas colunas numéricas e remove valores nulos
    df_numeric = df.select_dtypes(include=[np.number]).dropna()
    
    if df_numeric.empty:
        raise ValueError("O DataFrame não contém colunas numéricas válidas para clustering.")
    
    # 2. Definição de parâmetros (com valores padrão)
    n_clusters = params.get("n_clusters", 3)
    linkage_method = params.get("linkage", "ward")
    
    # 3. Ajuste do modelo de Clustering Hierárquico
    model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage_method)
    labels = model.fit_predict(df_numeric)
    
    # Cria cópia do DataFrame com os clusters atribuídos
    df_resultado = df_numeric.copy()
    df_resultado['Cluster'] = labels
    
    # 4. Cálculo de métricas de avaliação
    if len(set(labels)) > 1:
        sil_score = float(silhouette_score(df_numeric, labels))
    else:
        sil_score = 0.0
        
    metrics = {
        "Número de Clusters": n_clusters,
        "Silhouette Score": round(sil_score, 4),
        "Total de Amostras": len(df_resultado)
    }
    
    # 5. Geração do Dendrograma usando Plotly
    fig_dendro = ff.create_dendrogram(
        df_numeric.values, 
        colorscale=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    )
    fig_dendro.update_layout(
        title="Dendrograma - Clustering Hierárquico",
        xaxis_title="Índice da Amostra",
        yaxis_title="Distância (Euclidiana)",
        width=800,
        height=500
    )
    
    # 6. Retorno estruturado no formato exigido
    return {
        "title": "Tarefa 31 - Clustering Hierárquico",
        "description": f"Foi aplicado o agrupamento hierárquico aglomerativo (linkage='{linkage_method}') para a criação de {n_clusters} clusters. O dendrograma reflete a estrutura de fusão das instâncias.",
        "metrics": metrics,
        "tables": [df_resultado.head(10).to_html(classes="table table-striped", index=False)],
        "plots": [fig_dendro.to_json()]
    }
