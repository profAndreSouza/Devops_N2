def run_feature(df, params=None):
    import pandas as pd
    import plotly.graph_objects as go
    from sklearn.preprocessing import PolynomialFeatures

    params = params or {}

    # Configurações
    degree = params.get("degree", 2)
    include_bias = params.get("include_bias", False)

    # Seleciona apenas colunas numéricas
    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        return {
            "title": "Tarefa 14 - Gerador de Polynomial Features",
            "description": "Nenhuma coluna numérica encontrada no DataFrame.",
            "metrics": {
                "Features Originais": 0,
                "Features Geradas": 0
            },
            "tables": [],
            "plots": []
        }

    # Geração das features polinomiais
    poly = PolynomialFeatures(
        degree=degree,
        include_bias=include_bias
    )

    poly_array = poly.fit_transform(numeric_df)

    feature_names = poly.get_feature_names_out(numeric_df.columns)

    df_poly = pd.DataFrame(
        poly_array,
        columns=feature_names,
        index=df.index
    )

    # Prévia da tabela
    preview_df = df_poly.head(20)

    # Métricas
    original_features = numeric_df.shape[1]
    generated_features = df_poly.shape[1]
    new_features = generated_features - original_features

    # Gráfico Plotly
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Originais", "Geradas"],
            y=[original_features, generated_features],
            marker_color=["#1f77b4", "#ff7f0e"]
        )
    )

    fig.update_layout(
        title=f"Polynomial Features (grau={degree})",
        xaxis_title="Tipo",
        yaxis_title="Quantidade de Features",
        template="plotly_white"
    )

    return {
        "title": "Tarefa 14 - Gerador de Polynomial Features",
        "description": (
            f"Foram selecionadas {original_features} colunas numéricas e "
            f"geradas {generated_features} features polinomiais utilizando "
            f"PolynomialFeatures do Scikit-learn com grau {degree}."
        ),
        "metrics": {
            "Features Originais": int(original_features),
            "Features Geradas": int(generated_features),
            "Novas Features Criadas": int(new_features),
            "Grau Polinomial": int(degree)
        },
        "tables": [
            preview_df.to_html(
                classes="table table-striped",
                index=False
            )
        ],
        "plots": [
            fig.to_json()
        ]
    }