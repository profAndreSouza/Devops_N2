"""
Tarefa 28: Análise de Resíduos & Métricas R²
Módulo: Diagnóstico & Métricas
Aluno Responsável: Nícolas Oliveira Carvalho Da Silva

Instruções para o Aluno (Nícolas Oliveira Carvalho Da Silva):
1. Utilize o DataFrame `df` recebido como parâmetro de entrada.
2. Objetivo: Calcular resíduos de regressão e métricas MSE, RMSE, MAE e R².
3. Desenvolva sua lógica utilizando Python, Pandas, Scikit-learn, Plotly, etc.
4. Retorne um dicionário no formato exato:
   {
       "title": "Tarefa 28 - Análise de Resíduos & Métricas R²",
       "description": "Explicação breve do que seu código realizou.",
       "metrics": {"Métrica 1": valor1, "Métrica 2": valor2},
       "tables": [df_resultado.to_html(classes="table table-striped")],
       "plots": [figura_plotly.to_json()]
   }
"""

import base64
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    explained_variance_score
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


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


def _detect_target_and_features(df, params):
    """Identifica automaticamente ou extrai dos parâmetros as variáveis alvo (y) e preditoras (X)."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Remover colunas típicas de ID
    id_like = [c for c in numeric_cols if c.lower().endswith("id") or c.lower() in ["id", "index", "row_id"]]
    candidate_cols = [c for c in numeric_cols if c not in id_like]
    
    if len(candidate_cols) < 2:
        return None, None, "São necessárias pelo menos 2 variáveis numéricas (1 alvo + 1 preditora)."
    
    # Verificar parâmetro de target enviado
    target_col = params.get("target_col") or params.get("target")
    if target_col not in candidate_cols:
        # Tentar correspondência automática com nomes comuns de target
        known_targets = ["fare", "vendas", "medhouseval", "target", "price", "preço", "valor", "desconto", "age"]
        matched = [c for c in candidate_cols if c.lower() in known_targets]
        if matched:
            target_col = matched[0]
        else:
            target_col = candidate_cols[-1]
            
    # Selecionar variáveis preditoras (X)
    feature_cols = params.get("feature_cols")
    if isinstance(feature_cols, str):
        feature_cols = [f.strip() for f in feature_cols.split(",") if f.strip() in candidate_cols]
    if not feature_cols:
        feature_cols = [c for c in candidate_cols if c != target_col]
        
    if not feature_cols:
        return None, None, "Nenhuma variável preditora válida foi encontrada."
        
    return target_col, feature_cols, None


def run_feature(df, params=None):
    params = params or {}
    
    # 1. Identificação das variáveis Target (y) e Features (X)
    target_col, feature_cols, err_msg = _detect_target_and_features(df, params)
    
    if err_msg:
        return {
            "title": "Tarefa 28 - Análise de Resíduos & Métricas R²",
            "description": f"Erro na seleção de dados: {err_msg}",
            "metrics": {
                "Aluno Responsável": "Nícolas Oliveira Carvalho Da Silva",
                "Status": "Erro de Dados Insuficientes"
            },
            "tables": [],
            "plots": []
        }
        
    # 2. Limpeza e preparação do dataset
    work_df = df[[target_col] + feature_cols].dropna()
    
    if len(work_df) < 10:
        return {
            "title": "Tarefa 28 - Análise de Resíduos & Métricas R²",
            "description": "O conjunto de dados possui menos de 10 observações válidas sem valores ausentes.",
            "metrics": {
                "Aluno Responsável": "Nícolas Oliveira Carvalho Da Silva",
                "Observações Válidas": len(work_df),
                "Status": "Amostra insuficiente para Regressão"
            },
            "tables": [],
            "plots": []
        }
        
    X = work_df[feature_cols]
    y = work_df[target_col]
    
    # 3. Divisão Treino / Teste (ou uso completo para amostras pequenas)
    if len(work_df) >= 30:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42
        )
    else:
        X_train, X_test, y_train, y_test = X, X, y, y
        
    # 4. Normalização das features e Treinamento do Modelo
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model_type = params.get("model_type", "LinearRegression")
    if model_type == "Ridge":
        model = Ridge(alpha=1.0)
    elif model_type == "RandomForest":
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    else:
        model = LinearRegression()
        
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    # 5. Cálculo dos Resíduos e Métricas de Regressão
    residuals = y_test - y_pred
    n = len(y_test)
    p = X_test.shape[1]
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # R² Ajustado
    if n > p + 1:
        adj_r2 = 1.0 - ((1.0 - r2) * (n - 1) / (n - p - 1))
    else:
        adj_r2 = r2
        
    exp_var = explained_variance_score(y_test, y_pred)
    max_err = float(np.max(np.abs(residuals)))
    mean_res = float(np.mean(residuals))
    std_res = float(np.std(residuals))
    
    metrics_summary = {
        "Aluno Responsável": "Nícolas Oliveira Carvalho Da Silva",
        "Variável Alvo (y)": target_col,
        "Qtd Features (X)": len(feature_cols),
        "Amostras (Teste)": n,
        "MSE (Erro Quadrático)": round(float(mse), 4),
        "RMSE (Raiz do MSE)": round(float(rmse), 4),
        "MAE (Erro Absoluto)": round(float(mae), 4),
        "R² Score": round(float(r2), 4),
        "R² Ajustado": round(float(adj_r2), 4)
    }
    
    # 6. Criação dos Gráficos Interativos em Plotly
    plots = []
    
    # Gráfico 1: Resíduos vs Valores Ajustados (Residuals vs Fitted)
    df_res_plot = pd.DataFrame({
        "Ajustados": y_pred,
        "Resíduos": residuals
    })
    
    fig_res_fitted = px.scatter(
        df_res_plot,
        x="Ajustados",
        y="Resíduos",
        title="1. Resíduos vs Valores Ajustados (Residuals vs Fitted)",
        labels={"Ajustados": "Valores Previstos (ŷ)", "Resíduos": "Resíduos (y - ŷ)"}
    )
    
    # Tendência polinomial dos resíduos via numpy
    if len(y_pred) > 3:
        sort_idx = np.argsort(y_pred)
        x_sorted = y_pred[sort_idx]
        y_res_sorted = residuals.values[sort_idx] if hasattr(residuals, 'values') else residuals[sort_idx]
        z = np.polyfit(x_sorted, y_res_sorted, deg=min(2, len(x_sorted) - 1))
        p_poly = np.poly1d(z)
        fig_res_fitted.add_trace(
            go.Scatter(
                x=x_sorted,
                y=p_poly(x_sorted),
                mode="lines",
                name="Tendência dos Resíduos",
                line=dict(color="#FFD166", width=2)
            )
        )
    
    # Adicionar linha horizontal y = 0
    fig_res_fitted.add_hline(
        y=0, line_dash="dash", line_color="#EF476F", annotation_text="Resíduo Zero", annotation_position="top left"
    )
    fig_res_fitted.update_traces(marker=dict(size=8, opacity=0.8, color="#4CC9F0"), selector=dict(mode='markers'))
    fig_res_fitted.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E9ECEF"),
        autosize=True,
        margin=dict(l=60, r=40, t=60, b=40)
    )
    plots.append(_fig_to_plain_json(fig_res_fitted))
    
    # Gráfico 2: Valores Reais vs Previstos (Actual vs Predicted)
    df_act_pred = pd.DataFrame({
        "Real": y_test,
        "Previsto": y_pred
    })
    
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    
    fig_act_pred = px.scatter(
        df_act_pred,
        x="Real",
        y="Previsto",
        title="2. Valores Reais vs Previstos (Linha Ideal y = x)",
        labels={"Real": "Valores Reais (y)", "Previsto": "Valores Previstos (ŷ)"}
    )
    # Adicionar linha de identidade perfeita (y = x)
    fig_act_pred.add_shape(
        type="line",
        x0=min_val, y0=min_val, x1=max_val, y1=max_val,
        line=dict(color="#06D6A0", width=2, dash="dash")
    )
    fig_act_pred.update_traces(marker=dict(size=8, opacity=0.8, color="#118AB2"))
    fig_act_pred.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E9ECEF"),
        autosize=True,
        margin=dict(l=60, r=40, t=60, b=40)
    )
    plots.append(_fig_to_plain_json(fig_act_pred))
    
    # Gráfico 3: Distribuição dos Resíduos (Histograma)
    fig_dist = px.histogram(
        residuals,
        nbins=25,
        title="3. Distribuição de Frequência dos Resíduos (Avaliação de Normalidade)",
        labels={"value": "Resíduo (y - ŷ)", "count": "Frequência"},
        marginal="box",
        color_discrete_sequence=["#06D6A0"]
    )
    fig_dist.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E9ECEF"),
        autosize=True,
        margin=dict(l=60, r=40, t=60, b=40),
        showlegend=False
    )
    plots.append(_fig_to_plain_json(fig_dist))
    
    # 7. Construção das Tabelas de Resultados
    # Tabela 1: Resumo Detalhado das Métricas
    metrics_table_df = pd.DataFrame([
        {"Métrica": "R² Score (Coeficiente de Determinação)", "Valor": f"{r2:.4f}", "Interpretabilidade": "Proporção da variância total explicada pelo modelo (0 a 1)."},
        {"Métrica": "R² Ajustado", "Valor": f"{adj_r2:.4f}", "Interpretabilidade": "R² ajustado pelo número de preditores no modelo."},
        {"Métrica": "RMSE (Raiz do Erro Quadrático Médio)", "Valor": f"{rmse:.4f}", "Interpretabilidade": "Desvio padrão dos resíduos na mesma unidade de y."},
        {"Métrica": "MAE (Erro Absoluto Médio)", "Valor": f"{mae:.4f}", "Interpretabilidade": "Média das magnitudes absolutas dos erros."},
        {"Métrica": "MSE (Erro Quadrático Médio)", "Valor": f"{mse:.4f}", "Interpretabilidade": "Média dos erros ao quadrado (penaliza grandes desvios)."},
        {"Métrica": "Variância Explicada", "Valor": f"{exp_var:.4f}", "Interpretabilidade": "Proporção de variabilidade capturada pelas previsões."},
        {"Métrica": "Maior Erro Absoluto (Max Error)", "Valor": f"{max_err:.4f}", "Interpretabilidade": "Maior discrepância pontual entre real e previsto."},
        {"Métrica": "Média dos Resíduos (Bias)", "Valor": f"{mean_res:.4f}", "Interpretabilidade": "Próximo de zero indica ausência de viés sistemático."},
        {"Métrica": "Desvio Padrão dos Resíduos", "Valor": f"{std_res:.4f}", "Interpretabilidade": "Variabilidade da dispersão dos resíduos em torno de zero."}
    ])
    
    # Tabela 2: Amostra da Tabela de Resíduos (Primeiras 15 linhas)
    y_test_vals = y_test.values if hasattr(y_test, 'values') else y_test
    res_vals = residuals.values if hasattr(residuals, 'values') else residuals
    
    sample_df = pd.DataFrame({
        "Valor Real (y)": np.round(y_test_vals[:15], 2),
        "Valor Previsto (ŷ)": np.round(y_pred[:15], 2),
        "Resíduo (e = y - ŷ)": np.round(res_vals[:15], 2),
        "Erro Absoluto (%)": np.round(np.abs(res_vals[:15] / np.where(y_test_vals[:15] == 0, 1e-5, y_test_vals[:15])) * 100, 2)
    })
    
    tables = [
        metrics_table_df.to_html(classes="table table-striped table-dark table-hover align-middle", index=False),
        sample_df.to_html(classes="table table-striped table-dark table-hover align-middle", index=False)
    ]
    
    description = (
        f"Análise diagnóstica de resíduos e cálculo de métricas de ajuste de regressão para a variável alvo '{target_col}' "
        f"utilizando {len(feature_cols)} variáveis preditoras ({', '.join(feature_cols[:4])}{'...' if len(feature_cols) > 4 else ''}). "
        f"O modelo atingiu um Coeficiente de Determinação R² = {r2:.4f} e RMSE = {rmse:.4f}. "
        f"Foram gerados gráficos de Resíduos vs Valores Ajustados (para diagnosticar heterocedasticidade), "
        f"Valores Reais vs Previstos e a Distribuição de Frequência dos Resíduos para avaliar a suposição de normalidade."
    )
    
    return {
        "title": "Tarefa 28 - Análise de Resíduos & Métricas R²",
        "description": description,
        "metrics": metrics_summary,
        "tables": tables,
        "plots": plots
    }
