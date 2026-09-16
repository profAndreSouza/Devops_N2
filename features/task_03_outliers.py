"""
Tarefa 03: Detecção e Filtro de Outliers
Módulo: Ingestão & Limpeza
Aluno Responsável: Arthur Faria E Silva

Instruções para o Aluno (Arthur Faria E Silva):
1. Utilize o DataFrame `df` recebido como parâmetro de entrada.
2. Objetivo: Detectar e filtrar outliers estatísticos utilizando Z-Score e Intervalo Interquartil (IQR).
3. Desenvolva sua lógica utilizando Python, Pandas, Scikit-learn, Plotly, etc.
4. Retorne um dicionário no formato exato:
   {
       "title": "Tarefa 03 - Detecção e Filtro de Outliers",
       "description": "Explicação breve do que seu código realizou.",
       "metrics": {"Métrica 1": valor1, "Métrica 2": valor2},
       "tables": [df_resultado.to_html(classes="table table-striped")],
       "plots": [figura_plotly.to_json()]
   }
"""

def run_feature(df, params=None):
    params = params or {}
    
    # TODO : Implementar a lógica de detecção e filtro de outliers utilizando Z-Score e IQR.

    Q1 = df['nome_da_coluna'].quantile(0.25)
    Q3 = df['nome_da_coluna'].quantile(0.75)
    IQR = Q3 - Q1

    # Definindo os limites
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

# Filtrando e mostrando apenas os outliers
    outliers = df[(df['nome_da_coluna'] < limite_inferior) | (df['nome_da_coluna'] > limite_superior)]
    print(outliers)

    
    return {
        "title": "Tarefa 03 - Detecção e Filtro de Outliers",
        "description": "Atividade aguardando implementação pelo(a) aluno(a) Arthur Faria E Silva.",
        "metrics": {
            "Aluno Responsável": "Arthur Faria E Silva",
            "Status": "Pendente de Implementação"
        },
        "tables": [],
        "plots": []
    }
