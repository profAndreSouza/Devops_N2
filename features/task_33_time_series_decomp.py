import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose


def run_feature(df, params=None):
    """
    Tarefa 33: Decomposição de Séries Temporais
    Aluno Responsável: Aluno 33

    Realiza a decomposição de uma série temporal em:
    - Tendência
    - Sazonalidade
    - Resíduos
    """

    params = params or {}

    # ---------------------------------------------------------
    # 1. Validação inicial
    # ---------------------------------------------------------

    if df is None or df.empty:
        return {
            "title": "Tarefa 33 - Decomposição de Séries Temporais",
            "description": "Não foi possível realizar a decomposição porque o DataFrame está vazio.",
            "metrics": {
                "Linhas Processadas": 0,
                "Colunas Disponíveis": 0,
                "Status": "Sem dados"
            },
            "tables": [],
            "plots": []
        }

    # Cria uma cópia para não alterar o DataFrame original
    data = df.copy()

    # ---------------------------------------------------------
    # 2. Identificar coluna temporal
    # ---------------------------------------------------------

    date_col = params.get("date_column")

    if date_col and date_col in data.columns:
        data[date_col] = pd.to_datetime(
            data[date_col],
            errors="coerce"
        )
    else:
        # Procura automaticamente uma coluna de data
        date_col = None

        for coluna in data.columns:
            coluna_convertida = pd.to_datetime(
                data[coluna],
                errors="coerce"
            )

            # Considera coluna temporal se a maioria dos valores
            # puder ser convertida para data
            if coluna_convertida.notna().mean() >= 0.7:
                date_col = coluna
                data[coluna] = coluna_convertida
                break

    # ---------------------------------------------------------
    # 3. Identificar coluna numérica
    # ---------------------------------------------------------

    numeric_cols = list(
        data.select_dtypes(include=["number"]).columns
    )

    value_col = params.get("value_column")

    if value_col and value_col in numeric_cols:
        pass
    elif numeric_cols:
        value_col = numeric_cols[0]
    else:
        value_col = None

    # ---------------------------------------------------------
    # 4. Criar tabela resumo
    # ---------------------------------------------------------

    summary_df = (
        data.describe()
        .T
        .reset_index()
        .round(2)
        if numeric_cols
        else data.head(10)
    )

    # ---------------------------------------------------------
    # 5. Verificar se existem dados suficientes
    # ---------------------------------------------------------

    if date_col is None:
        fig = px.bar(
            data.head(10),
            x=data.columns[0],
            title="Dados - Coluna temporal não identificada"
        )

        return {
            "title": "Tarefa 33 - Decomposição de Séries Temporais",
            "description": (
                "Não foi possível realizar a decomposição porque "
                "nenhuma coluna temporal foi identificada."
            ),
            "metrics": {
                "Linhas Processadas": len(data),
                "Colunas Disponíveis": len(data.columns),
                "Status": "Coluna temporal não encontrada"
            },
            "tables": [
                summary_df.head(10).to_html(
                    classes="table table-hover table-striped table-sm",
                    index=False
                )
            ],
            "plots": [fig.to_json()]
        }

    if value_col is None:
        fig = px.bar(
            data.head(10),
            x=date_col,
            title="Dados - Coluna numérica não identificada"
        )

        return {
            "title": "Tarefa 33 - Decomposição de Séries Temporais",
            "description": (
                "Não foi possível realizar a decomposição porque "
                "nenhuma coluna numérica foi identificada."
            ),
            "metrics": {
                "Linhas Processadas": len(data),
                "Colunas Disponíveis": len(data.columns),
                "Status": "Coluna numérica não encontrada"
            },
            "tables": [
                summary_df.head(10).to_html(
                    classes="table table-hover table-striped table-sm",
                    index=False
                )
            ],
            "plots": [fig.to_json()]
        }

    # ---------------------------------------------------------
    # 6. Preparar série temporal
    # ---------------------------------------------------------

    serie = data[[date_col, value_col]].copy()

    serie[date_col] = pd.to_datetime(
        serie[date_col],
        errors="coerce"
    )

    serie[value_col] = pd.to_numeric(
        serie[value_col],
        errors="coerce"
    )

    serie = serie.dropna()

    # Ordena cronologicamente
    serie = serie.sort_values(date_col)

    # Remove datas duplicadas calculando a média
    serie = (
        serie
        .groupby(date_col, as_index=False)[value_col]
        .mean()
    )

    # Define a data como índice
    serie = serie.set_index(date_col)

    # ---------------------------------------------------------
    # 7. Detectar período da sazonalidade
    # ---------------------------------------------------------

    period = params.get("period")

    if period is None:
        # Tenta inferir uma frequência
        frequencia = pd.infer_freq(serie.index)

        if frequencia:
            frequencia_upper = frequencia.upper()

            if "H" in frequencia_upper:
                period = 24
            elif "D" in frequencia_upper:
                period = 7
            elif "W" in frequencia_upper:
                period = 52
            elif "M" in frequencia_upper:
                period = 12
            elif "Q" in frequencia_upper:
                period = 4
            elif "Y" in frequencia_upper:
                period = 1
            else:
                period = 12
        else:
            # Valor padrão
            period = 12

    period = int(period)

    # ---------------------------------------------------------
    # 8. Verificar quantidade mínima de observações
    # ---------------------------------------------------------

    minimo_observacoes = period * 2

    if len(serie) < minimo_observacoes:
        fig = px.line(
            serie.reset_index(),
            x=date_col,
            y=value_col,
            title=f"Série Temporal - {value_col}"
        )

        return {
            "title": "Tarefa 33 - Decomposição de Séries Temporais",
            "description": (
                f"Não há observações suficientes para realizar a "
                f"decomposição com período {period}. "
                f"São necessárias pelo menos {minimo_observacoes} "
                f"observações."
            ),
            "metrics": {
                "Linhas Processadas": len(data),
                "Colunas Disponíveis": len(data.columns),
                "Observações da Série": len(serie),
                "Período": period,
                "Status": "Dados insuficientes"
            },
            "tables": [
                summary_df.head(10).to_html(
                    classes="table table-hover table-striped table-sm",
                    index=False
                )
            ],
            "plots": [fig.to_json()]
        }

    # ---------------------------------------------------------
    # 9. Realizar decomposição
    # ---------------------------------------------------------

    try:
        resultado = seasonal_decompose(
            serie[value_col],
            model=params.get("model", "additive"),
            period=period,
            extrapolate_trend="freq"
        )

    except Exception as erro:
        fig = px.line(
            serie.reset_index(),
            x=date_col,
            y=value_col,
            title=f"Série Temporal - {value_col}"
        )

        return {
            "title": "Tarefa 33 - Decomposição de Séries Temporais",
            "description": (
                f"Erro ao realizar a decomposição: {str(erro)}"
            ),
            "metrics": {
                "Linhas Processadas": len(data),
                "Colunas Disponíveis": len(data.columns),
                "Status": "Erro na decomposição"
            },
            "tables": [
                summary_df.head(10).to_html(
                    classes="table table-hover table-striped table-sm",
                    index=False
                )
            ],
            "plots": [fig.to_json()]
        }

    # ---------------------------------------------------------
    # 10. Criar DataFrame da decomposição
    # ---------------------------------------------------------

    decomposicao_df = pd.DataFrame({
        "data": resultado.observed.index,
        "observado": resultado.observed.values,
        "tendencia": resultado.trend.values,
        "sazonalidade": resultado.seasonal.values,
        "residuo": resultado.resid.values
    })

    # ---------------------------------------------------------
    # 11. Gráfico da série original
    # ---------------------------------------------------------

    fig_original = px.line(
        decomposicao_df,
        x="data",
        y="observado",
        title=f"Série Temporal Original - {value_col}"
    )

    fig_original.update_layout(
        xaxis_title="Data",
        yaxis_title=value_col
    )

    # ---------------------------------------------------------
    # 12. Gráfico da tendência
    # ---------------------------------------------------------

    fig_tendencia = px.line(
        decomposicao_df,
        x="data",
        y="tendencia",
        title="Tendência da Série Temporal"
    )

    fig_tendencia.update_layout(
        xaxis_title="Data",
        yaxis_title="Tendência"
    )

    # ---------------------------------------------------------
    # 13. Gráfico da sazonalidade
    # ---------------------------------------------------------

    fig_sazonalidade = px.line(
        decomposicao_df,
        x="data",
        y="sazonalidade",
        title="Sazonalidade da Série Temporal"
    )

    fig_sazonalidade.update_layout(
        xaxis_title="Data",
        yaxis_title="Sazonalidade"
    )

    # ---------------------------------------------------------
    # 14. Gráfico dos resíduos
    # ---------------------------------------------------------

    fig_residuos = px.line(
        decomposicao_df,
        x="data",
        y="residuo",
        title="Resíduos da Série Temporal"
    )

    fig_residuos.update_layout(
        xaxis_title="Data",
        yaxis_title="Resíduo"
    )

    # ---------------------------------------------------------
    # 15. Tabela da decomposição
    # ---------------------------------------------------------

    tabela_decomposicao = decomposicao_df.tail(20).round(4)

    # ---------------------------------------------------------
    # 16. Métricas
    # ---------------------------------------------------------

    residuo_validos = decomposicao_df["residuo"].dropna()

    media_residuo = (
        float(residuo_validos.mean())
        if len(residuo_validos) > 0
        else 0
    )

    desvio_residuo = (
        float(residuo_validos.std())
        if len(residuo_validos) > 0
        else 0
    )

    return {
        "title": "Tarefa 33 - Decomposição de Séries Temporais",

        "description": (
            f"Decomposição da série temporal '{value_col}' "
            f"utilizando a coluna temporal '{date_col}'. "
            f"A série foi dividida em tendência, sazonalidade "
            f"e resíduos."
        ),

        "metrics": {
            "Linhas Processadas": len(data),
            "Colunas Disponíveis": len(data.columns),
            "Observações da Série": len(serie),
            "Coluna Temporal": date_col,
            "Coluna Analisada": value_col,
            "Período Sazonal": period,
            "Modelo": params.get("model", "additive"),
            "Média dos Resíduos": round(media_residuo, 4),
            "Desvio dos Resíduos": round(desvio_residuo, 4),
            "Status": "Ativo / Operacional"
        },

        "tables": [
            summary_df.head(10).to_html(
                classes="table table-hover table-striped table-sm",
                index=False
            ),

            tabela_decomposicao.to_html(
                classes="table table-hover table-striped table-sm",
                index=False
            )
        ],

        "plots": [
            fig_original.to_json(),
            fig_tendencia.to_json(),
            fig_sazonalidade.to_json(),
            fig_residuos.to_json()
        ]
    }