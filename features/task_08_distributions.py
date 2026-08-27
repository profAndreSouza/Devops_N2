"""
Tarefa 08: Histogramas & Curvas KDE
Módulo: EDA & Estatística
Aluno Responsável: Fabio Bitencourt Ribeiro

Instruções para o Aluno (Fabio Bitencourt Ribeiro):
1. Utilize o DataFrame `df` recebido como parâmetro de entrada.
2. Objetivo: Gerar histogramas e estimativas de densidade de kernel (KDE) para variáveis numéricas.
3. Desenvolva sua lógica utilizando Python, Pandas, Scikit-learn, Plotly, etc.
4. Retorne um dicionário no formato exato:
   {
       "title": "Tarefa 08 - Histogramas & Curvas KDE",
       "description": "Explicação breve do que seu código realizou.",
       "metrics": {"Métrica 1": valor1, "Métrica 2": valor2},
       "tables": [df_resultado.to_html(classes="table table-striped")],
       "plots": [figura_plotly.to_json()]
   }
"""

def run_feature(df, params=None):
    params = params or {}
    
    # TODO (Fabio Bitencourt Ribeiro): Desenvolva aqui a lógica da sua funcionalidade.
    
    import pandas as pd
import numpy as np
import plotly.figure_factory as ff

def executar_tarefa_08(df: pd.DataFrame) -> dict:
    """
    Gera histogramas e curvas KDE para as variáveis numéricas de um DataFrame.
    Aluno Responsável: Fabio Bitencourt Ribeiro
    """
    
    # 1. Isolar variáveis numéricas
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not num_cols:
        return {
            "title": "Tarefa 08 - Histogramas & Curvas KDE",
            "description": "Nenhuma variável numérica foi encontrada no DataFrame fornecido.",
            "metrics": {"Variáveis Numéricas": 0},
            "tables": [],
            "plots": []
        }
    
    # Selecionar até as 4 primeiras colunas para manter o gráfico legível
    cols_to_plot = num_cols[:4]
    
    hist_data = []
    group_labels = []
    
    # 2. Preparar os dados removendo valores nulos (exigência do Plotly KDE)
    for col in cols_to_plot:
        dados_limpos = df[col].dropna()
        # O cálculo do KDE exige variância (múltiplos valores e não constantes)
        if len(dados_limpos) > 1 and dados_limpos.nunique() > 1:
            hist_data.append(dados_limpos.values)
            group_labels.append(col)
            
    plots_list = []
    
    # 3. Gerar a figura com Histograma + KDE
    if hist_data:
        # curve_type='kde' é o padrão, show_rug=False limpa um pouco a visualização
        fig = ff.create_distplot(hist_data, group_labels, show_hist=True, show_rug=False)
        fig.update_layout(
            title_text="Distribuição de Variáveis: Histograma + Curva KDE",
            template="plotly_white",
            legend_title="Variáveis"
        )
        plots_list.append(fig.to_json())
        
    # 4. Gerar DataFrame de resultados (Estatísticas Descritivas)
    df_resultado = df[cols_to_plot].describe().reset_index()
    df_resultado.rename(columns={'index': 'Métrica'}, inplace=True)
    
    # 5. Retornar dicionário no formato exato solicitado
    return {
        "title": "Tarefa 08 - Histogramas & Curvas KDE",
        "description": f"Análise de distribuição gerando Histogramas e curvas KDE para as variáveis: {', '.join(cols_to_plot)}. Inclui tabela de estatísticas descritivas.",
        "metrics": {
            "Total de Observações": len(df),
            "Variáveis Analisadas (KDE)": len(hist_data),
            "Valores Ausentes Ignorados": int(df[cols_to_plot].isna().sum().sum())
        },
        "tables": [df_resultado.to_html(classes="table table-striped", index=False)],
        "plots": plots_list
    }