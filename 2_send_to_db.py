import pandas as pd
import psycopg2
import sys

# load data
mwe = pd.read_csv("data/dbtestdata_mwe2.csv")

################################
########CREATE TABLE AND LOAD DATA INTO TABLE USING SQLALCHEMY
################################
### make columns names lowercase
mwe.columns = map(str.lower,mwe.columns)
mwe.messdatum = pd.to_datetime(mwe.messdatum)

from sqlalchemy import create_engine
engine = create_engine('postgresql://isewer_adm:B!!irkenbr0t@postgres:5432/isewer')
# automatically creates table
# new table
#mwe.to_sql('winddaten', engine, index=False, if_exists="append")
# append to existing one (does not store date as date)
# use method=multi, way faster"
mwe.to_sql('winddaten_1mio', engine, index=False,method="multi", if_exists="append")


mwe.messdatum.min()
mwe.messdatum.max()
