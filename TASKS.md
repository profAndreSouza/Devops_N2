# 📚 Guia Oficial de Tarefas e Contribuição dos Alunos (37 Tarefas)

Bem-vindo à plataforma de **Ciência de Dados em Python (Devops N2)**! Este repositório foi construído com **Flask** para permitir que cada um dos **37 alunos da turma** desenvolva, teste e publique sua própria funcionalidade de Ciência de Dados de forma isolada e profissional.

---

## 🎯 Contrato de Código Obrigatório

Cada aluno é responsável por um único arquivo dentro do diretório `features/`.

Seu arquivo deve obrigatoriamente exportar a função `run_feature(df, params=None)`:

```python
def run_feature(df, params=None):
    """
    Entrada:
        - df (pandas.DataFrame): O conjunto de dados selecionado no portal web.
        - params (dict): Parâmetros opcionais enviados pelo formulário da página.

    Retorno (dict):
        {
            "title": "Título da sua Funcionalidade",
            "description": "Breve explicação do seu algoritmo de Ciência de Dados.",
            "metrics": {
                "Nome da Métrica 1": valor_1,
                "Nome da Métrica 2": valor_2
            },
            "tables": [df_resultado.to_html(classes="table table-striped")],
            "plots": [figura_plotly.to_json()]
        }
    """
```

---

## 📋 Tabela Oficial das 37 Tarefas Atribuídas aos Alunos

