import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
from sklearn.decomposiiton import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import silhouette_score as sil_score

def import_data(file):
    df=pd.read_csv(file, header = 0)
    return df.to_numpy()


def kmeans_clusters(X, n_clusters = None):
    # Adapted from:
    # https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html#sphx-glr-auto-examples-cluster-plot-kmeans-silhouette-analysis-py
    if(not n_clusters):
        n_clusters = [5, 10, 14, 15, 16]
    results = cluster.cv_results_
    data = pd.DataFrame(results)
    print(data[["params", "mean_train_score", "mean_test_score"]])
    for size in n_clusters:
        # Create a subplot with 1 row and 2 columns
        fig, ax1 = plt.subplots(1)
        fig.set_size_inches(18, 7)

        ax1.set_xlim([-0.1, 1])
        ax1.set_ylim([0, len(X) + (sizes + 1) * 10])

        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = clusterer.fit_predict(X)

        silhouette_avg = silhouette_score(X, cluster_labels)
        print("For ", n_clusters,
            " clusters, the average silhouette_score is :", silhouette_avg)

        sample_silhouette_values = silhouette_samples(X, cluster_labels)

        y_lower = 10
        for i in range(size):
            ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i].sort()
            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = cm.nipy_spectral(float(i) / n_clusters)
            ax1.fill_betweenx(np.arange(y_lower, y_upper),
                            0, ith_cluster_silhouette_values,
                            facecolor=color, edgecolor=color, alpha=0.7)

            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
            y_lower = y_upper + 10  
        
        ax1.set_title("The silhouette plot for the various clusters.")
        ax1.set_xlabel("The silhouette coefficient values")
        ax1.set_ylabel("Cluster labels")

        # The vertical line for average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="b-")

        ax1.set_yticks([])  # Clear the yaxis labels / ticks
        ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

        plt.suptitle(("KMeans on sample data "
                    "with n_clusters = {:d}".format(n_clusters)),
                    fontsize=20, fontweight='bold')
        
# Basic PCA, data processing stuff here
def find_pcs(data):
    scaled_data = StandardScaler().fit_transform(data)
    pca = PCA(n_components=0.95)
    pca.fit(data)
    components = pd.DataFrame(pca.components_, columns = cols) 
    components["var_explained"] = pca.explained_variance_ratio_
    return components
    
if __name__ == "__main__":
