"""
Tarefa 18: Árvore de Decisão Classifier
Módulo: ML Classificação
Aluno Responsável: Henrique Gabriel Raz Antunes

Instruções para o Aluno (Henrique Gabriel Raz Antunes):
1. Utilize o DataFrame `df` recebido como parâmetro de entrada.
2. Objetivo: Treinar uma Árvore de Decisão para classificação e extrair as regras de decisão.
3. Desenvolva sua lógica utilizando Python, Pandas, Scikit-learn, Plotly, etc.
4. Retorne um dicionário no formato exato:
   {
       "title": "Tarefa 18 - Árvore de Decisão Classifier",
       "description": "Explicação breve do que seu código realizou.",
       "metrics": {"Métrica 1": valor1, "Métrica 2": valor2},
       "tables": [df_resultado.to_html(classes="table table-striped")],
       "plots": [figura_plotly.to_json()]
   }
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import warnings

warnings.filterwarnings("ignore")


def preprocess_data(df, target_column=None):
    """Preprocessa o DataFrame: identifica target, codifica categóricas, trata nulos."""
    df = df.copy()
    
    if target_column is None:
        common_targets = ["survived", "target", "species", "class", "label", "classe", "target_class"]
        for col in df.columns:
            if col.lower() in common_targets:
                target_column = col
                break
        if target_column is None:
            for col in df.columns:
                if df[col].dtype == "object":
                    target_column = col
                    break
        if target_column is None:
            target_column = df.columns[-1]
    
    y = df[target_column]
    X = df.drop(columns=[target_column])
    
    for col in X.columns:
        if X[col].dtype == "object" or col.lower() in ["sex", "embarked", "pclass"]:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
    
    for col in X.columns:
        if X[col].isnull().any():
            X[col] = X[col].fillna(X[col].median())
    
    if y.dtype == "object":
        le_y = LabelEncoder()
        y = le_y.fit_transform(y)
    
    return X, y, target_column


def extract_tree_rules(tree, feature_names, class_names):
    """Extrai as regras de decisão da árvore."""
    tree_rules = export_text(tree, feature_names=feature_names)
    rules = []
    lines = tree_rules.split("\n")
    current_rule = []
    
    for line in lines:
        if not line.strip():
            continue
        text = line.strip()
        if text.startswith("class:"):
            class_name = text.replace("class:", "").strip()
            rules.append({
                "rule": " E ".join(current_rule) if current_rule else "raiz",
                "class": class_name
            })
            current_rule = []
        else:
            current_rule.append(text)
    
    return rules, tree_rules


def run_feature(df, params=None):
    params = params or {}
    
    target_column = params.get("target_column", None)
    max_depth = params.get("max_depth", 5)
    test_size = params.get("test_size", 0.2)
    random_state = params.get("random_state", 42)
    
    X, y, target_column = preprocess_data(df, target_column)
    
    if len(X.columns) == 0:
        return {
            "title": "Tarefa 18 - Árvore de Decisão Classifier",
            "description": "Não foi possível identificar colunas de features para treinamento.",
            "metrics": {"Status": "Erro: Sem features"},
            "tables": [],
            "plots": []
        }
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y if len(np.unique(y)) > 1 else None
    )
    
    model = DecisionTreeClassifier(
        max_depth=max_depth,
        random_state=random_state,
        criterion="gini"
    )
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
    
    class_names = [str(c) for c in np.unique(y)]
    feature_names = list(X.columns)
    
    rules, tree_rules_text = extract_tree_rules(model, feature_names, class_names)
    
    df_rules = pd.DataFrame(rules)
    if df_rules.empty:
        df_rules = pd.DataFrame({"rule": ["(árvore muito pequena - sem regras extraídas)"], "class": ["N/A"]})
    
    metrics = {
        "Acurácia": round(acc, 4),
        "Precisão": round(prec, 4),
        "Recall": round(rec, 4),
        "F1-Score": round(f1, 4),
        "Profundidade Máxima": max_depth,
        "Nº de Features": len(feature_names),
        "Aluno Responsável": "Henrique Gabriel Raz Antunes",
        "Status": "Implementado"
    }
    
    fig_importance = px.bar(
        x=feature_names,
        y=model.feature_importances_,
        labels={"x": "Feature", "y": "Importância"},
        title="Importância das Features (Decision Tree)",
        color=model.feature_importances_,
        color_continuous_scale="Blues"
    )
    fig_importance.update_layout(showlegend=False, height=450)
    
    cm = confusion_matrix(y_test, y_pred)
    fig_cm = px.imshow(
        cm,
        labels=dict(x="Predito", y="Real", color="Contagem"),
        x=class_names,
        y=class_names,
        text_auto=True,
        title="Matriz de Confusão",
        color_continuous_scale="Blues"
    )
    fig_cm.update_layout(height=450)
    
    return {
        "title": "Tarefa 18 - Árvore de Decisão Classifier",
        "description": (
            "Modelo de Árvore de Decisão treinado com scikit-learn. "
            f"Foram utilizadas {len(feature_names)} features e {len(X)} amostras. "
            f"Alvo (target): {target_column}. "
            f"Profundidade máxima configurada: {max_depth}. "
            f"Acurácia obtida: {acc:.2%}. "
            f"As regras de decisão extraídas estão disponíveis na tabela abaixo."
        ),
        "metrics": metrics,
        "tables": [df_rules.to_html(classes="table table-striped", index=False)],
        "plots": [fig_importance.to_json(), fig_cm.to_json()]
    }
