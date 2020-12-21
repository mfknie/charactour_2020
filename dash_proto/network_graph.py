
#%% 
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_cytoscape as cyto
from dash.dependencies import Input, Output

#%%
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx

#%%
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
#%% 
#Not bothering with css for now
app = dash.Dash(
    __name__,
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
)

#%%
# Preprocessing data 
drop_cols = ["id", "name", "name_title", "labels"]
likes = pd.read_csv(os.path.join("..", "data", "user_likes_chars.csv"))
data = pd.read_csv(os.path.join("..", "dash_proto", "dash_data", "data2.csv"))
# Filter by cosine similarity first - top 20 for now?
char_id = 782 # Hope van Dyne
char_idx = data.query('id == @char_id').index[0]
data_traits = data.drop(columns=drop_cols) \
    .replace({"%": ""}, regex=True)\
    .to_numpy("float32")
X = data_traits[char_idx].reshape(1, -1)
data["cosine"] = cosine_similarity(X, data_traits).flatten()
data_cos_20 = data.sort_values(by = ["cosine"]).tail(20)

likes_subset = likes[likes["likable_id"].isin(data_cos_20["id"])]
#%%

# This is slow, might use - https://stackoverflow.com/questions/22219004/how-to-group-dataframe-rows-into-list-in-pandas-groupby
# Even faster - https://stackoverflow.com/questions/38013778/is-there-any-numpy-group-by-function
user_likes_per_char = likes_subset.groupby('user_id')['likable_id'].apply(list).reset_index(name='chars') 


like_counts = likes_subset["user_id"].value_counts()
greater_1_idx = like_counts[like_counts > 1].index

# %%
# Edges
# First, find users who have liked more than one character
edges = user_likes_per_char[user_likes_per_char.isin(greater_1_idx)]
from collections import defaultdict
from itertools import combinations 
edges = defaultdict(int)
def eval_edges(l, d)
    # all unique pairs in list
    for x, y in combinations(l.sorted(), 2):
        edges[] += 1
        

user_likes_per_char.apply()

#%%
char_likes = nx.random_geometric_graph()
char_likes.add_nodes_from(data_cos_20["name_title"])  


# https://dash.plotly.com/cytoscape
# https://dash.plotly.com/cytoscape/styling
# For color gradient https://stackoverflow.com/questions/25668828/how-to-create-colour-gradient-in-python

cyto.Cytoscape(
    id='cytoscape-layout-9',
    elements=elements,
    style={'width': '100%', 'height': '350px'},
    layout={
        'name': 'cose'
    }
)
#%%


# Adding image https://community.plotly.com/t/displaying-image-on-point-hover-in-plotly/9223/11
# Need dash 

if __name__ == "__main__":
    app.run_server(debug=True)