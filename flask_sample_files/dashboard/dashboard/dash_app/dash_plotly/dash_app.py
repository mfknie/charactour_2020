import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table
import plotly.express as px

import pandas as pd
import os

# Don't like relative paths :(
data_path = os.path.join("..", "..", "..", "data")


def create_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
        ]
    )
    
    data_df = pd.read_csv(os.path.join(data_path, "data.csv"))
    # Consider putting entire table for each graph into MySQL DB?

    x_col = "Polite"
    y_col = "Optimistic"
    z_col = "Organized"
    fig = px.scatter_3d(data_df, x=x_col, y=y_col, z=z_col, 
        color="cluster_label", hover_name = "id")
    # Create Dash Layout
    # To eliminate columns already in the graph, we can maybe run a callback to itself
    dash_app.layout = html.Div(id='dash-container', children = [
        html.H1(children='Dashboard'),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in data_df.columns if i not in [y_col, z_col]],
                    value='X'
                )
            ], style={'width': '48%', 'float': 'left', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in data_df.columns if i not in [x_col, z_col]],
                    value='Y'
                )
            ],
            style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='zaxis-column',
                    options=[{'label': i, 'value': i} for i in data_df.columns if i not in [y_col, z_col]],
                    value='Z'
                )
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]),
        dcc.Graph(
            id = "3d_traits_plot",
            figure = fig
        ),
    ])
    
    init_callbacks(dash_app)


    return dash_app.server


def generate_table(df, name, max_rows=10):
    return dash_table.DataTable(
        id=name,
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )


def init_callbacks(dash_app, df):
    @dash_app.callback(
        Output(component_id='3d_traits_plot', component_property='figure'),
        Input('xaxis-column', 'value'),
        Input('yaxis-column', 'value'),
        Input('zaxis-column', 'value')
    )
    def update_3d_traits_plot(xaxis_column_name, yaxis_column_name,
        zaxis_column_name):
        
        fig = px.scatter_3d(df, x = xaxis_column_name, y = yaxis_column_name, z = zaxis_column_name, 
            color="cluster_label", hover_name = "id")

        fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

        fig.update_xaxes(title=xaxis_column_name)
        fig.update_yaxes(title=yaxis_column_name)
        fig.update_yaxes(title=zaxis_column_name)

        return fig
    
    
    @dash_app.callback(
        Output('xaxis-column', 'options'),
        Output('yaxis-column', 'options'),
        Output('zaxis-column', 'options'),
        Input('xaxis-column', 'value'),
        Input('yaxis-column', 'value'),
        Input('zaxis-column', 'value')
    )
    def update_3d_traits_dropdown(xaxis_column, yaxis_column,
        zaxis_column):
        x_opts = [{'label': i, 'value': i} for i in data_df.columns if i not in [yaxis_column, zaxis_column]]
        y_opts = [{'label': i, 'value': i} for i in data_df.columns if i not in [xaxis_column, zaxis_column]]
        z_opts = [{'label': i, 'value': i} for i in data_df.columns if i not in [xaxis_column, yaxis_column]]
        return x_opts, y_opts, z_opts