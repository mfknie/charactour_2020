# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %%
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import silhouette_score, silhouette_samples

def import_data(file):
    df=pd.read_csv(file, header = 0)
    return df.to_numpy()


def kmeans_n_sil_plot(X, n_clusters = None):
    # Adapted from:
    # https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html#sphx-glr-auto-examples-cluster-plot-kmeans-silhouette-analysis-py
    if(not n_clusters):
        n_clusters = [5, 10, 14, 15, 16]
    for size in n_clusters:
        fig, ax1 = plt.subplots(1)
        fig.set_size_inches(18, 10)

        ax1.set_xlim([-0.1, 1])
        ax1.set_ylim([0, len(X) + (size + 1) * 10])

        kmeans = KMeans(n_clusters=size, random_state = 42)
        cluster_labels = kmeans.fit_predict(X)

        silhouette_avg = silhouette_score(X, cluster_labels)
        print("For ", n_clusters,
            " clusters, the average silhouette_score is :", silhouette_avg)

        sample_sil_values = silhouette_samples(X, cluster_labels)

        y_lower = 10
        for i in range(size):
            ith_cluster_sil_values = np.sort(sample_sil_values[cluster_labels == i])
            size_cluster_i = ith_cluster_sil_values.shape[0]
            y_upper = y_lower + size_cluster_i

            plt.nipy_spectral()
            ax1.fill_betweenx(y = np.arange(y_lower, y_upper),
                            x1 = 0, x2 = ith_cluster_sil_values, 
                            facecolor=color, edgecolor=color, alpha=0.7)

            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
            y_lower = y_upper + 10  
        
        ax1.set_title("The silhouette plot for the various clusters.")
        ax1.set_xlabel("The silhouette coefficient values")
        ax1.set_ylabel("Cluster labels")

        # The vertical line for average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

        ax1.set_yticks([])  # Clear the yaxis labels / ticks
        ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

        plt.suptitle(("KMeans on sample data "
                    "with n_clusters = {:d}".format(size)),
                    fontsize=20, fontweight='bold')
        
if __name__ == "__main__":
    print("No active abilities!")
