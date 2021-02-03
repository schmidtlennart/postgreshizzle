### FIRST ANALYSIS OF SAMPLE DATA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = "/Users/schmidle/OneDrive/i-SEWER/AP3_Prototyp - konzeptioneller digitaler Zwilling/1_Bestandsaufnahme/3.1.2 Datenverfügbarkeit/Prozessierte_daten/Datenexport_bnn/Export_clean_header.csv"
path_meta = "/Users/schmidle/OneDrive/i-SEWER/AP3_Prototyp - konzeptioneller digitaler Zwilling/1_Bestandsaufnahme/3.1.2 Datenverfügbarkeit/Prozessierte_daten/Datenexport_bnn/RUEs_StrangBerlin.csv"

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

##############################
### Corrections: Duplicates, missing values, outliers based on data validation
##############################
# duplicates in timestamps
dups = data.DateTime.duplicated()
dups.sum()#120 duplicates in timestamps
#remove
data1 = data.copy().loc[~dups,:]

# extraordinarily high values in Hindenburgstr
data1["RU_Hindenburgstrasse"].loc[data1["RU_Hindenburgstrasse"]>4,] = np.nan


##############################
### Wide to long format # Add auxiliary information
##############################
# RU: drop NSMs
data_RU = data1.loc[:,~data1.columns.str.contains("NSM")].copy()
# NSM: drop RUs
data_NSM = data1.loc[:,~data1.columns.str.contains("RU_")].copy()

# RU: calculate % and add as column
# % of schwelle and % of overall volume
# static: height of schwelle, maximum height possible and schwellenhöhe as percent of that maximum value (from excel file)
schwellenhoehen = {'BerlinerAllee':1.75,'Hindenburgstrasse':1.32,'Uferstrasse':2.44}
maxhoehen = {'BerlinerAllee':4.52,'Hindenburgstrasse':3.57,'Uferstrasse':5.23}
schwellenhoehen_per_m = {'BerlinerAllee':38.72,'Hindenburgstrasse':36.98,'Uferstrasse':46.65}

fig, axs = plt.subplots(1,3,figsize=(10,6))
axs = axs.flatten()
for i,col in enumerate(schwellenhoehen.keys()):
    print(i)
    # construct names
    name_per_s = "PER_S_RU_"+col#dynamic: measured height as percent of schwellenhöhe
    name_per_m = "PER_M_RU_"+col#dynamic: measured height as percent of maximum height
    # get respective value
    value_schw = schwellenhoehen[col]
    value_max = maxhoehen[col]
    #calculate percent
    data_RU[name_per_s] = data_RU["RU_"+col]/value_schw*100 #dynamic: measured height as percent of schwellenhöhe
    data_RU[name_per_m] = data_RU["RU_"+col]/value_max*100 #dynamic: measured height as percent of maximum height
    #plot for verification
    axs[i].plot(data_RU["RU_"+col],data_RU[name_per_s],label="Percent of Schwelle")
    axs[i].plot(data_RU["RU_"+col],data_RU[name_per_m],label="Percent of Max")
    axs[i].set(xlabel="Niveau [m]",ylabel="Niveau [%]",title=col,ylim=(0,165))
    # add schwellenhöhe in percent and 100% hlines
    axs[i].axhline(schwellenhoehen_per_m[col],label="Schwellenhöhe as percent of Max",linestyle='--',c="grey")
    axs[i].axhline(100, color='black', linestyle='--')

axs[i].legend()
# Does this make sense?
plt.tight_layout()
#plt.show()
fig.savefig("plots/true_vs_percent.png")


# wide to long transformation
data_RU_out = pd.wide_to_long(data_RU,stubnames=["RU_","PER_S_RU_","PER_M_RU_"],i="DateTime",j="RUEB", suffix="\w+")
data_NSM_out = pd.wide_to_long(data_NSM,stubnames=["NSM"],i="DateTime",j="Messstation")                                                 

data_RU_out = data_RU_out.reset_index()
data_NSM_out = data_NSM_out.reset_index()

# percent values correct/check ranges
data_RU_out.groupby("RUEB").agg(["min","max"])

# Add static values (maximmum level, schwellenhöhe etc.)
data_RU_out["SCHW"] = data_RU_out.RUEB.map(schwellenhoehen)#static: Schwellenhöhe in m
data_RU_out["SCHW_PER_M"] = data_RU_out.RUEB.map(schwellenhoehen_per_m)#static: Schwellenhöhe in % of maximalhöhe
data_RU_out["MAX"] = data_RU_out.RUEB.map(maxhoehen)#static: maximalhöhe in m
data_RU_out["MAX_PER_M"] = 100#static: maximalhöhe in % = 100 (for plotting)

#### Add coord to RU-data
# rename in metadata for merge
coord_dict = {"B 31 A AUTOBAHNZUBRINGER MITTE":'BerlinerAllee',"HINDENBURGSTR":'Hindenburgstrasse',"UFERSTR":'Uferstrasse'}
metadata.STRASSENNA = metadata.STRASSENNA.map(coord_dict)
# merge
data_RU_out = data_RU_out.merge(metadata[["STRASSENNA","xcoord","ycoord"]],"left",left_on="RUEB",right_on="STRASSENNA").drop("STRASSENNA",1)

# rename
data_RU_out.columns = ["messdatum","rueb","niveau","niveau_per_s","niveau_per_m","schwelle","schwelle_per","max","max_per","xcoord","ycoord"]
data_NSM.columns = ['messdatum', 'NSM1', 'NSM2', 'NSM3', 'NSM4', 'NSM5', 'NSM6', 'NSM7','NSM8']
# save
data_RU_out.to_csv("/Users/schmidle/Documents/GIT-Projects/isewer/data_repo/data/RUEs/1_data_RU.csv",index=False)
data_NSM.to_csv("/Users/schmidle/Documents/GIT-Projects/isewer/data_repo/data/RUEs/1_data_NSM.csv",index=False)

### CREATE MWE AND SAVE
data_RU_out.messdatum = pd.to_datetime(data_RU_out.messdatum, infer_datetime_format=True)   
data_NSM.messdatum = pd.to_datetime(data_NSM.messdatum, infer_datetime_format=True)   

# create mwe
data_mwe = data_RU_out.set_index("messdatum")#for slicing
data_mwe_nsm = data_NSM.set_index("messdatum")#for slicing

# NSM: select time period with more values
data_mwe_nsm.groupby()

data_mwe = data_mwe.loc["2018-11-16 16:15:11":"2018-11-30 16:15:11"].reset_index()
data_mwe_nsm2 = data_mwe_nsm.loc["2018-11-16 16:15:11":"2018-11-30 16:15:11"].reset_index()

ax = data_mwe_nsm2.NSM1.plot()


data_mwe.to_csv("/Users/schmidle/Documents/GIT-Projects/isewer/data_repo/data/RUEs/1_data_RU_mwe.csv",index=False)

len(data_mwe)