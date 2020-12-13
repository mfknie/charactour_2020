from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import pandas as pd

db = SQLAlchemy()
# add  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') to config
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
#     os.getenv('DB_USER', 'flask'),
#     os.getenv('DB_PASSWORD', ''),
#     os.getenv('DB_HOST', 'mysql'),
#     os.getenv('DB_NAME', 'flask')
# )


# Should we use ORM or pandas? speed test?

### Define schema/tables we need to use on website
# TODO - move to models.py
# class user_acct(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(80), unique=True, nullable=False)
#     last_name = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<User {}>'.format(self.first_name)


# class user_percentiles(db.Model):

#     user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
#     # JSON?
#     percentiles = db.Column(db.String(1000), unique=False, nullable=False)
#     __tablename__ = "user_percentiles"

#     def __repr__(self):
#         return '<User {}>'.format(self.user_id)


class pd_sql:
    def __init__(self, db): 
        self.db = db
    
    def get_tbl_df(self, query):
        """Takes SQL query. Returns pandas dataframe."""
        try:             
            df = pd.read_sql_query(sql=query,
                                con=self.db.engine())
            return df
        except:
            return "Oops!" 

    def set_tbl_df(self, df, tbl_name):
        """Takes pandas dataframe, inserts into database with name tbl_name"""
        try:
            some_num = 20
            ins_type = 'multi'
            if(df.shape[1] > some_num):
                # can write custom callable with mysql-connector and cursor in future
                ins_type = None
            
            df.to_sql(tbl_name, con=self.db.engine, if_exists="replace", method = ins_type)
        except:
            return "Oops!" 