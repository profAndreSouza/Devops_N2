"""
Tarefa 10: Matriz de Dispersão (Pairplot)
Módulo: EDA & Estatística
Aluno Responsável: Felipe Pinheiro Lopes

Instruções para o Aluno (Felipe Pinheiro Lopes):
1. Utilize o DataFrame `df` recebido como parâmetro de entrada.
2. Objetivo: Construir matriz de dispersão multivariada para identificar padrões cruzados.
3. Desenvolva sua lógica utilizando Python, Pandas, Scikit-learn, Plotly, etc.
4. Retorne um dicionário no formato exato:
   {
       "title": "Tarefa 10 - Matriz de Dispersão (Pairplot)",
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


def _decode_bdata(obj):
    """Plotly 6.x serializa arrays numéricos como base64 (bdata/dtype).
    O Plotly.js 2.27 (usado no template) não decodifica isso, deixando o
    gráfico vazio. Convertemos de volta para listas Python planas."""
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


def _select_features(df, max_vars):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) > max_vars:
        numeric_cols = numeric_cols[:max_vars]
    return numeric_cols


def _detect_color_col(df, numeric_cols, requested):
    if requested and requested in df.columns:
        return requested
    candidates = [
        c for c in df.columns
        if c not in numeric_cols and df[c].dtype == object
    ]
    for c in candidates:
        if 2 <= df[c].nunique(dropna=True) <= 12:
            return c
    return None


def run_feature(df, params=None):
    params = params or {}
    max_vars = int(params.get("max_vars", 5))
    color_col = params.get("color_col", None)
    corr_method = params.get("corr_method", "pearson")

    numeric_cols = _select_features(df, max_vars)

    if len(numeric_cols) < 2:
        return {
            "title": "Tarefa 10 - Matriz de Dispersão (Pairplot)",
            "description": "Não há variáveis numéricas suficientes para construir a matriz de dispersão.",
            "metrics": {
                "Aluno Responsável": "Felipe Pinheiro Lopes",
                "Variáveis Numéricas Disponíveis": len(numeric_cols),
                "Status": "Sem dados suficientes"
            },
            "tables": [],
            "plots": []
        }

    color_col = _detect_color_col(df, numeric_cols, color_col)
    plot_cols = list(numeric_cols)
    if color_col:
        plot_cols = plot_cols + [color_col]

    work = df[plot_cols].dropna()

    fig = px.scatter_matrix(
        work,
        dimensions=numeric_cols,
        color=color_col if color_col else None,
        title="Matriz de Dispersão (Pairplot) - Relacionamentos Cruzados",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    if color_col:
        fig.update_traces(
            diagonal={"visible": False},
            showupperhalf=False,
            marker_size=4
        )
    else:
        fig.update_traces(
            diagonal={"visible": False},
            showupperhalf=False,
            marker_size=4,
            marker_color="#4CC9F0"
        )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E9ECEF"),
        autosize=True,
        margin=dict(l=60, r=40, t=60, b=40)
    )

    corr = df[numeric_cols].corr(method=corr_method)
    corr_reset = corr.round(3).reset_index().rename(columns={"index": "Variável"})

    strongest_pair = None
    strongest_val = 0.0
    cols = corr.columns.tolist()
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            v = abs(corr.iloc[i, j])
            if v > strongest_val:
                strongest_val = v
                strongest_pair = (cols[i], cols[j], round(float(corr.iloc[i, j]), 3))

    metrics = {
        "Aluno Responsável": "Felipe Pinheiro Lopes",
        "Variáveis Analisadas": len(numeric_cols),
        "Observações Utilizadas": int(len(work)),
        "Cor Coloração": color_col if color_col else "Nenhuma",
        "Método de Correlação": corr_method,
    }
    if strongest_pair:
        metrics["Par Mais Correlacionado"] = f"{strongest_pair[0]} x {strongest_pair[1]}"
        metrics["Correlação do Par"] = strongest_pair[2]

    description = (
        "Matriz de dispersão (pairplot) construída com Plotly para inspecionar "
        "visualmente os relacionamentos cruzados entre as variáveis numéricas. "
        "Cada célula fora da diagonal é um gráfico de dispersão entre um par de "
        "variáveis, permitindo identificar correlações, agrupamentos e padrões "
        "multivariados. A diagonal é omitida para destacar as relações entre pares."
    )

    return {
        "title": "Tarefa 10 - Matriz de Dispersão (Pairplot)",
        "description": description,
        "metrics": metrics,
        "tables": [corr_reset.to_html(classes="table table-striped table-dark", index=False)],
        "plots": [_fig_to_plain_json(fig)]
    }
