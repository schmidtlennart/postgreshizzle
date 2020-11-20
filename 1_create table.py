import pandas as pd
import psycopg2
import sqlalchemy
import sys

# load data
mwe = pd.read_csv("data/dbtestdata_mwe2.csv")

# connect to db
#con =  psycopg2.connect("dbname='isewer' user='isewer_rw' host='postgres' port='5432' password='abwasser2020_rw'")
con =  psycopg2.connect("dbname='isewer' user='isewer_adm' host='postgres' port='5432' password='B!!irkenbr0t'")

# set cursor
cur = con.cursor()
################################
######## CREATE TABLE
################################

# execute Statement
statement = """
        CREATE TABLE winddaten (
        messdatum time PRIMARY KEY,
        st_id integer,
        st_name varchar,
        dd numeric,
        ff numeric,
        fx numeric,
        ff_max_mw numeric,
        ff_ws numeric,
        dd_ws numeric,
        lat numeric,
        lon numeric,
        height numeric
        )
        """
cur.execute(statement)#get created into schema "public"
# commit changes
con.commit()

### Close connection
con.close()
