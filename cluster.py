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

def run_kmeans():
    
        
if __name__ == "__main__":
