import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
# import dash_table
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

### Global code to set up dash app and graph layout


# Dash will automatically look for /assets directory in the same directory
# that the python file is located in, at least when name = __name__ 

# The css file I am using atm is copy pasted from 'https://codepen.io/chriddyp/pen/bWLwgP.css',
# with all modifications kept at the beginning.
app = dash.Dash(
    __name__
)


# Consider putting entire table for any graphs into DB as opposed to running calculations in the dash code
# and periodically updating those tables.


# Assume we magically have the character we are rendering graph for:
char_id = 1527 # Drax
data_df = pd.read_csv(os.path.join("dash_data", "data2.csv"), dtype = {"labels": "str"})
char_idx = data_df.index[data_df["id"] == char_id][0]
traits = [x for x in data_df.columns if x not in ["name", "id", "name_title", "labels"]]

# Default to top three traits.
sing_char = data_df.query('id == @char_id')
top_traits = sing_char.drop(columns=["name", "id", "name_title", "labels"])\
    .sort_values(by = [char_idx], axis=1)\
    .columns[-1:-4:-1]

x_col = top_traits[0]
y_col = top_traits[1]
z_col = top_traits[2]

# Calculate cosine similarity
minus_char = data_df.drop(index = data_df.query('id == @char_id').index)

def percent_ston(df, type="float32"):
    '''
    Convert percent from string to numerical data type
    Inputs:
    df - dataframe with percentages
    type - numpy data type to convert to, np.float32 (single precision) by default.
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

minus_char["cs_perct"] = get_cosine(sing_char, minus_char, ["name", "id", "name_title", "labels"])
#minus_char["cs_perct"] = (minus_char["cs_perct"].rank(method = "min", pct = True))*0.9999

# Create Dash Layout
app.layout = html.Div(id='dash-container', children = [
    html.H1(children='3D Traits Dashboard', style={"text-align": "center"}),
    # TODO - add form or dropdown menu to allow users to switch characters
    # html.Div(children=[
    #
    # ]),
    html.Div(className='row-container', children=[
        html.Div(id='drop-container', children=[
            html.Div(className='drop-item', children=[
                dcc.Dropdown(
                    id='xaxis-col',
                    options=[{'label': i, 'value': i} for i in traits if i not in [y_col, z_col]],
                    value=x_col
                )
            ]),
            html.Div(className='drop-item', children=[
                dcc.Dropdown(
                    id='yaxis-col',
                    options=[{'label': i, 'value': i} for i in traits if i not in [x_col, z_col]],
                    value=y_col
                )
            ]),
            html.Div(className='drop-item', children=[
                dcc.Dropdown(
                    id='zaxis-col',
                    options=[{'label': i, 'value': i} for i in traits if i not in [y_col, x_col]],
                    value=z_col
                )
            ])
        ]),
        html.Div(id="3d-plot-container", children=[
            dcc.Graph(
                id = "3d-traits-plot"
            )
        ])
    ])
], style={'height': '100%'})

@app.callback(
    Output('3d-traits-plot', 'figure'),
    Input('xaxis-col', 'value'),
    Input('yaxis-col', 'value'),
    Input('zaxis-col', 'value')
)
def update_3d_plot(xaxis_col, yaxis_col, zaxis_col):
    '''
    Callback function to update 3d scatterplot when a trait is selection from the dropdown menu
    Inputs: Values from x, y and z 
    Output: 
    '''
    #sing_char = data_df.query('id == @char_id')
    #minus_char = data_df.drop(index = data_df.query('id == @char_id').index)
    fig = px.scatter_3d(minus_char, x = xaxis_col, y = yaxis_col, z = zaxis_col, width = 800, height = 600,
        hover_name = "name_title", color = "cs_perct", labels = {"cs_perct": "cosine similarity"})
    fig.update_traces(marker=dict(size=3))

    # Extracting x, y, z
    x_val = sing_char.iloc[0, data_df.columns.get_loc(xaxis_col)]
    y_val = sing_char.iloc[0, data_df.columns.get_loc(yaxis_col)]
    z_val = sing_char.iloc[0, data_df.columns.get_loc(zaxis_col)]
    fig.add_scatter3d(
        x = [x_val],
        y = [y_val],
        z = [z_val],
        marker=dict(
            color='green',
            # size=20,
            # line=dict(
            #     color='MediumPurple',
            #     width=2
            # )
            size = 9
        ),
        hoverinfo = "text",
        hovertemplate = '<b>{}</b>:<br>'.format(sing_char.iloc[0, data_df.columns.get_loc("name_title")]) +
        '{}: {} <br>'.format(xaxis_col, str(x_val)) +
        '{}: {} <br>'.format(yaxis_col, str(y_val)) +
        '{}: {} <br>'.format(zaxis_col, str(z_val)) +
        '<i>cluster: {}</i>'.format(sing_char.iloc[0, data_df.columns.get_loc("labels")]),
        name = sing_char.iloc[0, data_df.columns.get_loc("name_title")],
        showlegend=False
    )   

    fig.update_layout(margin={'l': 0, 'b': 0, 't': 0, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_col)
    fig.update_yaxes(title=yaxis_col)
    fig.update_yaxes(title=zaxis_col)
    print(fig)
    return fig


@app.callback(
    Output('xaxis-col', 'options'),
    Output('yaxis-col', 'options'),
    Output('zaxis-col', 'options'),
    Input('xaxis-col', 'value'),
    Input('yaxis-col', 'value'),
    Input('zaxis-col', 'value')
)
def update_3d_traits_dropdown(xaxis_col, yaxis_col,
    zaxis_col):
    x_opts = [{'label': i, 'value': i} for i in traits if i not in [yaxis_col, zaxis_col]]
    y_opts = [{'label': i, 'value': i} for i in traits if i not in [xaxis_col, zaxis_col]]
    z_opts = [{'label': i, 'value': i} for i in traits if i not in [xaxis_col, yaxis_col]]
    return x_opts, y_opts, z_opts

if __name__ == "__main__":
    app.run_server(debug=True)