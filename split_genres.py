# %%
import pandas as pd
import numpy as np 
import os
# %%
def ind_genre_csvs(df, genre_name, movie, char):
    if(movie):
        df.query('genre == @genre_name').to_csv("data/chars_per_mov_genre/" +  genre_name + ".csv", index=False)
    if(char):
        df.query('genre == @genre_name').to_csv("data/chars_per_genre/" +  genre_name + ".csv", index=False)
# %%
if __name__ == "__main__":
    # %%
    # TODO - add video game genres later
    movie_genres = pd.read_csv(os.path.join("data", "movie_genres.csv"))
    char_genres = pd.read_csv(os.path.join("data", "char_genre.csv"))
    
    # %%
    #
    movie_g = movie_genres["genre"].unique()
    char_g = char_genres["genre"].unique()
    all_g = np.union1d(movie_g, char_g)
    both_g = np.intersect1d(movie_g, char_g)

    # %%
    combined_genres = pd.concat([movie_genres, char_genres]).drop_duplicates()
    # %%
    for g in all_g:
        if (g in both_g):
            ind_genre_csvs(combined_genres, g, True, True)
        elif (g in movie_g):
            ind_genre_csvs(movie_genres, g, True, False)
        else:
            ind_genre_csvs(char_genres, g, False, True)
# %%
