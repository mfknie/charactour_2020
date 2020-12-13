# Dash prototype
I built a dash prototype based off 3D plot rendered [here])(https://start.charactour.com/character-insight-panel/). There is not much html formatting, but it works.

## How to run
You need to install `pandas`, `numpy`, `scikit-learn`, `dash` and `plotly` with pip or conda. Then, navigate to this directory and run `python dash_prototype.py` or `python3 dash_protoype.py`.

## Files/Directories
* dash_data - holds data used in dashboard
    * dash_data/data.csv - original test data file (with percentile fan trait information for selected characters - 412 total), pulled from Ken/Markus's work
    * dash_data/data2.csv - same as data.csv, but added a column with basic kmeans clustering -> check ../cluster.py for that code.
* assets - default directory in which dash locates css and other assets
    * plotly.css - copied from 'https://codepen.io/chriddyp/pen/bWLwgP.css' (default plotly css?), with all my modifications written in at the top of the file.


## Code
The code is split into three parts, the first defining the dash app layout (made of html elements), 