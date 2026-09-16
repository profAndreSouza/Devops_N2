"""
Tarefa 11: Frequência de Categoria & Barras
Módulo: EDA & Estatística
Aluno Responsável: Gabriel Camargo Gonçalves Silva

Instruções para o Aluno (Gabriel Camargo Gonçalves Silva):
1. Utilize o DataFrame `df` recebido como parâmetro de entrada.
2. Objetivo: Analisar frequências e proporções de variáveis categóricas em gráficos de barras.
3. Desenvolva sua lógica utilizando Python, Pandas, Scikit-learn, Plotly, etc.
4. Retorne um dicionário no formato exato:
   {
       "title": "Tarefa 11 - Frequência de Categoria & Barras",
       "description": "Explicação breve do que seu código realizou.",
       "metrics": {"Métrica 1": valor1, "Métrica 2": valor2},
       "tables": [df_resultado.to_html(classes="table table-striped")],
       "plots": [figura_plotly.to_json()]
   }
"""
import pandas as pd
import plotly.express as px

def run_feature(df, params=None):
    params = params or {}
    
    # Identifica a primeira coluna categórica ou de texto do DataFrame (fallback para a primeira coluna se não houver texto puro)
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    target_col = cat_cols[0] if len(cat_cols) > 0 else df.columns[0]
    
    # 1. Calcula a frequência absoluta e relativa (proporção) da categoria
    freq_abs = df[target_col].value_counts().reset_index()
    freq_abs.columns = ['Categoria', 'Frequencia_Absoluta']
    
    freq_rel = df[target_col].value_counts(normalize=True).reset_index()
    freq_rel.columns = ['Categoria', 'Proporcao']
    
    # Junta os dados em um único DataFrame de resultado
    df_resultado = pd.merge(freq_abs, freq_rel, on='Categoria')
    df_resultado['Proporcao'] = df_resultado['Proporcao'].round(4) # Arredonda para 4 casas decimais
    
    # 2. Cria o gráfico de barras interativo com Plotly
    fig = px.bar(
        df_resultado,
        x='Categoria',
        y='Frequencia_Absoluta',
        title=f'Frequência da Variável: {target_col}',
        labels={'Categoria': target_col, 'Frequencia_Absoluta': 'Frequência'},
        text='Frequencia_Absoluta'
    )
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(template='plotly_white')
    
    # 3. Define métricas úteis para o dicionário de retorno
    total_registros = len(df)
    categorias_unicas = df_resultado['Categoria'].nunique()
    
    metrics = {
        "Total de Registros": int(total_registros),
        "Categorias Únicas": int(categorias_unicas),
        "Coluna Analisada": str(target_col)
    }
    
    description = f"Análise exploratória da variável categórica '{target_col}', exibindo contagem absoluta e proporção relativa em formato tabular e gráfico de barras."

    return {
        "title": "Tarefa 11 - Frequência de Categoria & Barras",
        "description": description,
        "metrics": metrics,
        "tables": [df_resultado.to_html(classes="table table-striped", index=False)],
        "plots": [fig.to_json()]
    }
