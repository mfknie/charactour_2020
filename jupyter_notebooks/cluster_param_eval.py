from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
import numpy as np
import pandas as pd

# code from https://stackoverflow.com/questions/34611038/grid-search-for-hyperparameter-evaluation-of-clustering-in-scikit-learn
def make_generator(parameters):
    if not parameters:
        yield dict()
    else:
        key_to_iterate = list(parameters.keys())[0]
        next_round_parameters = {p : parameters[p]
                    for p in parameters if p != key_to_iterate}
        for val in parameters[key_to_iterate]:
            for pars in make_generator(next_round_parameters):
                temp_res = pars
                temp_res[key_to_iterate] = val
                yield temp_res


def eval_params(X, params, algo):
    '''
    Evaluate different parameters for cluster algorithm
    Input:
    sizes - dictionary with a single "n_clusters" key, with the value being a list of # of n_clusters
    X - training data to run clusterer
    Output:
    Dataframe with performance metrics listed for each set of algorithm parameters.
    '''
    metrics = {"n_clusters": [], "sil_score": [], "inertia": []}
    for p in make_generator(params):
        cluster = algo( **p) #, n_init = 20)
        cluster.fit(X)
        for k, v in p.items():
            metrics[k].append(v)
        metrics["sil_score"].append(silhouette_score(X, cluster.labels_))
        metrics["inertia"].append(cluster.inertia_)
    return pd.DataFrame.from_dict(metrics)