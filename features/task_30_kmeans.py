"""
Tarefa 30: K-Means & Método do Cotovelo
Módulo: Clustering

Instruções para o Aluno:
1. Utilize o DataFrame `df` recebido como parâmetro de entrada.
2. Objetivo: Executar agrupamento K-Means e plotar o gráfico do cotovelo (Elbow Method).
3. Desenvolva sua lógica utilizando Python, Pandas, Scikit-learn, Plotly, etc.
4. Retorne um dicionário no formato exato:
   {
       "title": "Tarefa 30 - K-Means & Método do Cotovelo",
       "description": "Explicação breve do que seu código realizou.",
       "metrics": {"Métrica 1": valor1, "Métrica 2": valor2},
       "tables": [df_resultado.to_html(classes="table table-striped")],
       "plots": [figura_plotly.to_json()]
   }
"""

import pandas as pd
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

def run_feature(df, params=None):
    params = params or {}

    if not isinstance(df, pd.DataFrame) or df.empty:
        raise ValueError("O DataFrame precisa conter pelo menos uma linha.")

    numeric_df = df.select_dtypes(include="number").copy()
    numeric_df = numeric_df.dropna(axis=1, how="all")
    if numeric_df.empty:
        raise ValueError("O DataFrame precisa conter colunas numéricas válidas.")
    if len(numeric_df) < 2:
        raise ValueError("O DataFrame precisa conter pelo menos duas linhas.")

    imputed = SimpleImputer(strategy="median").fit_transform(numeric_df)
    features = StandardScaler().fit_transform(imputed)

    def integer_param(name, default):
        try:
            return int(params.get(name, default))
        except (TypeError, ValueError):
            return default

    random_state = integer_param("random_state", 42)
    max_allowed_k = min(10, len(numeric_df))
    min_k = max(2, integer_param("min_k", 2))
    max_k = min(max_allowed_k, integer_param("max_k", max_allowed_k))
    if min_k > max_k:
        raise ValueError("Os parâmetros min_k e max_k não formam um intervalo válido.")

    elbow_values = []
    for cluster_count in range(min_k, max_k + 1):
        model = KMeans(n_clusters=cluster_count, n_init=10, random_state=random_state)
        model.fit(features)
        elbow_values.append({"k": cluster_count, "inertia": float(model.inertia_)})

    selected_k = integer_param("n_clusters", min(3, max_k))
    selected_k = max(min_k, min(selected_k, max_k))
    final_model = KMeans(n_clusters=selected_k, n_init=10, random_state=random_state)
    labels = final_model.fit_predict(features)

    result_df = df.copy()
    result_df["cluster"] = labels
    elbow_df = pd.DataFrame(elbow_values)
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=elbow_df["k"],
            y=elbow_df["inertia"],
            mode="lines+markers",
            name="Inércia",
        )
    )
    selected_inertia = float(final_model.inertia_)
    figure.add_trace(
        go.Scatter(
            x=[selected_k],
            y=[selected_inertia],
            mode="markers",
            marker={"size": 12, "color": "#e4572e"},
            name=f"K selecionado ({selected_k})",
        )
    )
    figure.update_layout(
        title="Método do Cotovelo",
        xaxis_title="Número de clusters (K)",
        yaxis_title="Inércia (within-cluster sum of squares)",
        template="plotly_white",
    )

    return {
        "title": "Tarefa 30 - K-Means & Método do Cotovelo",
        "description": (
            f"Dados numéricos imputados e padronizados; K-Means executado com "
            f"{selected_k} clusters e inércias calculadas para o gráfico do cotovelo."
        ),
        "metrics": {
            "Número de clusters": selected_k,
            "Inércia final": round(selected_inertia, 4),
            "Observações agrupadas": len(result_df),
            "Variáveis utilizadas": len(numeric_df.columns),
        },
        "tables": [result_df.to_html(classes="table table-striped", index=False)],
        "plots": [figure.to_json()],
    }
