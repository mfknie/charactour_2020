# %%
import pandas as pd
import numpy as np 
import os
import gc
# %%
def genre_traits(movie, genre):
    data_path = os.path.join("data", "chars_per_genre")
    if(movie):
        data_path = os.path.join("data", "chars_per_mov_genre")
    #print(data_path)
    likes = pd.read_csv(os.path.join("data", "user_likes_chars.csv"))
    chars = pd.read_csv(os.path.join("data", "char_info.csv")).query('like_count >= 50')
    genre_df = pd.read_csv(os.path.join(data_path, genre + ".csv"))
    
    # Extracting characters 
    likes = likes.merge(chars["id"], left_on = "likable_id", right_on = "id")

    users_genres = genre_df.merge(likes, "inner", left_on = "id", right_on = "likable_id").drop_duplicates(subset="user_id")

    traits = pd.read_csv(os.path.join("data", "user_traits.csv"))

    #gc.collect()
    return users_genres.merge(traits, "inner", left_on = "user_id", right_on = "user_id", suffixes = ["_"+genre, "_traits"]).loc[:,["user_id", "traits"]]


def write_csv(df, path):
    df.to_csv(path, index=False)

# %%
if __name__ == "__main__":

    # %%
    for g in os.listdir(os.path.join("data", "chars_per_mov_genre")):
        if(".csv" not in g):
            continue
        g = g.split(".")[0]
        traits_per_genre = genre_traits(True, g)
        
        traits_dict = traits_per_genre["traits"].apply(lambda x: dict(eval(x)))
        traits_df = pd.json_normalize(traits_dict)
        rtn_df = pd.concat([traits_per_genre["user_id"], traits_df], axis=1)

        write_csv(rtn_df, os.path.join("data", "chars_per_mov_genre", "traits", g + "_traits.csv"))

# %%
