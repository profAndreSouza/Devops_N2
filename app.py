import os
import importlib
from flask import Flask, render_template, request, jsonify, send_file
from utils.data_loader import get_available_datasets, load_dataset

app = Flask(__name__)

# Definir as 37 tarefas com metadados
TASKS_METADATA = [
    {"id": 1, "filename": "task_01_upload_schema", "title": "Inspeção de Schema & Tipos de Dados", "student": "Aluno 01", "module": "Ingestão & Limpeza", "description": "Validação de schema, identificação de tipos primitivos e contagem de nulos."},
    {"id": 2, "filename": "task_02_missing_values", "title": "Tratamento de Valores Ausentes", "student": "Aluno 02", "module": "Ingestão & Limpeza", "description": "Imputação de valores nulos utilizando Média, Mediana, Moda e KNN Imputer."},
    {"id": 3, "filename": "task_03_outliers", "title": "Detecção e Filtro de Outliers", "student": "Aluno 03", "module": "Ingestão & Limpeza", "description": "Identificação de anomalias estatísticas via Z-Score e Intervalo Interquartil (IQR)."},
    {"id": 4, "filename": "task_04_duplicates", "title": "Limpeza de Duplicadas e Formatador", "student": "Aluno 04", "module": "Ingestão & Limpeza", "description": "Remoção de registros duplicados e padronização de nomenclatura de colunas."},
    {"id": 5, "filename": "task_05_encoding", "title": "Codificação Categórica (One-Hot & Label)", "student": "Aluno 05", "module": "Ingestão & Limpeza", "description": "Transformação de variáveis textuais/categóricas para codificação numérica."},
    {"id": 6, "filename": "task_06_summary_stats", "title": "Estatísticas Descritivas & Perfil", "student": "Aluno 06", "module": "EDA & Estatística", "description": "Métricas de tendência central, dispersão, assimetria e curtose."},
    {"id": 7, "filename": "task_07_correlation", "title": "Matriz de Correlação Interativa", "student": "Aluno 07", "module": "EDA & Estatística", "description": "Heatmap interativo de correlação de Pearson e Spearman entre variáveis."},
    {"id": 8, "filename": "task_08_distributions", "title": "Histogramas & Curvas KDE", "student": "Aluno 08", "module": "EDA & Estatística", "description": "Visualização de distribuições empíricas e estimativa de densidade de kernel."},
    {"id": 9, "filename": "task_09_boxplots", "title": "Boxplots & Violin Plots Comparativos", "student": "Aluno 09", "module": "EDA & Estatística", "description": "Comparação de quartis e densidade entre diferentes grupos e categorias."},
    {"id": 10, "filename": "task_10_pairplot", "title": "Matriz de Dispersão (Pairplot)", "student": "Aluno 10", "module": "EDA & Estatística", "description": "Dispersão cruzada multivariada para análise de relacionamentos entre pares."},
    {"id": 11, "filename": "task_11_categorical_bars", "title": "Frequência de Categoria & Barras", "student": "Aluno 11", "module": "EDA & Estatística", "description": "Contagem de frequência e proporção de categorias em gráficos de barra."},
    {"id": 12, "filename": "task_12_scaling", "title": "Escalonamento de Features (Scaler)", "student": "Aluno 12", "module": "Engenharia de Features", "description": "Normalização e padronização (StandardScaler, MinMaxScaler, RobustScaler)."},
    {"id": 13, "filename": "task_13_feature_calculator", "title": "Calculadora de Novas Features", "student": "Aluno 13", "module": "Engenharia de Features", "description": "Criação de novos atributos a partir de operações aritméticas entre colunas."},
    {"id": 14, "filename": "task_14_polynomial_features", "title": "Gerador de Polynomial Features", "student": "Aluno 14", "module": "Engenharia de Features", "description": "Geração de interações e potências polinomiais para capturar não-linearidades."},
    {"id": 15, "filename": "task_15_pca", "title": "PCA (Componentes Principais)", "student": "Aluno 15", "module": "Engenharia de Features", "description": "Redução de dimensionalidade linear preservando a variância explicada."},
    {"id": 16, "filename": "task_16_tsne", "title": "Redução de Dimensionalidade (t-SNE)", "student": "Aluno 16", "module": "Engenharia de Features", "description": "Projeção de alta dimensão em espaço 2D/3D para visualização de clusters."},
    {"id": 17, "filename": "task_17_logistic_regression", "title": "Regressão Logística & Odds Ratio", "student": "Aluno 17", "module": "ML Classificação", "description": "Modelo linear de classificação probabilística e cálculo de razão de chances."},
    {"id": 18, "filename": "task_18_decision_tree", "title": "Árvore de Decisão Classifier", "student": "Aluno 18", "module": "ML Classificação", "description": "Classificador baseado em regras de decisão e partição de entropia/Gini."},
    {"id": 19, "filename": "task_19_random_forest", "title": "Random Forest & Feature Importance", "student": "Aluno 19", "module": "ML Classificação", "description": "Ensemble de árvores e ranqueamento de importância de variáveis."},
    {"id": 20, "filename": "task_20_svm", "title": "Support Vector Machine (SVM)", "student": "Aluno 20", "module": "ML Classificação", "description": "Classificação por hiperplano de margem máxima e truque de kernel."},
    {"id": 21, "filename": "task_21_gradient_boosting", "title": "Gradient Boosting Classifier", "student": "Aluno 21", "module": "ML Classificação", "description": "Algoritmo de boosting sequencial de árvores para alta acurácia."},
    {"id": 22, "filename": "task_22_linear_regression", "title": "Regressão Linear & Ridge", "student": "Aluno 22", "module": "ML Regressão", "description": "Modelagem de valor contínuo e regularização L2 contra overfitting."},
    {"id": 23, "filename": "task_23_rf_regressor", "title": "Random Forest Regressor", "student": "Aluno 23", "module": "ML Regressão", "description": "Estimador ensemble para previsão de variáveis numéricas contínuas."},
    {"id": 24, "filename": "task_24_lasso_elasticnet", "title": "Regressão Lasso & ElasticNet", "student": "Aluno 24", "module": "ML Regressão", "description": "Regularização L1/L2 com seleção automática de variáveis irrelevantes."},
    {"id": 25, "filename": "task_25_polynomial_regression", "title": "Ajuste de Regressão Polinomial", "student": "Aluno 25", "module": "ML Regressão", "description": "Ajuste de curvas de tendência não-lineares em conjuntos de dados."},
    {"id": 26, "filename": "task_26_confusion_matrix", "title": "Matriz de Confusão & Curva ROC", "student": "Aluno 26", "module": "Diagnóstico & Métricas", "description": "Métricas de Precision, Recall, F1-Score, Matriz de Confusão e AUC-ROC."},
    {"id": 27, "filename": "task_27_cross_validation", "title": "Validação Cruzada & Learning Curve", "student": "Aluno 27", "module": "Diagnóstico & Métricas", "description": "Avaliação K-Fold e análise do viés vs variância do modelo."},
    {"id": 28, "filename": "task_28_regression_residuals", "title": "Análise de Resíduos & Métricas R²", "student": "Aluno 28", "module": "Diagnóstico & Métricas", "description": "Gráficos de resíduos vs ajustados, cálculo de MSE, RMSE, MAE e R²."},
    {"id": 29, "filename": "task_29_hyperparameter_tuning", "title": "Tuning de Hiperparâmetros", "student": "Aluno 29", "module": "Diagnóstico & Métricas", "description": "Simulação de busca em grade (GridSearch) para otimização de parâmetros."},
    {"id": 30, "filename": "task_30_kmeans", "title": "K-Means & Método do Cotovelo", "student": "Aluno 30", "module": "Clustering", "description": "Particionamento em K grupos e determinação do K ideal pelo gráfico Elbow."},
    {"id": 31, "filename": "task_31_hierarchical_clustering", "title": "Clustering Hierárquico", "student": "Aluno 31", "module": "Clustering", "description": "Agrupamento aglomerativo e análise gráfica através de Dendrograma."},
    {"id": 32, "filename": "task_32_dbscan", "title": "DBSCAN & Anomalias", "student": "Aluno 32", "module": "Clustering", "description": "Agrupamento por densidade espacial e identificação de ruídos/outliers."},
    {"id": 33, "filename": "task_33_time_series_decomp", "title": "Decomposição de Séries Temporais", "student": "Aluno 33", "module": "Tópicos Especiais", "description": "Isolamento de tendência, sazonalidade e resíduos em dados temporais."},
    {"id": 34, "filename": "task_34_time_series_forecast", "title": "Previsão de Séries Temporais", "student": "Aluno 34", "module": "Tópicos Especiais", "description": "Modelos de suavização exponencial e projeção de demanda futura."},
    {"id": 35, "filename": "task_35_wordcloud", "title": "Nuvem de Palavras (WordCloud)", "student": "Aluno 35", "module": "Tópicos Especiais", "description": "Extração de frequência de termos em textos e geração gráfica da nuvem."},
    {"id": 36, "filename": "task_36_sentiment_analysis", "title": "Análise de Sentimento em Texto", "student": "Aluno 36", "module": "Tópicos Especiais", "description": "Classificação de polaridade (Positivo, Neutro, Negativo) em avaliações."},
    {"id": 37, "filename": "task_37_report_generator", "title": "Gerador de Relatórios Automatizado", "student": "Aluno 37", "module": "Tópicos Especiais", "description": "Compilação automatizada dos achados em relatório executivo de dados."}
]

