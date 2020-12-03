# %%
import pandas as pd
import numpy as np 
import os
import gc
from mySQL import mysql_pd
# %%
def write_csv(df, path, mode_str = "w", header = True):
    df.to_csv(path, index=False, mode = mode_str, header = header)

# %% 
def make_per(df, non_cols = None):
    p_age = df.drop(non_cols, axis = 1).div(df.sum(axis = 1), axis = 0) 
    p_ile = (p_age.rank(method = "min", pct = True))*0.9999
    return pd.concat([df[non_cols], p_ile], axis = 1)

# %%
def traits_to_json(df, cols, keep_cols = None):
    formatted_traits = pd.Series(df.loc[:, cols].to_dict("records"), dtype = "string", name = "traits")
    if(keep_cols is not None):
        formatted_traits = pd.concat([df.loc[:, keep_cols], formatted_traits], ignore_index=True, axis=1)
    return formatted_traits
    

# %%
if __name__ == "__main__":

    # %%
    path_in = os.path.join("data", "agg_mov_genre_traits.csv")
    path_out = os.path.join("data", "agg_mov_genre_perct.csv")
    write_csv(make_per(pd.read_csv(path_in), non_cols = ["genre", "total"]), path_out)
        
    # %%
