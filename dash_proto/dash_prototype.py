### Dash imports
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

### Plotly imports
# import dash_table
import plotly.express as px
import plotly.graph_objects as go

### Other
import pandas as pd
import os
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# Dash will automatically look for /assets directory in the same directory
# that the python file is located in, at least when name = __name__ 

# The css file I am using atm is copy pasted from 'https://codepen.io/chriddyp/pen/bWLwgP.css',
# with all modifications kept at the beginning.
app = dash.Dash(
    __name__
)

### Issues

# Consider putting entire table for any graphs into DB as opposed to running calculations in the dash code
# and periodically updating those tables.

# We technically don't have to refilter dataframe and recalculating cosine similarity when we change axis (slowdown may be more apparent with more characters)
# Check http://dash.plotly.com/performance.

### Helper functions
def top_3_traits(one_char_df):
    '''
    Helper function to extract top three traits for any given character in terms of percentile
    Inputs: Dataframe with only the given character
    Output: Names of top three traits as a tuple.
    '''
    top_traits = one_char_df.drop(columns=["name", "id", "name_title", "labels"])\
        .sort_values(by = [one_char_df.index[0]], axis=1)\
        .columns[-1:-4:-1]
    return top_traits[0], top_traits[1], top_traits[2]

def percent_ston(df, type="float32"):
    '''
    Convert percent from string to numerical data type
    Inputs:
    df - dataframe with percentages/percentiles.
    type - numpy data type to convert to, np.float32 (single precision) by default.
    Output: ndarray of numerical percentages/percentiles
    '''
    return df.replace({"%": ""}, regex=True).to_numpy(type)

def get_cosine(X, Y, non_num_cols=None):
    '''
    Inputs:
    X - dataframe of fan trait percentiles for focus character
    Y - dataframe of fan trait percentiles for all other characters
    non_num_cols - extraneous name or id columns
    Output: ndarray of cosine similarities relative to character of focus
    '''
    y_data = percent_ston(Y.drop(columns=non_num_cols))
    x_data = percent_ston(X.drop(columns=non_num_cols))
    return cosine_similarity(x_data, y_data).flatten()



### Default actions to set everything up
char_id = 1527 # Drax
# TODO - grab data from mysql someday, once MVC/ORM is set up to do so
data_df = pd.read_csv(os.path.join("dash_data", "data2.csv"), dtype = {"labels": "str"})
traits = [x for x in data_df.columns if x not in ["name", "id", "name_title", "labels"]]

# Dataframe with just the select character id (in the callback for the name dropdown menu, 
# we filter by name instead of id, may be an issue later on)
sing_char = data_df.query('id == @char_id')
# Filtering out every other character.
minus_char = data_df.drop(index = data_df.query('name == @char_id').index)
minus_char["cs_perct"] = get_cosine(sing_char, minus_char, ["name", "id", "name_title", "labels"])

# # Initial values for top three traits (should select top three in general)
#x_col, y_col, z_col = top_3_traits(data_df.query('id == @char_id'))
#minus_char["cs_perct"] = (minus_char["cs_perct"].rank(method = "min", pct = True))*0.9999

# Create Dash Layout
app.layout = html.Div(id='dash-container', children = [
    html.H1(children='3D Traits Dashboard', style={"text-align": "center"}),
    html.Div(id='name-container', children=[
        dcc.Dropdown(
            id='drop-name',
            options=[{'label': i, 'value': i} for i in data_df["name"]],
            value=sing_char["name"].iloc[0]
        )
    ]),
    html.Div(className='row-container', children = [
        html.Div(id='perct-high', children = [
            dcc.Graph(
                id='perct-high-bar'
            )
        ]),
        html.Div(id='perct-low', children = [
            dcc.Graph(
                id='perct-low-bar'
            )
        ])
    ]),
    html.Div(className='row-container', children=[
        html.Div(id='drop-container', children=[
            html.Div(className='drop-item', children=[
                dcc.Dropdown(
                    id='xaxis-col',
                    options=[{'label': i, 'value': i} for i in traits]#,value=x_col
                )
            ]),
            html.Div(className='drop-item', children=[
                dcc.Dropdown(
                    id='yaxis-col',
                    options=[{'label': i, 'value': i} for i in traits]#,value=y_col
                )
            ]),
            html.Div(className='drop-item', children=[
                dcc.Dropdown(
                    id='zaxis-col',
                    options=[{'label': i, 'value': i} for i in traits]#,value=z_col
                )
            ])
        ]),
        html.Div(id="3d-plot-container", children=[
            dcc.Graph(
                id = "3d-traits-plot"
            )
        ])
    ]),
    html.Div(id='invis-data', style={'display': 'none'})
], style={'height': '100%'})

