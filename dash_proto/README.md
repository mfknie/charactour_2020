# Dash prototype
I built a dash prototype based off 3D plot rendered [here](https://start.charactour.com/character-insight-panel/). There is not much html formatting, but it works.

## How to run
You need to install the following python libraries, along with their dependencies:
* `pandas` 
* `numpy` 
* `scikit-learn`
* `dash` (which should also install `dash_html_components` and `dash_core_components`, but if not, install these separately)
* `plotly` 
* `dash-cytoscape` (if I ever do the network graph)
with pip or conda. Then, navigate to this directory and run `python dash_prototype.py` or `python3 dash_protoype.py`.

## Directories (containing assets and other materials)
* dash_data (in .gitignore atm) - holds data used in dashboard
    * dash_data/data.csv - original test data file (with percentile fan trait information for selected characters - 412 total), pulled from Ken/Markus's work
    * dash_data/data2.csv - same as data.csv, but added a column with basic kmeans clustering -> check ../cluster.py for that code.
* assets - default directory in which dash locates css and other assets
    * plotly.css - copied from 'https://codepen.io/chriddyp/pen/bWLwgP.css' (default plotly css?), with all my modifications written near the top of the file

## Code
* dash_prototype.py - Main file containing dash app, callbacks and helper functions (need to refactor this into multiple files someday)
    * The first section of the code defines the dash app layout (made of html elements), and also reads in the data (from disk, for now)
    * The rest of the code contains callbacks, which is what tells the graphs to change when different options in the dropdown menu are selected, etc...
    * The app is run through app.run() called in the `if __name__ = "__main__"` part of the code, which will be delegated to blueprints in the future
* network_graph.py - I am currently experimenting with building a network graph with dash. 
    * Basically, the goal is to be able to represent character relationships (in terms of joint likes by users) 
    by having each character as a node, and each edge's color representing the number of likes. 
    * See https://dash.plotly.com/cytoscape for more information