# %%
import pandas as pd
import numpy as np
# %%
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
from sklearn.decomposiiton import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import silhouette_score as sil_score

def import_data(file):
    df=pd.read_csv(file, header = 0)
    return df.to_numpy()

class cluster:
    def __init__(self, algo, **kwargs):
        self.algo = algo( **kwargs )

    def fit(self, X):
        self.algo.fit(X)

    def transform(self, X): 
        self.df = pd.DataFrame(X)
        return self.algo.labels_

    def pcp_plot(self, cols, names):
        pd.plotting.parallel_coordinates(df, cols, names)


if __name__ == "__main__":