### 3D plot stuff

### After consolidating callbacks, I am commenting this out for now
# def update_fig(sing_char, minus_char, xaxis_col, yaxis_col, zaxis_col):
#     '''
#     Helper function to update figure with axises information.
#     Takes sing_char (dataframe with just selected character) and minus_char (dataframe without selected character) from global
#     Inputs: Current values for dropdown menus per axis
#     Output: Updated figure with columns configured to user selection
#     '''
#     fig = px.scatter_3d(minus_char, x = xaxis_col, y = yaxis_col, z = zaxis_col, width = 1000, height = 800,
#         hover_name = "name_title", color = "cs_perct", labels = {"cs_perct": "cosine similarity"})
#     fig.update_traces(marker=dict(size=3))

#     # To highlight the single character, we make the point green and larger than all the other points
#     # To do this, we must add it as another "trace" onto the point, hence the separation of data earlier in the code
#     x_val = sing_char.iloc[0, data_df.columns.get_loc(xaxis_col)]
#     y_val = sing_char.iloc[0, data_df.columns.get_loc(yaxis_col)]
#     z_val = sing_char.iloc[0, data_df.columns.get_loc(zaxis_col)]
#     fig.add_scatter3d(
#         x = [x_val],
#         y = [y_val],
#         z = [z_val],
#         marker=dict(
#             color='black',
#             size = 9
#         ),
#         hoverinfo = "text",
#         hovertemplate = '<b>{}</b>:<br>'.format(sing_char.iloc[0, data_df.columns.get_loc("name_title")]) +
#             '{}: {} <br>'.format(xaxis_col, str(x_val)) +
#             '{}: {} <br>'.format(yaxis_col, str(y_val)) +
#             '{}: {} <br>'.format(zaxis_col, str(z_val)),
#         name = sing_char.iloc[0, data_df.columns.get_loc("name_title")],
#         showlegend = False
#     )   

#     # Some code I saw online to tighten margins, not sure if this does anything.
#     # fig.update_layout(margin={'l': 0, 'b': 0, 't': 0, 'r': 0}, hovermode='closest')

#     fig.update_xaxes(title=xaxis_col)
#     fig.update_yaxes(title=yaxis_col)
#     fig.update_yaxes(title=zaxis_col)
#     #print(fig)
#     return fig

@app.callback(
    Output('3d-traits-plot', 'figure'),
    [Input('xaxis-col', 'value'),
    Input('yaxis-col', 'value'),
    Input('zaxis-col', 'value')],
    [State('drop-name', 'value'),
    State('invis-data', 'children')]
)
def update_3d_traits(xaxis_col, yaxis_col, zaxis_col, drop_name, cosine_sim):
    '''
    Callback function to update 3d scatterplot traits are changed
    NOte
    Inputs: 
    Current values for dropdown menus per axis
    drop_name - value from drop-name character name dropdown
    cosine_sim - json information from invisible div
    Output: Updated figure with columns configured to user selection
    '''
    sing_char = data_df.query('name == @drop_name')
    minus_char = data_df.drop(index = data_df.query('name == @drop_name').index)
    minus_char["cs_perct"] = json.loads(cosine_sim)
    # Moving everything to another calback
    # We want only want to recalculate cosine similarity (as there can be up to 6k characters eventually)
    # shouldn't be a problem - https://stackoverflow.com/questions/855191/how-big-can-a-python-list-get
    # The intermediate value is 
    # ctx = dash.callback_context
    # if not ctx.triggered or (ctx.triggered[0]['prop_id'].split('.')[0] == 'drop-name'):
    #     cosine_new = get_cosine(sing_char, minus_char, ["name", "id", "name_title", "labels"])
    #     cosine_sim = json.dumps(cosine_new.tolist())
    #     minus_char["cs_perct"] = cosine_new        
    # else:
    #     minus_char["cs_perct"] = json.loads(cosine_sim) #get_cosine(sing_char, minus_char, ["name", "id", "name_title", "labels"])

    fig = px.scatter_3d(minus_char, x = xaxis_col, y = yaxis_col, z = zaxis_col, width = 1000, height = 800,
        hover_name = "name_title", color = "cs_perct", labels = {"cs_perct": "cosine similarity"})
    fig.update_traces(marker=dict(size=3))

    # To highlight the single character, we make the point green and larger than all the other points
    # To do this, we must add it as another "trace" onto the point, hence the separation of data earlier in the code
    x_val = sing_char.iloc[0, data_df.columns.get_loc(xaxis_col)]
    y_val = sing_char.iloc[0, data_df.columns.get_loc(yaxis_col)]
    z_val = sing_char.iloc[0, data_df.columns.get_loc(zaxis_col)]
    fig.add_scatter3d(
        x = [x_val],
        y = [y_val],
        z = [z_val],
        marker=dict(
            color='black',
            size = 9
        ),
        hoverinfo = "text",
        hovertemplate = '<b>{}</b>:<br>'.format(sing_char.iloc[0, data_df.columns.get_loc("name_title")]) +
            '{}: {} <br>'.format(xaxis_col, str(x_val)) +
            '{}: {} <br>'.format(yaxis_col, str(y_val)) +
            '{}: {} <br>'.format(zaxis_col, str(z_val)),
        name = sing_char.iloc[0, data_df.columns.get_loc("name_title")],
        showlegend = False
    )   

    # Some code I saw online to tighten margins, not sure if this does anything.
    # fig.update_layout(margin={'l': 0, 'b': 0, 't': 0, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_col)
    fig.update_yaxes(title=yaxis_col)
    fig.update_yaxes(title=zaxis_col)
    return fig

