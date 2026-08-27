"""
Tarefa 24: Regressão Lasso & ElasticNet
Módulo: ML Regressão
Aluno Responsável: Juliana Karla Camargo Da Silva

Instruções para o Aluno (Juliana Karla Camargo Da Silva):
1. Utilize o DataFrame `df` recebido como parâmetro de entrada.
2. Objetivo: Treinar Regressão Lasso / ElasticNet para seleção de variáveis com regularização.
3. Desenvolva sua lógica utilizando Python, Pandas, Scikit-learn, Plotly, etc.
4. Retorne um dicionário no formato exato:
    {
        "title": "Tarefa 24 - Regressão Lasso & ElasticNet",
        "description": "Explicação breve do que seu código realizou.",
        "metrics": {"Métrica 1": valor1, "Métrica 2": valor2},
        "tables": [df_resultado.to_html(classes="table table-striped")],
        "plots": [figura_plotly.to_json()]
    }
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso, ElasticNet
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def run_feature(df, params=None):
    params = params or {}

    df_work = df.copy()

    numeric_cols = df_work.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) < 2:
        return {
            "title": "Tarefa 24 - Regressão Lasso & ElasticNet",
            "description": "Dataset não possui colunas numéricas suficientes para regressão.",
            "metrics": {"Erro": "Colunas numéricas insuficientes"},
            "tables": [],
            "plots": []
        }

    target_col = numeric_cols[-1]
    feature_cols = [c for c in numeric_cols if c != target_col]

    X = df_work[feature_cols]
    y = df_work[target_col]

    X = X.fillna(X.mean())
    y = y.fillna(y.mean())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    lasso_alpha = params.get("lasso_alpha", 0.1)
    elastic_alpha = params.get("elastic_alpha", 0.1)
    elastic_l1_ratio = params.get("elastic_l1_ratio", 0.5)

    lasso = Lasso(alpha=lasso_alpha, max_iter=10000, random_state=42)
    lasso.fit(X_train_scaled, y_train)

    elastic = ElasticNet(alpha=elastic_alpha, l1_ratio=elastic_l1_ratio, max_iter=10000, random_state=42)
    elastic.fit(X_train_scaled, y_train)

    lasso_coefs = pd.Series(lasso.coef_, index=feature_cols)
    elastic_coefs = pd.Series(elastic.coef_, index=feature_cols)

    lasso_selected = lasso_coefs[lasso_coefs != 0].index.tolist()
    elastic_selected = elastic_coefs[elastic_coefs != 0].index.tolist()

    selected_features = sorted(set(lasso_selected + elastic_selected))
    if not selected_features:
        selected_features = feature_cols.copy()

    lasso_pred = lasso.predict(X_test_scaled)
    elastic_pred = elastic.predict(X_test_scaled)

    lasso_r2 = r2_score(y_test, lasso_pred)
    lasso_mae = mean_absolute_error(y_test, lasso_pred)
    lasso_mse = mean_squared_error(y_test, lasso_pred)
    lasso_rmse = np.sqrt(lasso_mse)

    elastic_r2 = r2_score(y_test, elastic_pred)
    elastic_mae = mean_absolute_error(y_test, elastic_pred)
    elastic_mse = mean_squared_error(y_test, elastic_pred)
    elastic_rmse = np.sqrt(elastic_mse)

    df_coef = pd.DataFrame({
        "Variavel": feature_cols,
        "Lasso": lasso_coefs.values,
        "ElasticNet": elastic_coefs.values,
        "Selecionada_Lasso": [col in lasso_selected for col in feature_cols],
        "Selecionada_ElasticNet": [col in elastic_selected for col in feature_cols],
    })

    df_coef = df_coef.sort_values("Lasso", key=abs, ascending=False).reset_index(drop=True)

    df_metrics = pd.DataFrame({
        "Modelo": ["Lasso", "ElasticNet"],
        "R2": [lasso_r2, elastic_r2],
        "MAE": [lasso_mae, elastic_mae],
        "MSE": [lasso_mse, elastic_mse],
        "RMSE": [lasso_rmse, elastic_rmse],
        "Variaveis_Selecionadas": [len(lasso_selected), len(elastic_selected)],
        "Alpha": [lasso_alpha, elastic_alpha],
        "L1_Ratio": ["N/A", elastic_l1_ratio],
    })

    df_selected = pd.DataFrame({
        "Variavel_Selecionada": selected_features,
        "Lasso_Ativa": [col in lasso_selected for col in selected_features],
        "ElasticNet_Ativa": [col in elastic_selected for col in selected_features],
    })

    plot_data = df_coef.melt(
        id_vars="Variavel",
        value_vars=["Lasso", "ElasticNet"],
        var_name="Modelo",
        value_name="Coeficiente"
    )
    plot_data = plot_data[plot_data["Variavel"].isin(selected_features)]

    fig1 = px.bar(
        plot_data,
        x="Coeficiente",
        y="Variavel",
        color="Modelo",
        barmode="group",
        orientation="h",
        title="Coeficientes das Variaveis Selecionadas - Lasso vs ElasticNet",
        labels={"Coeficiente": "Valor do Coeficiente (padronizado)", "Variavel": "Variavel"},
        category_orders={"Variavel": selected_features[::-1]}
    )

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=y_test, y=lasso_pred, mode="markers", name="Lasso", marker=dict(color="blue")))
    fig2.add_trace(go.Scatter(x=y_test, y=elastic_pred, mode="markers", name="ElasticNet", marker=dict(color="red")))
    min_val = min(y_test.min(), lasso_pred.min(), elastic_pred.min())
    max_val = max(y_test.max(), lasso_pred.max(), elastic_pred.max())
    fig2.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val], mode="lines", name="Ideal", line=dict(dash="dash", color="gray")))
    fig2.update_layout(
        title="Valores Reais vs Preditos - Lasso & ElasticNet",
        xaxis_title="Valor Real",
        yaxis_title="Valor Predito",
        legend=dict(x=0.02, y=0.98)
    )

    fig3 = px.bar(
        df_metrics.melt(id_vars="Modelo", value_vars=["R2", "MAE", "MSE", "RMSE"], var_name="Metrica", value_name="Valor"),
        x="Metrica",
        y="Valor",
        color="Modelo",
        barmode="group",
        title="Comparacao de Metricas - Lasso vs ElasticNet"
    )

    figs = [fig1, fig2, fig3]

    description = (
        f"Selecao de variaveis com Lasso e ElasticNet aplicados sobre {len(feature_cols)} variaveis numericas. "
        f"Variavel alvo: '{target_col}'. "
        f"Lasso selecionou {len(lasso_selected)} variaveis e ElasticNet selecionou {len(elastic_selected)} variaveis. "
        f"Lasso R2: {lasso_r2:.4f}, ElasticNet R2: {elastic_r2:.4f}."
    )

    return {
        "title": "Tarefa 24 - Regressao Lasso & ElasticNet",
        "description": description,
        "metrics": {
            "Lasso_R2": round(float(lasso_r2), 6),
            "Lasso_MAE": round(float(lasso_mae), 6),
            "Lasso_RMSE": round(float(lasso_rmse), 6),
            "ElasticNet_R2": round(float(elastic_r2), 6),
            "ElasticNet_MAE": round(float(elastic_mae), 6),
            "ElasticNet_RMSE": round(float(elastic_rmse), 6),
            "Variaveis_Selecionadas_Lasso": int(len(lasso_selected)),
            "Variaveis_Selecionadas_ElasticNet": int(len(elastic_selected)),
            "Variavel_Alvo": target_col,
        },
        "tables": [
            df_coef.to_html(classes="table table-striped", index=False),
            df_metrics.to_html(classes="table table-striped", index=False),
            df_selected.to_html(classes="table table-striped", index=False),
        ],
        "plots": [fig.to_json() for fig in figs],
    }