# %%
import pandas as pd
import numpy as np
import os
# %%
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import silhouette_score as sil_score
from sklearn.metrics.pairwise import cosine_similarity
# %%

def import_data(file):
    df=pd.read_csv(file, header = 0)
    return df.to_numpy()

class cluster:
    def __init__(self, data, algo, **kwargs):
        self.algo = algo( **kwargs )
        self.data = data

    def fit(self, X):
        self.algo.fit(X)

    def transform(self, X): 
        lab = "label"
        while(lab in self.data.columns):
            lab = lab + str(np.random.randint(0, 9))
        self.data[lab] = self.algo.labels_
    
        return self.algo.labels_

    def pcp_plot(self, cols, names):
        pd.plotting.parallel_coordinates(self.data, cols, names)





if __name__ == "__main__":
# %%
    # some driver code to get kmeans classes for dash data
    data_df = pd.read_csv(os.path.join("dash_proto", "dash_data", "data.csv"))
    data_arr = data_df.drop(columns=["name", "id", "name_title"]).\
        replace({"%": ""}, regex=True).\
        to_numpy("float16")
    
    kmeans = KMeans(n_clusters=4)
    scaler = StandardScaler()

    labels = kmeans.fit_predict(scaler.fit_transform(data_arr))
    data_df["labels"] = labels

# %%
    data_df.to_csv(os.path.join("dash_proto", "dash_data", "data2.csv"), index=False)