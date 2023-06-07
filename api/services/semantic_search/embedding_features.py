import json

from sklearn.manifold import TSNE  # clustering
from sklearn.model_selection import train_test_split  # feature encoder for ML algorithms
from sklearn.metrics import mean_squared_error, mean_absolute_error  # Random forest
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier  # Random forest

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# embedding model parameters
EMBEDDING_STORAGE = "./api/services/semantic_search/data/embeddings_previous_features.json"


def embedded_features(filepath):
    """
    We assume the filepath is a csv with embeddings created
    """
    storage_key = filepath
    # Check if the query has been made before
    # with open(EMBEDDING_STORAGE, 'r') as f:
    #     previous_suggestions = json.load(f)
    #     if storage_key in previous_suggestions:
    #         print("Query has been made before, returning previous suggestion")
    #         return 200, previous_suggestions[storage_key]

    print("Query has not been made before, getting embedding")
    # If the query has not been made before, we need to get the embedding
    df = pd.read_csv(filepath)
    # _clustering(df)
    _ml_algorithms(df)
    # Ask the question
    res = 1,'str'
    # Save the emmbedding as follows: key = filepath+query, value = res
    # with open(EMBEDDING_STORAGE, 'r') as f:
    #     previous_suggestions = json.load(f)
    #     previous_suggestions[storage_key] = res
    # with open(EMBEDDING_STORAGE, 'w') as f:
    #     json.dump(previous_suggestions, f)

    return 200, res


def _clustering(df):
    print("-- create matrix")
    matrix = np.array(df.embedding.apply(eval).to_list())
    print("-- TSNE")
    tsne = TSNE(n_components=2, perplexity=15, random_state=42, init='random', learning_rate=200)
    print("-- vis dims")
    vis_dims = tsne.fit_transform(matrix)

    colors = ["red", "orange", "yellow", "lightgreen", "darkgreen"]
    x = [x for x,y in vis_dims]
    y = [y for x,y in vis_dims]
    color_indices = df.quality.values - 1

    colormap = matplotlib.colors.ListedColormap(colors)
    plt.scatter(x, y, c=color_indices, cmap=colormap, alpha=0.3)
    plt.title("Clustering the provided dataset using t-SNE")
    plt.legend()
    plt.savefig("./api/services/semantic_search/data/latest_clustering.png")


def _ml_algorithms(df):
    print("-- ML algorithms")
    print("-- train test split")
    df["embedding"] = df.embedding.apply(eval).apply(np.array)

    # Regression
    # x_train, x_test, y_train, y_test = train_test_split(
    #     list(df.embedding.values),
    #     df.quality,
    #     test_size = 0.2,
    #     random_state=42
    # )

    # rfr = RandomForestRegressor(n_estimators=100)
    # rfr.fit(x_train, y_train)
    # preds = rfr.predict(x_test)
    # mse = mean_squared_error(y_test, preds)
    # mae = mean_absolute_error(y_test, preds)
    # print(f"Regression: embedding regression performance on wine quality scores: mse={mse:.2f}, mae={mae:.2f}")

    # from openai.embeddings_utils import plot_multiclass_precision_recall
    # rfc = RandomForestClassifier(n_estimators=100)
    # rfc.fit(x_train, y_train)
    # probas = rfc.predict_proba(x_test)
    # with Capturing() as output:
    #     plot_multiclass_precision_recall(probas, y_test, [3,4,5,6,7,8], rfc)
    # print(f"Classifier: {output[0]}")

    # # Train a logistic regression model
    # from sklearn.preprocessing import StandardScaler
    # from sklearn.linear_model import LogisticRegression
    # from sklearn.metrics import classification_report
    # scaler = StandardScaler()
    # X_train = scaler.fit_transform(X_train)
    # X_test = scaler.transform(X_test)
    # lr = LogisticRegression()
    # lr.fit(X_train, y_train)
    # y_pred = lr.predict(X_test)
    # print(classification_report(y_test, y_pred))

    import seaborn as sns
    sns.countplot(x='quality', data=df)
    plt.savefig("./api/services/semantic_search/data/latest_countplot.png")

    sns.heatmap(df.corr(), cmap='coolwarm')
    plt.savefig("./api/services/semantic_search/data/latest_heatmap.png")

    df.hist(bins=10, figsize=(20, 15))
    plt.tight_layout()
    plt.savefig("./api/services/semantic_search/data/latest_histogram.png")

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='volatile acidity', y='alcohol', hue='quality', data=df)
    plt.savefig("./api/services/semantic_search/data/latest_scatterplot.png")
    


# Tool to capture the output, used in this case to capture internal plot output
from io import StringIO 
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
