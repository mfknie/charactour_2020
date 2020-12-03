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

def write_data_incr(df, name):
    df.to_csv("data/"+name+".csv", index=False, mode="a")


# %%
class mysql_pd:
    def __init__(self, info=None):
        if(info is None):
            print("No config specified")
            return None
        self.connect_str = "mysql+mysqlconnector://{0}:{1}@{2}/{3}".format(
            info.config("username"), 
            info.config("password"), 
            "localhost",
            info.config("MYSQL_DB"))
        self.engine = sqlalchemy.create_engine(self.connect_str)
        self.conn = None
    
    def connect(self):
        self.conn = self.engine.connect()
        return self.conn

    def disconnect(self):
        self.conn.close()
        self.conn = None

    def get_query(self, *args, once=True):
        if(once):
            self.connect()
        query_dfs = []
        for query in args:
            cur_df = pd.read_sql(sql = query, con = self.conn)
            query_dfs.append(cur_df)
        if(once):
            self.disconnect()
        return pd.concat(query_dfs)
    
    def write_sql(self, df, table_name, once=True):
        if(once):
            self.connect()
        df.to_sql(name = table_name, con = self.conn, if_exists="replace")
        if(once):
            self.disconnect()

# %%
if __name__ == "__main__":

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
    char_info = ("""select id, fullname, like_count, traits from characters""")
    traits_info = ("""select * from similartraits;""")
    user_info = (""" select id, first_name, last_name, has_liked, pronoun_id from users; """)

# %%    
    db_conn = mysql_pd(App)
    #db_conn.connect()
    #write_data(db_conn.get_query(chr_genre_query), "char_genre")
    #write_data(db_conn.get_query(movie_genre_query), "movie_genres")
    #write_data(db_conn.get_query(user_traits_query), "user_traits")
    write_data(db_conn.get_query(user_likes_query), "user_likes_chars")
    #db_conn.disconnect()

# %%