def load_student_feature(task_info, df, params=None):
    """Carrega dinamicamente a função run_feature do módulo do aluno."""
    filename = task_info["filename"]
    try:
        module = importlib.import_module(f"features.{filename}")
        if hasattr(module, "run_feature"):
            return module.run_feature(df, params)
        else:
            return {
                "title": task_info["title"],
                "description": "Função run_feature não encontrada no módulo.",
                "metrics": {"Erro": "Não implementado"},
                "tables": [], "plots": []
            }
    except Exception as e:
        return {
            "title": task_info["title"],
            "description": f"Erro de execução no módulo do aluno: {str(e)}",
            "metrics": {"Status": "Erro de Execução"},
            "tables": [], "plots": []
        }

@app.route("/")
def index():
    selected_dataset = request.args.get("dataset", "titanic")
    datasets = get_available_datasets()
    df = load_dataset(selected_dataset)
    
    return render_template(
        "index.html",
        tasks_list=TASKS_METADATA,
        datasets=datasets,
        selected_dataset=selected_dataset,
        dataset_rows=len(df)
    )

@app.route("/tasks")
def public_tasks():
    """Página Pública das 37 Tarefas dos Alunos com especificações técnicas e repositório."""
    return render_template("tasks_public.html", tasks_list=TASKS_METADATA)

