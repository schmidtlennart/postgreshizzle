### FIRST ANALYSIS OF SAMPLE DATA


import pandas as pd
import numpy as np


path = "/Users/schmidle/Documents/GIT-Projects/isewer/data_analysis/data/RUEs/Export_clean_header.csv"
path_meta = "/Users/schmidle/Documents/GIT-Projects/isewer/data_analysis/data/RUEs/RUEs_StrangBerlin.csv"

data = pd.read_csv(path,encoding = "ISO-8859-1", sep=";",decimal=",")
metadata = pd.read_csv(path_meta,sep=",")

##############################
### Data Preparation
##############################
# drop unnecessary columns (all with "type" and some other)
drop1 = data.columns.str.contains("type")
drop2 = ["DaylightSavingTime","Millisecond"]
data = data.loc[:,~drop1]
data = data.drop(drop2,axis=1)

# Rename RU-columns for wide to long-operation
#RU_dict = {"RU_Uferstrasse":"RU1", "RU_BerlinerAllee":"RU2", "RU_Hindenburgstrasse":"RU3"}
#data.rename(columns=RU_dict, inplace=True)

##############################
### Analysis: Duplicates, missing values
##############################
# n missing values in %
data.isna().sum()/len(data)*100# 0.1 + 1.2% for RUs, all N-sensors >80%

# duplicates in timestamps?
dups = data.DateTime.duplicated()
dups.sum()#120 duplicates in timestamps
#remove
data1 = data.copy().loc[~dups,:]


##############################
### Wide to long format # Add auxiliary information
##############################
# RU: drop NSMs
data_RU = data1.loc[:,~data1.columns.str.contains("NSM")].copy()
# NSM: drop RUs
data_NSM = data1.loc[:,~data1.columns.str.contains("RU_")].copy()

# wide to long transformation
data_RU = pd.wide_to_long(data_RU,stubnames=["RU_"],i="DateTime",j="RÜB", suffix="\w+")
data_NSM = pd.wide_to_long(data_NSM,stubnames=["NSM"],i="DateTime",j="Messstation")

data_RU = data_RU.reset_index()
data_NSM = data_NSM.reset_index()
#### Add coord to RU-data
# rename in metadata for merge
coord_dict = {"B 31 A AUTOBAHNZUBRINGER MITTE":'BerlinerAllee',"HINDENBURGSTR":'Hindenburgstrasse',"UFERSTR":'Uferstrasse'}
metadata.STRASSENNA = metadata.STRASSENNA.map(coord_dict)
# merge
data_RU = data_RU.merge(metadata[["STRASSENNA","xcoord","ycoord"]],"left",left_on="RÜB",right_on="STRASSENNA").drop("STRASSENNA",1)

# rename
data_RU.columns = ["messdatum","rueb","niveau","xcoord","ycoord"]

# save
data_RU.to_csv("/Users/schmidle/Documents/GIT-Projects/isewer/data_analysis/data/RUEs/1_data_RU.csv",index=False)
data_NSM.to_csv("/Users/schmidle/Documents/GIT-Projects/isewer/data_analysis/data/RUEs/1_data_NSM.csv",index=False)


### SOME ANALYSIS
data_RU.messdatum = pd.to_datetime(data_RU.messdatum, infer_datetime_format=True)   
#min, max of date, unit of niveau?
data_RU.groupby("rueb").agg([min,max])
#NOTES:
# All timeseries range: 2018-11-16 16:15:11' - ‘2020-11-16 16:15:10’
# But niveau-minmax vaires largely (2.7/3 vs 43 (Hindeburgstr))


### CREATE MWE AND SAVE
data_RU.messdatum = pd.to_datetime(data_RU.messdatum, infer_datetime_format=True)   

# create mwe

data_mwe = data_RU.set_index("messdatum")#for slicing
data_mwe = data_mwe.loc["2018-11-16 16:15:11":"2018-11-30 16:15:11"].reset_index()
data_mwe.to_csv("/Users/schmidle/Documents/GIT-Projects/isewer/data_analysis/data/RUEs/1_data_RU_mwe.csv",index=False)

len(data_mwe)
