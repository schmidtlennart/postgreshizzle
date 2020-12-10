import pandas as pd
import psycopg2
import sys

# get db log-in credentials
exec(open('100_config_passwords.py').read())


# load data
#mwe = pd.read_csv("data/dbtestdata_mwe1mio.csv")
mwe = pd.read_csv("data/dbtestdata_mwe100.csv")
################################
########CREATE TABLE AND LOAD DATA INTO TABLE USING SQLALCHEMY
################################
### make columns names lowercase
mwe.columns = map(str.lower,mwe.columns)
#mwe.messdatum = pd.to_datetime(mwe.messdatum)


from sqlalchemy import create_engine
engine = create_engine(engine_string_rw)
# automatically creates table
# new table
#mwe.to_sql('winddaten', engine, index=False, if_exists="append")
# append to existing one (does not store date as date)
# use method=multi, way faster"
mwe.to_sql('winddaten_test2', engine, index=False,method="multi", if_exists="append")

mwe.dtypes

sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint "winddaten_test2_pkey"
DETAIL:  Key (messdatum)=(09:50:00) already exists.