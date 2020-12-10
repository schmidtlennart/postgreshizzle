import pandas as pd
import psycopg2
import sqlalchemy
import sys

# load data
data_RU = pd.read_csv("/Users/schmidle/Documents/GIT-Projects/isewer/data_analysis/data/RUEs/1_data_RU.csv")
#data_NSM = pd.read_csv("/Users/schmidle/Documents/GIT-Projects/isewer/data_analysis/data/RUEs/1_data_NSM.csv")

# # get db log-in credentials
exec(open('100_config_passwords.py').read())

################################
########CREATE TABLE AND LOAD DATA INTO TABLE USING SQLALCHEMY
################################

from sqlalchemy import create_engine
engine = create_engine(engine_string_adm) # or _rw

# to datetime for easier handling
data_RU.messdatum = pd.to_datetime(data_RU.messdatum, infer_datetime_format=True)   

# automatically creates table
# use method=multi, way faster"
# Split-up -> Think of stupid non-inclusive slicing!!
data_RU.iloc[0:1000000,:].to_sql('strang_berlin', engine, index=False,method="multi", if_exists="replace")
data_RU.iloc[1000000:2000000,:].to_sql('strang_berlin', engine, index=False,method="multi", if_exists="append")
data_RU.iloc[2000000:,:].to_sql('strang_berlin', engine, index=False,method="multi", if_exists="append")

len(data_RU)
################################
######## MWE
################################
# data_mwe = pd.read_csv("/Users/schmidle/Documents/GIT-Projects/isewer/data_analysis/data/RUEs/1_data_RU_mwe.csv")
# data_mwe.messdatum = pd.to_datetime(data_mwe.messdatum, infer_datetime_format=True)   
# data_mwe.to_sql('strang_berlin_mwe', engine, index=False,method="multi", if_exists="replace")