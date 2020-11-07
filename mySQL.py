# %%
import pandas as pd
import numpy as np
import mysql.connector
import sqlalchemy
from config import App
# %%

def import_data(file):
    pd.read_csv(file)

def write_data(df, name):
    df.to_csv("data/"+name+".csv", index=False)

def write_data_incr(df):
    df.to_csv("data/"+name+".csv", index=False, mode="a")

# %%
if __name__ == "__main__":
    # %%
    connect_str = "mysql+mysqlconnector://{0}:{1}@{2}/{3}".format(
        App.config("username"), 
        App.config("password"), 
        "localhost",
        App.config("MYSQL_DB"))
    engine = sqlalchemy.create_engine(connect_str)
    
    # %%
    chr_genre_query = ("""select characters.id, characters.fullname, genres.genre 
        from characters inner join genres on characters.genres LIKE genres.id;
    """)
    movie_genre_query = ("""select characters.id, characters.fullname, title_movie_genres.genre from characters 
        inner join title_movie_genres_pivot on characters.bookmovieid = title_movie_genres_pivot.title_id
        inner join title_movie_genres on title_movie_genres_pivot.genre_id = title_movie_genres.id;
    """)
    user_traits_query = ("""select * from usertraits""")
    user_likes_query = ("""select * from likeable_likes where likable_type = "character" """)
    
# %%
    genre_df = None
# %%
    conn = engine.connect()
# %%
    with engine.connect() as conn:
# %%    
        write_data(pd.read_sql(sql = chr_genre_query, con = conn), "char_genre")
        write_data(pd.read_sql(sql = movie_genre_query, con = conn), "movie_genres")
        write_data(pd.read_sql(sql = user_traits_query, con = conn), "user_traits")
        write_data(pd.read_sql(sql = user_likes_query, con = conn), "user_likes_chars")

# %%
# for VSscode jupyter
    conn.close()

# %%