@app.route("/task/<int:task_id>")
def run_task_page(task_id):
    task_info = next((t for t in TASKS_METADATA if t["id"] == task_id), None)
    if not task_info:
        return "Tarefa não encontrada", 404
        
    selected_dataset = request.args.get("dataset", "titanic")
    if task_id in [35, 36]:  # tarefas de NLP usam texto por padrão
        selected_dataset = request.args.get("dataset", "synthetic_text")
    elif task_id in [33, 34]:  # tarefas de Séries Temporais usam dataset temporal
        selected_dataset = request.args.get("dataset", "synthetic_ts")
        
    datasets = get_available_datasets()
    df = load_dataset(selected_dataset)
    
    # Executar código do aluno
    result = load_student_feature(task_info, df)
    
    return render_template(
        "task_detail.html",
        task_info=task_info,
        result=result,
        datasets=datasets,
        selected_dataset=selected_dataset
    )

@app.route("/doc/tasks")
def view_tasks_doc():
    """Download/Visualização do documento TASKS.md público."""
    tasks_md_path = os.path.join(app.root_path, "TASKS.md")
    if os.path.exists(tasks_md_path):
        return send_file(tasks_md_path, mimetype="text/markdown")
    return "Documento TASKS.md não encontrado.", 404

@app.route("/api/run-task/<int:task_id>", methods=["POST"])
def api_run_task(task_id):
    """API Endpoint para execução remota da tarefa via JSON."""
    task_info = next((t for t in TASKS_METADATA if t["id"] == task_id), None)
    if not task_info:
        return jsonify({"error": "Tarefa não encontrada"}), 404
        
    data = request.json or {}
    dataset_name = data.get("dataset", "titanic")
    params = data.get("params", {})
    
    df = load_dataset(dataset_name)
    result = load_student_feature(task_info, df, params)
    
    return jsonify(result)

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    app.run(host=host, port=port, debug=True)