@app.callback(
    [Output('xaxis-col', 'value'),
    Output('yaxis-col', 'value'),
    Output('zaxis-col', 'value'),
    Output('invis-data', 'children')],
    [Input('drop-name', 'value')]
    #prevent_initial_call = "True"
)
def update_top_3(drop_name):
    '''
    Callback function to set column dropdown values to top three for given character, as well as invisible cosine similarity calculation
    This will lead to the 3d_plots graph being updated as well (chained callback)
    Inputs:
    drop-name - name of character to switch to
    Output: Return three current values for dropdown menu (for x, y, z axis)
    '''
    #print(drop_name)
    sing_char = data_df.query('name == @drop_name')
    minus_char = data_df.drop(index = data_df.query('name == @drop_name').index)
    cosine_new = get_cosine(sing_char, minus_char, ["name", "id", "name_title", "labels"])
    cosine_sim = json.dumps(cosine_new.tolist())
    top3 = top_3_traits(data_df.query('name == @drop_name'))
    return top3[0], top3[1], top3[2], cosine_sim


@app.callback(
    [Output('xaxis-col', 'options'),
    Output('yaxis-col', 'options'),
    Output('zaxis-col', 'options')],
    [Input('xaxis-col', 'value'),
    Input('yaxis-col', 'value'),
    Input('zaxis-col', 'value')]
)
def update_trait_choices(xaxis_col, yaxis_col, zaxis_col):
    '''
    Callback to restrict the selection of two or more of the same traits in different axis. 
    Doing so wouldn't break the graph, but I think it is sensible to have it this way for now.
    Inputs: Current values for dropdown menus per axis
    Output: Return three updated lists dropdown options per axis
    '''
    x_opts = [{'label': i, 'value': i} for i in traits if i not in [yaxis_col, zaxis_col]]
    y_opts = [{'label': i, 'value': i} for i in traits if i not in [xaxis_col, zaxis_col]]
    z_opts = [{'label': i, 'value': i} for i in traits if i not in [xaxis_col, yaxis_col]]
    return x_opts, y_opts, z_opts

### Percentile bar graphs
@app.callback(
    [Output('perct-high-bar', 'figure'),
    Output('perct-low-bar', 'figure')],
    [Input('drop-name', 'value')]
)
def update_perct_graphs(drop_name):
    sing_char = data_df.query('name == @drop_name')
    idx = sing_char.index[0]
    sing_char = sing_char.drop(columns=["name", "id", "name_title", "labels"])\
        .replace({"%": ""}, regex=True)\
        .apply(pd.to_numeric, errors='coerce')\
        .sort_values(by = [idx], ascending = False, axis=1)\
        .T\
        .rename(columns = {idx: "perct"})
    sing_char["traits"] = sing_char.index
    
    #Higher bar graph
    fig_high = px.bar(sing_char.head(10).sort_values(by = "perct"), y = "traits", x = "perct", text = "perct",
        orientation = 'h', title = "Highest percentile traits", labels=dict(traits="", perct=""),
        hover_data = ["perct"])
    fig_high.update_xaxes(range=[0, 100])
    #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    #Lower bar graph
    fig_low = px.bar(sing_char.tail(10), y = "traits", x = "perct", text = "perct",
        orientation = 'h', title = "Lowest percentile traits", labels=dict(traits="", perct=""),
        hover_data = ["perct"])
    fig_low.update_xaxes(range=[0, 100])
    return fig_high, fig_low


if __name__ == "__main__":
    app.run_server(debug=True)