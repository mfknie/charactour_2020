import pandas as pd
import numpy as np
import mysql.connector
from cluster import app

def import_data(file):
    pd.read_csv(file)


if __name__ == "__main__":
    with connect = mysql.connector.connect(user=App.config("username")
            password=App.config("password")
            host=""
            database=App.config("MYSQL_DB")
        ):
        