
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
data_cos_20 = data.sort_values(by = ["cosine"]).tail(10)

likes_subset = likes.merge(data_cos_20.loc[:, ["id", "name"]], left_on="likable_id", right_on="id")

# %%
### Filter users: 
# Find which users like more than one character
# This is slow, might use - https://stackoverflow.com/questions/22219004/how-to-group-dataframe-rows-into-list-in-pandas-groupby
# Even faster - https://stackoverflow.com/questions/38013778/is-there-any-numpy-group-by-function
user_likes_per_char = likes_subset.groupby('user_id')['likable_id']\
    .apply(list)\
    .reset_index(name='chars') 
like_counts = likes_subset["user_id"].value_counts()
greater_1_idx = like_counts[like_counts > 1].index.to_series(name = "user_id")
user_likes_multi = user_likes_per_char.merge(greater_1_idx, 
    on = "user_id")

# %%
### Construct edges:
from collections import defaultdict
from itertools import combinations 

edges = defaultdict(int)
def eval_edges(l, d):  
    # all unique pairs in list - need sort first
    # l.sort()
    for x, y in combinations(sorted(l), 2):
        d[(x,y)] += 1  

user_likes_multi["chars"].apply(eval_edges, d = edges)


#%%
# char_likes = nx.random_geometric_graph()
# char_likes.add_nodes_from(data_cos_20["name_title"])  


# https://dash.plotly.com/cytoscape
# https://dash.plotly.com/cytoscape/styling
# For color gradient https://stackoverflow.com/questions/25668828/how-to-create-colour-gradient-in-python
from matplotlib import cm
import statistics 
ssheet = [{
        'selector': 'node',
        'style': {
            'content': 'data(label)'
        }
    },
    {
    'selector': '.terminal',
    'style': {
        'width': 80,
        'height': 80,
        'background-fit': 'cover',
        'background-image': 'url(url)'#'data(url)'
    }
}]
elements = data_cos_20.loc[:, ["id", "name"]]\
    .apply(lambda x: {"group": "nodes", 
    "classes": "terminal",
    "data": {
        "id": x[0], 
        "label": x[1],
        "url": os.path.join(".", "dash_data", "pics", "{}.jpg".format(x[0]))
    }}, axis = 1)\
    .to_list()
max_val = max(edges.values())
min_val = min(edges.values())
print(max_val)
blues = cm.get_cmap("binary")
for x, y in edges.items():
    # add edge 
    elements.append({"group": "edges", "data": {
        "id": "{}{}".format(x[0], x[1]),
        "source": x[0], 
        "target": x[1]
    }})
    cur_color = blues((y/max_val) - (min_val/max_val))
    print(cur_color)
    print("New : {}".format(x[0]))
    ssheet.append({"selector": "#{}{}".format(x[0], x[1]),#, x[1], x[0]),
        "style": {
            'line-color': 'rgb({}, {}, {})'.format(cur_color[0], cur_color[1], cur_color[2]) 
        }
    })
# print(elements)
# print(ssheet)    


# %%
### Constructing the graph itself
app = dash.Dash(
    __name__,
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
)
app.layout = html.Div([
        cyto.Cytoscape(
            id='cytoscape-layout-9',
            elements=elements,
            style={'width': '100%', 'height': '500px'},
            layout={
                'name': 'circle'
            },
            stylesheet=ssheet
        ),
        html.Div("test")
    ], 
    style = {
        "height": "100%"
    }
)
#%%


# Adding image https://community.plotly.com/t/displaying-image-on-point-hover-in-plotly/9223/11
# Need dash 

if __name__ == "__main__":
    app.run_server(debug=True)
# %%
