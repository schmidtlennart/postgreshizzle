import pandas as pd
### OLD: GET DATA FROM DWD DATASETS
dataname = "df1718"

### data with locations
data_all = pd.read_feather("/Users/schmidle/Documents/GIT-Projects/dwdproto/data/norddeutschland/"+dataname+"_tidy.feather")
data_all = data_all.drop(["index","ID","Station","DD_QB","FF_QB","FF_MAX_MW_QB","FF_WS_QB","DD_WS_QB"], axis=1)#remove quality byte columns
print(list(data_all.columns))
data_all.to_csv("data/dbtestdata.csv")
# not quite sure if this is what I did to get to dbtestdata


### READ AND CREATE MWE
dt = pd.read_csv("data/dbtestdata.csv")# Load full dataset without quality bytes
dt["MESSDATUM"] = pd.to_datetime(dt["MESSDATUM"])
# set index
dt = dt.set_index("MESSDATUM")
#drop unwanted column
dt = dt.drop("Unnamed: 0",axis=1)
dt = dt.drop("FX_QB",axis=1)
dt.columns
dt.to_csv("data/dbtestdata.csv")
# save without header too
dt.to_csv("data/dbtestdata_nh.csv", header=False, index=False)

### Create mwe
len(dt)
mwe = dt.iloc[:100]

mwe.to_csv("data/dbtestdata_mwe.csv")
mwe.to_csv("data/dbtestdata_mwe_nh.csv", header=False, index=False)

# create half-sized mwe (1 mio) - or, as before, 0.5 mio etc.
mwe2 = dt.iloc[:1000000]
mwe2.to_csv("data/dbtestdata_mwe1mio.csv")
