"""
Tarefa 23: Random Forest Regressor
Módulo: ML Regressão
Aluno Responsável: João Victor Leite

Instruções para o Aluno (João Victor Leite):
1. Utilize o DataFrame `df` recebido como parâmetro de entrada.
2. Objetivo: Treinar um modelo de Random Forest Regressor para prever variáveis contínuas.
3. Desenvolva sua lógica utilizando Python, Pandas, Scikit-learn, Plotly, etc.
4. Retorne um dicionário no formato exato:
   {
       "title": "Tarefa 23 - Random Forest Regressor",
       "description": "Explicação breve do que seu código realizou.",
       "metrics": {"Métrica 1": valor1, "Métrica 2": valor2},
       "tables": [df_resultado.to_html(classes="table table-striped")],
       "plots": [figura_plotly.to_json()]
   }
"""

def run_feature(df, params=None):
    params = params or {}
    
    # TODO (João Victor Leite): Desenvolva aqui a lógica da sua funcionalidade.
    
    return {
        "title": "Tarefa 23 - Random Forest Regressor",
        "description": "Atividade concluída com implementação pelo(a) aluno(a) João Victor Leite.",
        "metrics": {
            "Aluno Responsável": "João Victor Leite",
            "Status": "Concluído"
        },
        "tables": [],
        "plots": []
    }


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import plotly.express as px


def tarefa_23(df: pd.DataFrame, target_col: str = None, random_state: int = 42):
    """
    Treina um Random Forest Regressor para prever uma variável contínua.

    Parâmetros:
        df (pd.DataFrame): DataFrame de entrada.
        target_col (str): nome da coluna alvo. Se None, usa a última coluna.
        random_state (int): seed para reprodutibilidade.

    Retorna:
        dict no formato esperado pela plataforma.
    """
    df = df.copy()

    # 1. Define a coluna alvo
    if target_col is None:
        target_col = df.columns[-1]

    # 2. Separa features e target
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # 3. Codifica colunas categóricas automaticamente (se houver)
    for col in X.select_dtypes(include=["object", "category"]).columns:
        X[col] = LabelEncoder().fit_transform(X[col].astype(str))

    # 4. Remove linhas com valores nulos (abordagem simples)
    X = X.fillna(X.median(numeric_only=True))
    y = y.fillna(y.median())

    # 5. Split treino/teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )

    # 6. Treina o modelo
    modelo = RandomForestRegressor(
        n_estimators=200,
        max_depth=None,
        random_state=random_state,
        n_jobs=-1
    )
    modelo.fit(X_train, y_train)

    # 7. Previsões e métricas
    y_pred = modelo.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    # 8. Tabela de resultados (real vs previsto)
    df_resultado = pd.DataFrame({
        "Valor Real": y_test.values,
        "Valor Previsto": np.round(y_pred, 2)
    }).reset_index(drop=True)

    # 9. Gráfico: real vs previsto
    fig = px.scatter(
        df_resultado,
        x="Valor Real",
        y="Valor Previsto",
        title="Random Forest Regressor - Valores Reais vs Previstos",
        trendline="ols"
    )
    fig.add_shape(
        type="line",
        x0=df_resultado["Valor Real"].min(),
        y0=df_resultado["Valor Real"].min(),
        x1=df_resultado["Valor Real"].max(),
        y1=df_resultado["Valor Real"].max(),
        line=dict(dash="dash", color="gray")
    )

    # 10. Importância das features (opcional, útil para análise)
    importancias = pd.Series(
        modelo.feature_importances_, index=X.columns
    ).sort_values(ascending=False)

    resultado = {
        "title": "Tarefa 23 - Random Forest Regressor",
        "description": (
            f"Modelo Random Forest Regressor treinado para prever '{target_col}'. "
            f"Foram utilizadas {X.shape[1]} variáveis preditoras, com divisão "
            f"80/20 entre treino e teste. A variável mais importante para o "
            f"modelo foi '{importancias.index[0]}'."
        ),
        "metrics": {
            "R²": round(r2, 4),
            "MAE": round(mae, 4),
            "RMSE": round(rmse, 4)
        },
        "tables": [df_resultado.to_html(classes="table table-striped")],
        "plots": [fig.to_json()]
    }

    return resultado

    