import pandas as pd
import numpy as np
from sklearn.datasets import load_iris, load_wine, fetch_california_housing

def get_available_datasets():
    return {
        "titanic": "Titanic - Sobrevivência de Passageiros (Classificação / Limpeza)",
        "iris": "Iris - Flores e Espécies (EDA / Classificação)",
        "housing": "California Housing - Preços de Imóveis (Regressão)",
        "wine": "Wine - Variedades e Propriedades Químicas (Clustering / PCA)",
        "synthetic_ts": "Série Temporal Sintética - Vendas e Demandas (Séries Temporais)",
        "synthetic_text": "Textos Sintéticos - Avaliações de Produtos (NLP / Sentimento)"
    }

def load_dataset(name="titanic"):
    name = str(name).lower()
    
    if name == "iris":
        iris = load_iris(as_frame=True)
        df = iris.frame
        df.columns = [col.replace(" (cm)", "").replace(" ", "_") for col in df.columns]
        df.rename(columns={"target": "species"}, inplace=True)
        species_map = {0: "setosa", 1: "versicolor", 2: "virginica"}
        df["species"] = df["species"].map(species_map)
        return df

    elif name == "wine":
        wine = load_wine(as_frame=True)
        df = wine.frame
        df.columns = [col.replace("/", "_").replace(" ", "_") for col in df.columns]
        return df

    elif name == "housing":
        housing = fetch_california_housing(as_frame=True)
        df = housing.frame.head(500)  # Limitar a 500 para performance rápida
        df.columns = [col.replace(" ", "_") for col in df.columns]
        return df

    elif name == "synthetic_ts":
        dates = pd.date_range(start="2024-01-01", periods=180, freq="D")
        np.random.seed(42)
        trend = np.linspace(100, 300, 180)
        seasonality = 30 * np.sin(np.linspace(0, 6 * np.pi, 180))
        noise = np.random.normal(0, 10, 180)
        vendas = trend + seasonality + noise
        df = pd.DataFrame({"data": dates, "vendas": np.round(vendas, 2), "desconto": np.random.choice([0, 5, 10, 15], 180)})
        return df

    elif name == "synthetic_text":
        data = {
            "review_id": range(1, 16),
            "texto": [
                "Excelente produto! A entrega foi super rápida e o funcionamento é perfeito.",
                "Péssima qualidade, quebrou no primeiro dia de uso. Não recomendo.",
                "Produto razoável pelo preço, mas o acabamento deixa a desejar.",
                "Sensacional! Superou todas as minhas expectativas, comprarei novamente.",
                "Muito ruim, o suporte ao cliente não respondeu e veio com defeito.",
                "Gostei muito, atende perfeitamente ao que promete.",
                "Horrível! Dinheiro jogado fora, nunca mais compro nesta loja.",
                "Ótimo custo benefício, fácil de usar e muito prático.",
                "Regular. Nada demais, funciona quando quer.",
                "Maravilhoso! Design incrível e altíssima performance.",
                "Decepcionante, a embalagem veio rasgada e faltaram peças.",
                "Muito bom! Chegou antes do prazo e funciona direitinho.",
                "Fraco. Material muito frágil e sem instruções claras.",
                "Recomendo a todos! Qualidade impecável.",
                "Péssimo atendimento e produto de baixa qualidade."
            ],
            "categoria": ["Eletrônicos", "Eletrônicos", "Moda", "Eletrônicos", "Casa", "Moda", "Casa", "Eletrônicos", "Moda", "Eletrônicos", "Casa", "Moda", "Casa", "Eletrônicos", "Casa"]
        }
        return pd.DataFrame(data)

    else:
        # Default Titanic Dataset
        np.random.seed(42)
        n = 200
        pclass = np.random.choice([1, 2, 3], n, p=[0.25, 0.25, 0.5])
        sex = np.random.choice(["male", "female"], n, p=[0.6, 0.4])
        age = np.random.choice([np.nan, 22, 38, 26, 35, 54, 2, 27, 14, 4, 58, 20, 39], n)
        fare = np.round(np.random.exponential(35, n) + 5, 2)
        embarked = np.random.choice(["S", "C", "Q", None], n, p=[0.7, 0.2, 0.05, 0.05])
        survived = np.random.choice([0, 1], n, p=[0.6, 0.4])
        
        df = pd.DataFrame({
            "passenger_id": range(1, n + 1),
            "survived": survived,
            "pclass": pclass,
            "sex": sex,
            "age": age,
            "fare": fare,
            "embarked": embarked
        })
        return df
