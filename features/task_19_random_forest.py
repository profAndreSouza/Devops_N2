"""
Tarefa 19: Random Forest & Feature Importance
Módulo: ML Classificação
Aluno Responsável: Henrique Marchetti Coutinho

Instruções para o Aluno (Henrique Marchetti Coutinho):
1. Utilize o DataFrame `df` recebido como parâmetro de entrada.
2. Objetivo: Treinar um modelo Random Forest Classifier e calcular a importância dos atributos.
3. Desenvolva sua lógica utilizando Python, Pandas, Scikit-learn, Plotly, etc.
4. Retorne um dicionário no formato exato:
   {
       "title": "Tarefa 19 - Random Forest & Feature Importance",
       "description": "Explicação breve do que seu código realizou.",
       "metrics": {"Métrica 1": valor1, "Métrica 2": valor2},
       "tables": [df_resultado.to_html(classes="table table-striped")],
       "plots": [figura_plotly.to_json()]
   }
"""

import pandas as pd
import plotly.express as px
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def _find_target_column(df, requested_target):
    if requested_target:
        if requested_target not in df.columns:
            raise ValueError(f"A coluna alvo '{requested_target}' não existe no DataFrame.")
        return requested_target

    for column in ("survived", "species", "target", "label", "class"):
        if column in df.columns:
            return column

    categorical_columns = df.select_dtypes(exclude="number").columns.tolist()
    if categorical_columns:
        return categorical_columns[-1]
    return df.columns[-1]

def run_feature(df, params=None):
    params = params or {}

    if not isinstance(df, pd.DataFrame) or df.empty:
        raise ValueError("O DataFrame de entrada não pode estar vazio.")

    target_column = _find_target_column(df, params.get("target_column"))
    working_df = df.dropna(subset=[target_column]).copy()
    target = working_df.pop(target_column)
    if target.nunique() < 2:
        raise ValueError("A coluna alvo precisa conter pelo menos duas classes.")

    feature_columns = working_df.columns.tolist()
    numeric_columns = working_df.select_dtypes(include="number").columns.tolist()
    categorical_columns = [
        column for column in feature_columns if column not in numeric_columns
    ]

    transformers = []
    if numeric_columns:
        transformers.append((
            "numeric",
            Pipeline([("imputer", SimpleImputer(strategy="median"))]),
            numeric_columns,
        ))
    if categorical_columns:
        transformers.append((
            "categorical",
            Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore")),
            ]),
            categorical_columns,
        ))
    if not transformers:
        raise ValueError("Não foram encontradas colunas preditoras válidas.")

    test_size = float(params.get("test_size", 0.2))
    if not 0 < test_size < 1:
        raise ValueError("test_size deve estar entre 0 e 1.")
    random_state = int(params.get("random_state", 42))
    n_estimators = int(params.get("n_estimators", 200))
    if n_estimators < 1:
        raise ValueError("n_estimators deve ser maior que zero.")

    class_counts = target.value_counts()
    stratify = target if class_counts.min() >= 2 else None
    if stratify is not None:
        test_count = max(1, int(len(target) * test_size))
        if test_count < target.nunique():
            test_size = target.nunique() / len(target)

    X_train, X_test, y_train, y_test = train_test_split(
        working_df,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )

    preprocessor = ColumnTransformer(transformers=transformers)
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
        class_weight="balanced",
    )
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", model),
    ])
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)

    feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
    importances = pipeline.named_steps["classifier"].feature_importances_
    importance_df = pd.DataFrame({
        "Atributo": feature_names,
        "Importância": importances,
    })
    importance_df["Atributo"] = importance_df["Atributo"].str.replace(
        r"^(numeric|categorical)__", "", regex=True
    )
    importance_df = (
        importance_df.groupby("Atributo", as_index=False)["Importância"]
        .sum()
        .sort_values("Importância", ascending=False)
        .reset_index(drop=True)
    )
    importance_df["Importância"] = importance_df["Importância"].round(6)

    top_importances = importance_df.head(20).sort_values("Importância")
    figure = px.bar(
        top_importances,
        x="Importância",
        y="Atributo",
        orientation="h",
        title="Importância dos atributos - Random Forest",
        labels={"Importância": "Importância", "Atributo": "Atributo"},
    )
    figure.update_layout(template="plotly_white")

    return {
        "title": "Tarefa 19 - Random Forest & Feature Importance",
        "description": (
            f"Random Forest treinado para prever '{target_column}' com "
            f"{len(importance_df)} atributos após o pré-processamento."
        ),
        "metrics": {
            "Acurácia": round(accuracy_score(y_test, predictions), 4),
            "Precisão (weighted)": round(
                precision_score(y_test, predictions, average="weighted", zero_division=0), 4
            ),
            "Recall (weighted)": round(
                recall_score(y_test, predictions, average="weighted", zero_division=0), 4
            ),
            "F1-Score (weighted)": round(
                f1_score(y_test, predictions, average="weighted", zero_division=0), 4
            ),
            "Árvore(s)": n_estimators,
            "Amostras de teste": len(y_test),
        },
        "tables": [importance_df.to_html(classes="table table-striped", index=False)],
        "plots": [figure.to_json()],
    }
