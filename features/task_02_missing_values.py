"""
Tarefa 02: Tratamento de Valores Ausentes
Módulo: Ingestão & Limpeza
Aluno Responsável: Anthony Pais Dos Santos

Instruções para o Aluno (Anthony Pais Dos Santos):
1. Utilize o DataFrame `df` recebido como parâmetro de entrada.
2. Objetivo: Implementar imputação de valores nulos utilizando Média, Mediana ou KNN Imputer.
3. Desenvolva sua lógica utilizando Python, Pandas, Scikit-learn, Plotly, etc.
4. Retorne um dicionário no formato exato:
   {
       "title": "Tarefa 02 - Tratamento de Valores Ausentes",
       "description": "Explicação breve do que seu código realizou.",
       "metrics": {"Métrica 1": valor1, "Métrica 2": valor2},
       "tables": [df_resultado.to_html(classes="table table-striped")],
       "plots": [figura_plotly.to_json()]
   }
"""

import base64
import json

import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.impute import KNNImputer, SimpleImputer


def _decode_bdata(obj):
    if isinstance(obj, dict):
        if "bdata" in obj and "dtype" in obj:
            raw = base64.b64decode(obj["bdata"])
            arr = np.frombuffer(raw, dtype=np.dtype(obj["dtype"]))
            return arr.tolist()
        return {k: _decode_bdata(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_decode_bdata(v) for v in obj]
    return obj


def _fig_to_plain_json(fig):
    fig_dict = json.loads(fig.to_json())
    return json.dumps(_decode_bdata(fig_dict))


def _get_numeric_cols(df):
    return df.select_dtypes(include=[np.number]).columns.tolist()


def run_feature(df, params=None):
    params = params or {}
    method = params.get("method", "knn").lower()

    numeric_cols = _get_numeric_cols(df)
    missing_counts = df[numeric_cols].isna().sum()
    total_missing = int(missing_counts.sum())

    if total_missing == 0:
        return {
            "title": "Tarefa 02 - Tratamento de Valores Ausentes",
            "description": "Nenhum valor ausente encontrado nas colunas numéricas. Nenhuma imputação foi necessária.",
            "metrics": {
                "Aluno Responsável": "Anthony Pais Dos Santos",
                "Colunas Numéricas": len(numeric_cols),
                "Valores Ausentes Totais": 0,
                "Status": "Sem valores ausentes"
            },
            "tables": [],
            "plots": []
        }

    df_imputed = df.copy()
    before_series = missing_counts[missing_counts > 0].sort_values(ascending=False)

    if method == "knn":
        imputer = KNNImputer(n_neighbors=5)
        df_imputed[numeric_cols] = imputer.fit_transform(df_imputed[numeric_cols])
        method_label = "KNN Imputer (k=5)"
    elif method == "median":
        imputer = SimpleImputer(strategy="median")
        df_imputed[numeric_cols] = imputer.fit_transform(df_imputed[numeric_cols])
        method_label = "Mediana"
    else:
        imputer = SimpleImputer(strategy="mean")
        df_imputed[numeric_cols] = imputer.fit_transform(df_imputed[numeric_cols])
        method_label = "Média"

    after_counts = df_imputed[numeric_cols].isna().sum()
    after_series = after_counts[before_series.index].sort_values(ascending=False)

    comparison = pd.DataFrame({
        "Coluna": before_series.index,
        "Ausentes_Antes": before_series.values,
        "Ausentes_Depois": after_series.values
    })

    comparison_html = comparison.to_html(classes="table table-striped table-dark", index=False)

    plot_df = pd.DataFrame({
        "Coluna": list(before_series.index) * 2,
        "Quantidade": list(before_series.values) + list(after_series.values),
        "Situação": ["Antes"] * len(before_series) + ["Depois"] * len(after_series)
    })

    fig = px.bar(
        plot_df,
        x="Coluna",
        y="Quantidade",
        color="Situação",
        barmode="group",
        title=f"Valores Ausentes por Coluna - Antes vs Depois ({method_label})",
        color_discrete_sequence=["#F72585", "#4CC9F0"]
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E9ECEF"),
        autosize=True,
        margin=dict(l=60, r=40, t=60, b=40)
    )

    metrics = {
        "Aluno Responsável": "Anthony Pais Dos Santos",
        "Método Utilizado": method_label,
        "Colunas Numéricas": len(numeric_cols),
        "Colunas com Ausências": int(len(before_series)),
        "Valores Ausentes Totais (Antes)": total_missing,
        "Valores Ausentes Totais (Depois)": int(after_counts.sum()),
        "Status": "Imputação Concluída"
    }

    description = (
        f"Imputação de valores ausentes aplicada nas colunas numéricas utilizando o método {method_label}. "
        "Os valores nulos foram substituídos mantendo a estrutura estatística original dos dados, "
        "permitindo que análises e modelos subsequentes funcionem corretamente."
    )

    return {
        "title": "Tarefa 02 - Tratamento de Valores Ausentes",
        "description": description,
        "metrics": metrics,
        "tables": [comparison_html],
        "plots": [_fig_to_plain_json(fig)]
    }
