# %%
import pandas as pd
import numpy as np 
import os
import gc
import mySQL
# %%
def write_csv(df, path, mode_str = "w", header = True):
    df.to_csv(path, index=False, mode = mode_str, header = header)

# %% 
def make_per(df, non_cols = None):
    p_age = df.drop(non_cols, axis = 1).div(df.sum(axis = 1), axis = 0) 
    p_ile = (p_age.rank(method = "min", pct = True))*0.9999
    return pd.concat([df[non_cols], p_ile], axis = 1)

# %%
if __name__ == "__main__":

    # %%
    path_in = os.path.join("data", "agg_mov_genre_traits.csv")
    path_out = os.path.join("data", "agg_mov_genre_perct.csv")
    write_csv(make_per(pd.read_csv(path_in), non_cols = ["genre", "total"]), path_out)
    
        
    # %%
