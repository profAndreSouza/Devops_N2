"""
Tarefa 09: Boxplots & Violin Plots Comparativos
Módulo: EDA & Estatística
Aluno Responsável: Felipe Nunes Ramalho

Cria boxplots e violin plots para comparar a distribuição de uma variável
numérica entre grupos. As colunas podem ser informadas em ``params`` por meio
das chaves ``value_col`` e ``group_col``; quando não são informadas, elas são
selecionadas automaticamente.
"""

import base64
import json

import numpy as np
import pandas as pd
import plotly.express as px


TITLE = "Tarefa 09 - Boxplots & Violin Plots Comparativos"
STUDENT = "Felipe Nunes Ramalho"


def _decode_bdata(obj):
    """Converte arrays binários do Plotly 6 para listas aceitas pelo frontend."""
    if isinstance(obj, dict):
        if "bdata" in obj and "dtype" in obj:
            raw = base64.b64decode(obj["bdata"])
            return np.frombuffer(raw, dtype=np.dtype(obj["dtype"])).tolist()
        return {key: _decode_bdata(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [_decode_bdata(value) for value in obj]
    return obj


def _fig_to_plain_json(fig):
    """Serializa a figura sem depender do suporte a bdata do Plotly.js."""
    return json.dumps(_decode_bdata(json.loads(fig.to_json())))


def _error_result(message, numeric_count=0):
    return {
        "title": TITLE,
        "description": message,
        "metrics": {
            "Aluno Responsável": STUDENT,
            "Variáveis Numéricas Disponíveis": int(numeric_count),
            "Status": "Sem dados suficientes",
        },
        "tables": [],
        "plots": [],
    }


def _is_identifier(series, column_name):
    """Evita selecionar IDs como a medida principal do gráfico."""
    name = str(column_name).lower()
    del series  # Mantido no contrato da função para facilitar extensões futuras.
    return (
        name == "id"
        or name.endswith("_id")
        or name.startswith("id_")
        or name in {"index", "row_number", "row_num"}
        or name.startswith("unnamed:")
    )


def _select_value_column(df, requested=None):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if requested in numeric_cols:
        return requested, numeric_cols

    continuous = [
        col
        for col in numeric_cols
        if df[col].nunique(dropna=True) > 5 and not _is_identifier(df[col], col)
    ]
    fallback = [col for col in numeric_cols if not _is_identifier(df[col], col)]
    # Se só houver identificadores numéricos, é melhor informar que não existe
    # uma medida adequada do que produzir uma comparação sem significado.
    candidates = continuous or fallback
    return (candidates[0] if candidates else None), numeric_cols


def _select_group_column(df, value_col, requested=None, max_groups=12):
    if requested in df.columns and requested != value_col:
        cardinality = df[requested].nunique(dropna=True)
        if 2 <= cardinality <= max_groups:
            return requested

    candidates = []
    for col in df.columns:
        if col == value_col:
            continue
        cardinality = df[col].nunique(dropna=True)
        if not 2 <= cardinality <= max_groups:
            continue
        is_categorical = (
            isinstance(df[col].dtype, pd.CategoricalDtype)
            or pd.api.types.is_object_dtype(df[col])
            or pd.api.types.is_string_dtype(df[col])
            or pd.api.types.is_bool_dtype(df[col])
        )
        # Colunas textuais têm prioridade; numéricas discretas são o fallback.
        priority = 0 if is_categorical else 1
        candidates.append((priority, cardinality, col))

    candidates.sort(key=lambda item: (item[0], item[1]))
    return candidates[0][2] if candidates else None


def _quartile_group(df, value_col, numeric_cols):
    """Cria grupos por quartis quando o dataset não possui categoria adequada."""
    alternatives = [
        col
        for col in numeric_cols
        if col != value_col
        and df[col].nunique(dropna=True) > 3
        and not _is_identifier(df[col], col)
    ]
    if not alternatives:
        return None, None

    source_col = alternatives[0]
    ranked = df[source_col].rank(method="first")
    try:
        groups = pd.qcut(ranked, q=4, labels=["Q1", "Q2", "Q3", "Q4"])
    except ValueError:
        return None, None
    return groups, source_col


def _group_statistics(work, group_col, value_col):
    rows = []
    for group, values in work.groupby(group_col, observed=True, sort=True)[value_col]:
        values = values.dropna()
        q1 = values.quantile(0.25)
        median = values.quantile(0.50)
        q3 = values.quantile(0.75)
        iqr = q3 - q1
        lower_limit = q1 - 1.5 * iqr
        upper_limit = q3 + 1.5 * iqr
        outliers = ((values < lower_limit) | (values > upper_limit)).sum()
        rows.append(
            {
                "Grupo": str(group),
                "Observações": int(values.count()),
                "Média": values.mean(),
                "Q1": q1,
                "Mediana": median,
                "Q3": q3,
                "IQR": iqr,
                "Limite inferior": lower_limit,
                "Limite superior": upper_limit,
                "Outliers": int(outliers),
            }
        )

    stats = pd.DataFrame(rows)
    numeric_stats = stats.select_dtypes(include=[np.number]).columns
    stats[numeric_stats] = stats[numeric_stats].round(3)
    return stats


def _style_figure(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#E9ECEF"},
        autosize=True,
        margin={"l": 60, "r": 40, "t": 70, "b": 60},
        legend_title_text="Grupo",
    )
    return fig


def run_feature(df, params=None):
    params = params or {}
    if not isinstance(df, pd.DataFrame) or df.empty:
        return _error_result("O DataFrame está vazio ou é inválido.")

    value_col, numeric_cols = _select_value_column(df, params.get("value_col"))
    if value_col is None:
        return _error_result(
            "Não há uma variável numérica disponível para construir os gráficos.",
            len(numeric_cols),
        )

    try:
        max_groups = max(2, int(params.get("max_groups", 12)))
    except (TypeError, ValueError):
        max_groups = 12

    group_col = _select_group_column(
        df, value_col, params.get("group_col"), max_groups=max_groups
    )
    work = df[[value_col]].copy()
    derived_from = None

    if group_col:
        work[group_col] = df[group_col]
        group_label = group_col
    else:
        groups, derived_from = _quartile_group(df, value_col, numeric_cols)
        if groups is None:
            return _error_result(
                "Não há uma coluna de agrupamento adequada para a comparação.",
                len(numeric_cols),
            )
        group_label = f"Quartil de {derived_from}"
        work[group_label] = groups
        group_col = group_label

    work = work.dropna(subset=[value_col, group_col]).copy()
    if work.empty or work[group_col].nunique() < 2:
        return _error_result(
            "Não há observações completas em pelo menos dois grupos para comparar.",
            len(numeric_cols),
        )

    # Rótulos textuais evitam que categorias numéricas sejam tratadas como escala.
    work[group_col] = work[group_col].astype(str)
    stats = _group_statistics(work, group_col, value_col)

    box_fig = px.box(
        work,
        x=group_col,
        y=value_col,
        color=group_col,
        points="outliers",
        title=f"Boxplot de {value_col} por {group_label}",
        labels={group_col: group_label, value_col: value_col},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    box_fig.update_traces(boxmean=True)
    box_fig = _style_figure(box_fig)

    violin_fig = px.violin(
        work,
        x=group_col,
        y=value_col,
        color=group_col,
        box=True,
        points="outliers",
        title=f"Violin plot de {value_col} por {group_label}",
        labels={group_col: group_label, value_col: value_col},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    violin_fig.update_traces(meanline_visible=True)
    violin_fig = _style_figure(violin_fig)

    total_outliers = int(stats["Outliers"].sum())
    metrics = {
        "Aluno Responsável": STUDENT,
        "Variável Analisada": value_col,
        "Variável de Agrupamento": group_label,
        "Grupos Comparados": int(work[group_col].nunique()),
        "Observações Utilizadas": int(len(work)),
        "Outliers pelo Critério IQR": total_outliers,
    }
    if derived_from:
        metrics["Agrupamento Automático"] = f"Quartis de {derived_from}"

    description = (
        f"Foram comparadas as distribuições de '{value_col}' entre os grupos de "
        f"'{group_label}'. O boxplot destaca mediana, quartis, média e possíveis "
        "outliers pelo critério de 1,5 × IQR; o violin plot complementa a análise "
        "mostrando a forma e a concentração da distribuição em cada grupo."
    )

    return {
        "title": TITLE,
        "description": description,
        "metrics": metrics,
        "tables": [
            stats.to_html(
                classes="table table-striped table-dark", index=False, border=0
            )
        ],
        "plots": [_fig_to_plain_json(box_fig), _fig_to_plain_json(violin_fig)],
    }
