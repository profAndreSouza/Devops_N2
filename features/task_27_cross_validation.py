"""
Tarefa 27 - Validação Cruzada (K-Fold) e Curvas de Aprendizado
Aluno: Matheus Henrique Koop Boff
Módulo: Diagnóstico & Métricas

O que este módulo faz:
    1. Roda Validação Cruzada K-Fold (cross_val_score) para medir a
       estabilidade do modelo em várias divisões do dataset.
    2. Gera a Curva de Aprendizado (learning_curve) para ver como o
       desempenho de treino e validação evolui conforme mais dados
       de treino são usados (diagnóstico de overfitting/underfitting).

Contrato obrigatório do projeto:
    def run_feature(df, params=None) -> dict
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score, learning_curve
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler


def _guess_target_column(df):
    """Escolhe a coluna-alvo pelo nome mais comum, ou usa a última coluna."""
    common_names = ["Survived", "target", "class", "Class", "Species", "species"]
    for name in common_names:
        if name in df.columns:
            return name
    return df.columns[-1]


def _is_classification(y):
    """Poucos valores únicos (ou texto) => classificação; senão, regressão."""
    if y.dtype == object:
        return True
    return y.nunique(dropna=True) <= 10


def run_feature(df, params=None):
    """
    Executa Validação Cruzada K-Fold (k=5) e gera a Curva de Aprendizado
    para um modelo padrão (Regressão Logística para classificação,
    Regressão Linear para regressão).
    """
    params = params or {}

    try:
        # 1) Preparar dados
        target_col = params.get("target") or _guess_target_column(df)
        data = df.dropna(subset=[target_col]).copy()

        y_raw = data[target_col]
        is_clf = _is_classification(y_raw)
        y = pd.Series(LabelEncoder().fit_transform(y_raw.astype(str)), index=y_raw.index) \
            if is_clf and y_raw.dtype == object else y_raw

        X = data.drop(columns=[target_col]).select_dtypes(include=[np.number])
        X = X.fillna(X.mean(numeric_only=True))
        X_scaled = StandardScaler().fit_transform(X)

        # 2) Modelo e estratégia de K-Fold
        model = LogisticRegression(max_iter=1000) if is_clf else LinearRegression()
        scoring = "accuracy" if is_clf else "r2"
        k = 5
        cv = StratifiedKFold(n_splits=k, shuffle=True, random_state=42) if is_clf \
            else KFold(n_splits=k, shuffle=True, random_state=42)

        # 3) Validação Cruzada K-Fold
        fold_scores = cross_val_score(model, X_scaled, y, cv=cv, scoring=scoring)

        fold_table = pd.DataFrame({
            "Fold": [f"Fold {i + 1}" for i in range(k)],
            f"Score ({scoring})": np.round(fold_scores, 4)
        })

        fig_folds = go.Figure()
        fig_folds.add_trace(go.Bar(
            x=fold_table["Fold"], y=fold_table[f"Score ({scoring})"],
            marker_color="#4C9AFF", name="Score por Fold"
        ))
        fig_folds.add_hline(
            y=fold_scores.mean(), line_dash="dash", line_color="orange",
            annotation_text=f"Média: {fold_scores.mean():.3f}"
        )
        fig_folds.update_layout(
            title=f"Validação Cruzada K-Fold (k={k})",
            xaxis_title="Fold", yaxis_title=scoring.upper(), template="plotly_dark"
        )

        # 4) Curva de Aprendizado
        train_sizes, train_scores, val_scores = learning_curve(
            model, X_scaled, y, cv=cv, scoring=scoring,
            train_sizes=np.linspace(0.1, 1.0, 6), n_jobs=-1
        )
        train_mean = train_scores.mean(axis=1)
        val_mean = val_scores.mean(axis=1)

        fig_lc = go.Figure()
        fig_lc.add_trace(go.Scatter(
            x=train_sizes, y=train_mean, mode="lines+markers",
            name="Score de Treino", line=dict(color="#00C48C")
        ))
        fig_lc.add_trace(go.Scatter(
            x=train_sizes, y=val_mean, mode="lines+markers",
            name="Score de Validação", line=dict(color="#FF6B6B")
        ))
        fig_lc.update_layout(
            title="Curva de Aprendizado (Treino vs. Validação)",
            xaxis_title="Tamanho do conjunto de treino",
            yaxis_title=scoring.upper(), template="plotly_dark"
        )

        