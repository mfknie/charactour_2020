# Charactour
Clustering work in python for Charactour: https://start.charactour.com/about/

## Aim

Utilize unsupervised learning to explore how fans interact with characters.

## Data

I am currently using a MySQL database from around 06/16/2020, containing data including but no limited to character information, users, user traits (based off quiz), genres, movie genres, video game genres, likes, etc...

## Code

__Usable__:  
* `mySQL.py` handles most of the reading from the MySQL database to pandas/csv, and depends on `config.py` for password/username information
* `kmeans_eval.py` contains adapted code from sklearn documentation for constructing silhouette plots to determine kmeans clusters.
* `split_genres.py` takes character and genre data and constructs .csv files containing all characters from each genre.
* `genre_process.py` is the primary workhorse for manipulating trait/like data. It contains:
    + Functions for splitting user traits based off genres users have liked (.csv files include total likes/likes devoted to this specific genre for each individual).
    + Functions for aggregating counts of users based off traits grouped by genre.
* `percentile_process.py` takes aggregate user trait counts and turns them into percentiles.
  
__Incomplete__:  
* `cluster.py` is meant contain a wrapper class for clusterers, which would include some standardized functions useful for metrics/analysis (e.x. pcp plot)
* `eval_pred.py` is a side project meant to evaluate classification performance (from using cosine similarlity) using F1 score, Hamming loss or Jaccard index.

### Jupyter Notebooks
* `initial_dbscan_genre.ipynb` and `initial_kmeans_genre.ipynb` contain initial clustering efforts (i.e. no filtering or quality control on data) using DBscan and Kmeans respectively on user traits from the Action genre, along with EDA in the former.
    + Contains automated parameter search to find optimal size/number of epsilon/clusters
* `genre_percent_cluster.ipynb` contains Kmeans clustering on the Romance genre, with the ability to filter data based off percentage of likes users devoted to X genre and the number of total likes (to avoid low quality data)
    + Used automated parameter search to find optimal number of clusters and best minimum pecentage/minimum number of likes to set as bounds    

The remaining notebooks contain much less progress so far:  
* `agg_genre_5-01-2020.ipynb` will contain some clustering on aggregate data for characters from X genre, using data from popular characters on the site as of 05/01/2020
* `genre_classication.ipynb` will be an experiment to see how well an ensemble classifier would work in predicting genres that users may become fans of (i.e. more precisely, they may become fans of, or like characters from those genres), based off their trait data (may need to look into http://scikit.ml/index.html to help deal with large number of labels, if there was a desire to predict characters directly) 

## Planned updates (in order of priority)

1. Clustering on overall user trait aggregation percentile data grouped by genre
2. Contributions to dashboard visualiztion project (based off clustering done on user trait percentile data) - will most likely use flask and bokeh.

## Notes
* Given size of data/confidentiality issues, the raw data is not included in the git repository. Contact me at marknie1998@gmail.com for more information. 


