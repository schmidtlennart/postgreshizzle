import pandas as pd
import psycopg2
import sqlalchemy
import sys

# load data
mwe = pd.read_csv("data/dbtestdata_mwe100.csv")

# get db log-in credentials
exec(open('100_config_passwords.py').read())


# connect to db
con =  psycopg2.connect(config_string_adm)

# set cursor
cur = con.cursor()
################################
######## CREATE TABLE
################################

# execute Statement
statement = """
        CREATE TABLE winddaten_test (
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


################################
######## FOR TESTING: DELETE TABLE
################################

#statement = "DROP TABLE winddaten_test"
