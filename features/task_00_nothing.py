"""
Tarefa 00: Violin Plot (Distribuição e Densidade Comparativa)
Módulo: EDA & Estatística
Aluno Responsável: Devops N2 Team / Nothing
"""

import base64
import json
import numpy as np
import pandas as pd
import plotly.express as px


def _decode_bdata(obj):
    """Garante compatibilidade de arrays serializados com plotly.js no front-end."""
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


def _find_columns(df, requested_num=None, requested_cat=None):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Seleção da coluna numérica
    if requested_num and requested_num in numeric_cols:
        num_col = requested_num
    elif numeric_cols:
        num_col = numeric_cols[0]
    else:
        num_col = None

    # Seleção da coluna categórica para agrupamento
    cat_col = None
    if requested_cat and requested_cat in df.columns:
        cat_col = requested_cat
    else:
        candidates = [
            c for c in df.columns
            if c != num_col and (df[c].dtype == object or df[c].nunique() <= 10)
        ]
        for c in candidates:
            n_unique = df[c].nunique(dropna=True)
            if 2 <= n_unique <= 10:
                cat_col = c
                break

    return num_col, cat_col


def run_feature(df, params=None):
    """
    Gera uma análise por Violin Plot combinando densidade KDE com boxplot integrado.
    """
    params = params or {}
    req_num = params.get("num_col")
    req_cat = params.get("cat_col")
    points = params.get("points", "all")
    show_box = params.get("box", True)

    num_col, cat_col = _find_columns(df, req_num, req_cat)

    if not num_col:
        return {
            "title": "Tarefa 00 - Violin Plot",
            "description": "Nenhuma coluna numérica disponível no DataFrame para geração do Violin Plot.",
            "metrics": {
                "Status": "Sem dados numéricos suficientes",
                "Total de Linhas": len(df),
                "Total de Colunas": len(df.columns)
            },
            "tables": [],
            "plots": []
        }

    # Filtrar dados válidos
    subset_cols = [num_col] + ([cat_col] if cat_col else [])
    df_clean = df[subset_cols].dropna().copy()

    if df_clean.empty:
        return {
            "title": "Tarefa 00 - Violin Plot",
            "description": "Os dados selecionados não possuem registros válidos após remoção de valores nulos.",
            "metrics": {"Status": "Sem registros válidos"},
            "tables": [],
            "plots": []
        }

    # Construção do gráfico Violin Plot com Plotly Express
    fig = px.violin(
        df_clean,
        y=num_col,
        x=cat_col if cat_col else None,
        color=cat_col if cat_col else None,
        box=show_box,
        points=points,
        hover_data=subset_cols,
        title=f"Violin Plot: Distribuição de '{num_col}'" + (f" por '{cat_col}'" if cat_col else ""),
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E9ECEF"),
        autosize=True,
        margin=dict(l=50, r=40, t=60, b=50),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Cálculo de métricas estatísticas
    series_num = df_clean[num_col]
    q1 = float(series_num.quantile(0.25))
    q3 = float(series_num.quantile(0.75))
    iqr = round(q3 - q1, 3)

    metrics = {
        "Variável Numérica": num_col,
        "Agrupamento": cat_col if cat_col else "Global (Sem grupo)",
        "Amostras Válidas": int(len(df_clean)),
        "Média": round(float(series_num.mean()), 3),
        "Mediana": round(float(series_num.median()), 3),
        "Desvio Padrão": round(float(series_num.std()), 3),
        "IQR (Q3 - Q1)": iqr,
        "Mínimo": round(float(series_num.min()), 3),
        "Máximo": round(float(series_num.max()), 3)
    }

    # Tabela descritiva por grupo ou geral
    if cat_col:
        stats_df = df_clean.groupby(cat_col)[num_col].describe().round(3).reset_index()
        stats_df.rename(columns={
            "count": "Contagem",
            "mean": "Média",
            "std": "Desvio Padrão",
            "min": "Mínimo",
            "25%": "Q1 (25%)",
            "50%": "Mediana (50%)",
            "75%": "Q3 (75%)",
            "max": "Máximo"
        }, inplace=True)
    else:
        stats_df = series_num.describe().round(3).to_frame(name="Valor").reset_index()
        stats_df.rename(columns={"index": "Estatística"}, inplace=True)

    table_html = stats_df.to_html(classes="table table-striped table-dark table-hover", index=False)

    description = (
        f"O Violin Plot combina a estimativa de densidade por kernel (KDE) com um boxplot "
        f"interno para a variável '{num_col}'"
        + (f", segmentado pelas categorias de '{cat_col}'." if cat_col else ".")
        + " Permite visualizar a forma da distribuição, assimetria, multimodalidade e a dispersão dos quartis simultaneamente."
    )

    return {
        "title": "Tarefa 00 - Violin Plot (Distribuição e Densidade)",
        "description": description,
        "metrics": metrics,
        "tables": [table_html],
        "plots": [_fig_to_plain_json(fig)]
    }
