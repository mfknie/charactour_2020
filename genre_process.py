# %%
import pandas as pd
import numpy as np 
import os
import gc
# %%
def write_csv(df, path, mode_str = "w", header = True):
    df.to_csv(path, index=False, mode = mode_str, header = header)

def extract_user_traits(movie, genre, char_likes, user_likes):
    #Load-in
    data_path = os.path.join("data", "chars_per_genre")
    if(movie):
        data_path = os.path.join("data", "chars_per_mov_genre")
    #print(data_path)
    likes = pd.read_csv(os.path.join("data", "user_likes_chars.csv"))
    chars = pd.read_csv(os.path.join("data", "char_info.csv")).query('like_count >= @char_likes')
    genre_df = pd.read_csv(os.path.join(data_path, genre + ".csv"))
    users = pd.read_csv(os.path.join("data", "user_info.csv")).query('has_liked > @user_likes')

    likes = likes.merge(chars["id"], left_on = "likable_id", right_on = "id")
    # Take sum of all likes of characters in the given genre grouped by user
    users_genre = genre_df.merge(likes, "inner", left_on = "id", right_on = "likable_id").groupby(by="user_id", as_index = False).count()
    users_genre = users_genre.loc[:, ["user_id", "likable_id"]]\
        .merge(users.loc[:, ["id", "has_liked"]], "inner", left_on = "user_id", right_on = "id")\
        .rename(columns={"likable_id": "genre_likes"})
    #print(users_genre.columns)
    users_genre["like_percentile"] = users_genre["genre_likes"]/users_genre["has_liked"]
    traits = pd.read_csv(os.path.join("data", "user_traits.csv"))

    #gc.collect()
    return users_genre.merge(traits, "inner", left_on = "user_id", right_on = "user_id", suffixes = ["_"+genre, "_traits"]).loc[:,["user_id", "traits", "like_percentile", "genre_likes", "has_liked"]]
# %%

# def extract_agg_user_traits(movie, genre, char_likes, user_likes):
#     data_path = os.path.join("data", "chars_per_genre")
#     if(movie):
#         data_path = os.path.join("data", "chars_per_mov_genre")
#     likes = pd.read_csv(os.path.join("data", "user_likes_chars.csv"))
#     chars = pd.read_csv(os.path.join("data", "char_info.csv")).query('like_count >= @char_likes')
#     genre_df = pd.read_csv(os.path.join(data_path, genre + ".csv"))
#     users = pd.read_csv(os.path.join("data", "user_info.csv")).query('has_liked > @user_likes')

#     likes = likes.merge(chars, left_on = "likable_id", right_on = "id")
#     users_genre = genre_df.merge(likes, "inner", left_on = "id", right_on = "likable_id").groupby(by=["fullname_x", "likable_id"], as_index = False).count()
#     print(users_genre)


# %%

def user_traits_by_genre(movie, genre):
    traits_per_genre = extract_user_traits(movie, genre, 50, 25)
    traits_dict = traits_per_genre.pop("traits").apply(lambda x: dict(eval(x)))
    traits_df = pd.json_normalize(traits_dict)
    rtn_df = pd.concat([traits_per_genre, traits_df], axis=1)
    return rtn_df

def agg_mov_genre_total(movie, genre, user_likes):
    data_path = os.path.join("data", "chars_per_genre")
    if(movie):
        data_path = os.path.join("data", "chars_per_mov_genre")
    genre_df = pd.read_csv(os.path.join(data_path, "traits", genre + "_traits.csv"))
    traits_info = pd.read_csv(os.path.join("data", "traits_info.csv"))
    
    genre_traits = {"genre": genre, "total": genre_df["user_id"].count()}
    genre_traits.update({ traits_info.iat[k - 1, 2]: genre_df[genre_df[str(k)] <= 2.0][str(k)].count() for k in list(range(1, 21)) + [23, 24, 25] })

    genre_traits.update({ traits_info.iat[k - 1, 3]: genre_df[genre_df[str(k)] >= 4.0][str(k)].count() for k in list(range(1, 21)) + [23, 24, 25] })
    
    #print(genre_traits)
    return pd.DataFrame(genre_traits, index=[0])

# %%
if __name__ == "__main__":

    # %%
    for i, g in enumerate(os.listdir(os.path.join("data", "chars_per_mov_genre"))):
        if(".csv" not in g):
            continue
        else: 
            g = g.split(".")[0]
        if(i == 1):
            mode_str = "w"
            h = True
        else:
            mode_str = "a"
            h = False
        #write_csv(agg_mov_genre_total(True, g, 25), os.path.join("data", "agg_mov_genre_traits.csv"), mode_str, header = h)
        #write_csv(user_traits_by_genre(True, g), os.path.join("data", "chars_per_mov_genre", "traits", g + "_traits.csv"))
# %%