| ID | Aluno Responsável | Módulo | Arquivo Python | Descrição da Feature |
|---|---|---|---|---|
| **01** | Ahslam Mendes Monteiro Dias | Ingestão & Limpeza | `features/task_01_upload_schema.py` | Inspeção de Schema, Tipos de Dados e Validação de Nulos |
| **02** | Anthony Pais Dos Santos | Ingestão & Limpeza | `features/task_02_missing_values.py` | Imputação de Valores Ausentes (Média, Mediana, Moda, KNN) |
| **03** | Arthur Faria E Silva | Ingestão & Limpeza | `features/task_03_outliers.py` | Detecção e Filtro de Outliers (Z-Score & IQR) |
| **04** | Bianca Cirilo | Ingestão & Limpeza | `features/task_04_duplicates.py` | Remoção de Duplicadas e Formatador de Colunas |
| **05** | Edilaine Paulino Solde | Ingestão & Limpeza | `features/task_05_encoding.py` | Codificação Categórica (One-Hot & Label Encoding) |
| **06** | Enrico Emanuel Proenca Batista | EDA & Estatística | `features/task_06_summary_stats.py` | Tabela de Estatísticas Descritivas e Perfil do Dataset |
| **07** | Enzo Gabriel Tomas De Souza | EDA & Estatística | `features/task_07_correlation.py` | Matriz de Correlação Interativa (Pearson & Spearman) |
| **08** | Fabio Bitencourt Ribeiro | EDA & Estatística | `features/task_08_distributions.py` | Histogramas Interativos e Estimativa de Densidade KDE |
| **09** | Felipe Nunes Ramalho | EDA & Estatística | `features/task_09_boxplots.py` | Gráficos de Boxplot e Violin Plots Comparativos |
| **10** | Felipe Pinheiro Lopes | EDA & Estatística | `features/task_10_pairplot.py` | Matriz de Dispersão (Pairplot / Scatter Matrix) |
| **11** | Gabriel Camargo Gonçalves Silva | EDA & Estatística | `features/task_11_categorical_bars.py` | Análise de Frequência de Variáveis Categóricas |
| **12** | Guilherme Aparecido De Arruda Garcia | Engenharia de Features | `features/task_12_scaling.py` | Escalonamento de Features (Standard, MinMax, Robust) |
| **13** | Guilherme Bueno Caetano | Engenharia de Features | `features/task_13_feature_calculator.py` | Criador de Features por Expressões Matemáticas |
| **14** | Guilherme Lima Leite | Engenharia de Features | `features/task_14_polynomial_features.py` | Gerador de Atributos Polinomiais |
| **15** | Gustavo Henrique Gouveia Gomes | Engenharia de Features | `features/task_15_pca.py` | Redução de Dimensionalidade com PCA (2D & 3D) |
| **16** | Gustavo Leme De Castro | Engenharia de Features | `features/task_16_tsne.py` | Redução de Dimensionalidade Não-Linear com t-SNE |
| **17** | Gustavo Martinez Tucci | ML Classificação | `features/task_17_logistic_regression.py` | Regressão Logística & Análise de Odds Ratio |
| **18** | Henrique Gabriel Raz Antunes | ML Classificação | `features/task_18_decision_tree.py` | Árvore de Decisão Classifier e Exibição de Regras |
| **19** | Henrique Marchetti Coutinho | ML Classificação | `features/task_19_random_forest.py` | Random Forest Classifier & Importância de Atributos |
| **20** | Isabelly Caroline Martins Pardim | ML Classificação | `features/task_20_svm.py` | Support Vector Machine (SVM) Classifier |
| **21** | Jeniffer Camargo Oliveira | ML Classificação | `features/task_21_gradient_boosting.py` | Gradient Boosting Classifier |
| **22** | João Carlos Aparecido Dos Reis Junior | ML Regressão | `features/task_22_linear_regression.py` | Regressão Linear Simples/Múltipla & Regressão Ridge |
| **23** | João Victor Leite | ML Regressão | `features/task_23_rf_regressor.py` | Random Forest Regressor |
| **24** | Juliana Karla Camargo Da Silva | ML Regressão | `features/task_24_lasso_elasticnet.py` | Regressão Lasso e ElasticNet (Seleção de Atributos) |
| **25** | Letícia Vieira | ML Regressão | `features/task_25_polynomial_regression.py` | Ajuste de Curvas com Regressão Polinomial |
| **26** | Matheus Alves De Oliveira Souza | Diagnóstico & Métricas | `features/task_26_confusion_matrix.py` | Matriz de Confusão e Curva ROC / AUC |
| **27** | Matheus Henrique Koop Boff | Diagnóstico & Métricas | `features/task_27_cross_validation.py` | Validação Cruzada (K-Fold) e Curvas de Aprendizado |
| **28** | Nícolas Oliveira Carvalho Da Silva | Diagnóstico & Métricas | `features/task_28_regression_residuals.py` | Análise de Resíduos de Regressão (MSE, RMSE, MAE, R²) |
| **29** | Nicolas Pureza Da Silva | Diagnóstico & Métricas | `features/task_29_hyperparameter_tuning.py` | Simulador de Tuning de Hiperparâmetros (GridSearch) |
| **30** | Nicolle Carolina Da Rocha | Clustering | `features/task_30_kmeans.py` | Agrupamento K-Means e Gráfico do Cotovelo (Elbow) |
| **31** | Paulo Alberto Poppes Vieira | Clustering | `features/task_31_hierarchical_clustering.py` | Clustering Hierárquico e Dendrograma |
| **32** | Pedro Henrique Campos Do Carmo | Clustering | `features/task_32_dbscan.py` | Agrupamento DBSCAN e Detecção de Anomalias |
| **33** | Ronaldo Francisco Do Amaral Soares | Tópicos Especiais | `features/task_33_time_series_decomp.py` | Decomposição de Séries Temporais (Tendência/Sazonalidade) |
| **34** | Ryan Amorim Carvalho | Tópicos Especiais | `features/task_34_time_series_forecast.py` | Previsão de Séries Temporais (Exponential Smoothing) |
| **35** | Samuel David Cardia Rabisquim | Tópicos Especiais | `features/task_35_wordcloud.py` | Processamento de Texto e Gerador de Nuvem de Palavras |
| **36** | Vinícius Pereira De Souza | Tópicos Especiais | `features/task_36_sentiment_analysis.py` | Análise de Sentimento em Textos e Classificação |
| **37** | Vitor Fazano | Tópicos Especiais | `features/task_37_report_generator.py` | Gerador de Relatório Automatizado de Ciência de Dados |

---

## 🚀 Como Testar Localmente

1. Suba a aplicação via Docker Compose:
   ```bash
   docker-compose up --build
   ```
2. Ou via Python local:
   ```bash
   python app.py
   ```
3. Abra o navegador em `http://localhost:5000`
