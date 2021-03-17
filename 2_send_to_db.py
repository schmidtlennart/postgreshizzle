import pandas as pd
import psycopg2
import sys

# MWE or full dataset?
mwe = True #True,False

# get db log-in credentials
exec(open('100_config_passwords.py').read())
#if local
#engine_string_rw = engine_string_local
# if admin on ufz postgres
eng_str = engine_string_adm

# load data
if mwe:
    data = pd.read_csv("/Users/schmidle/Documents/GIT-Projects/isewer/data/1_data_RU_mwe.csv")
else:
    data = pd.read_csv("/Users/schmidle/Documents/GIT-Projects/isewer/data/1_data_RU.csv")
################################
########CREATE TABLE AND LOAD DATA INTO TABLE USING SQLALCHEMY
################################
### make columns names lowercase
data.columns = map(str.lower,data.columns)
data.messdatum = pd.to_datetime(data.messdatum)

from sqlalchemy import create_engine
engine = create_engine(eng_str,executemany_mode='values',executemany_values_page_size=10000, executemany_batch_page_size=5000)
# automatically creates table
# new table
#mwe.to_sql('winddaten', engine, index=False, if_exists="append")
# append to existing one (does not store date as date)
# use method=multi, way faster"
if mwe:
    data.to_sql('strang_berlin_mwe', engine, index=False,method="multi", if_exists="replace")
else:
    data.to_sql('strang_berlin', engine, index=False,method="multi", if_exists="replace")
 