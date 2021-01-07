import pandas as pd
import psycopg2
import sys

# get db log-in credentials
exec(open('100_config_passwords.py').read())
engine_string_rw = engine_string_local

# load data
#mwe = pd.read_csv("data/dbtestdata_mwe1mio.csv")
mwe = pd.read_csv("/Users/schmidle/Documents/GIT-Projects/isewer/data_repo/data/RUEs/1_data_RU.csv")
################################
########CREATE TABLE AND LOAD DATA INTO TABLE USING SQLALCHEMY
################################
### make columns names lowercase
mwe.columns = map(str.lower,mwe.columns)
mwe.messdatum = pd.to_datetime(mwe.messdatum)


from sqlalchemy import create_engine

engine = create_engine(engine_string_rw)
# automatically creates table
# new table
#mwe.to_sql('winddaten', engine, index=False, if_exists="append")
# append to existing one (does not store date as date)
# use method=multi, way faster"
mwe.to_sql('strangberlin', engine, index=False,method="multi", if_exists="replace")
