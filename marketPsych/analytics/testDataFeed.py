# coding: utf-8

from generateTrmiMatrix import genTrmiMatrix as trmi
from scipy.stats.stats import pearsonr
import pandas as pd
import statsmodels.formula.api as sm
from sklearn import linear_model as lm
import numpy as np
import math



# DELETING LAST UNNECESSARY COLUMNS
df = pd.read_csv("../sql/JP.trmi.ret", sep=',')
name = df.columns.values
df = df.drop( name[len(df.columns.str.contains('^Unnamed')) - 1],1)
name = df.columns.values

dfp = pd.read_csv("../sql/JPY.prc.ret", sep=',')
namep = dfp.columns.values
dfp = dfp.drop( namep[len(dfp.columns.str.contains('^Unnamed')) - 1],1)
namep = dfp.columns.values

# DATA MATCHING BY windowTimestamp!!
timeTrmi= df['windowTimestamp']
timePrice=dfp['windowTimestamp']
trmiTimeMap = {}
priceTimeMap = {}

# CREATE KEY VALUE MAP key = Time, Item = SEQ NUM on windowTimestamp
for n in range( 0, len(timeTrmi) ):
    trmiTimeMap[timeTrmi[n]] = n
for n in range( 0, len(timePrice) ):
    priceTimeMap[timePrice[n]] = n
print ('Num trmiTime ==> ' + str(len(trmiTimeMap)))
print ('Num priceTime ==> ' + str(len(priceTimeMap)))

# SPECIFY windowTimestamp which is covered in TRMI dataframe (based on proce dataframe)
# Then eliminate dupplicate TRMI record
trmiRows = []
priceRows = []
for pKey, pItem in priceTimeMap.items():
    if pKey in trmiTimeMap:
        trmiRows.append(trmiTimeMap[pKey])
        priceRows.append(pItem)
trmiRows.sort()
priceRows.sort()

# RECONSTRUCT TRMI DATAFRAME based on matching windowTimeFrame
df2list = []
for n in range(0, len(trmiRows)):
    #df2.append(df.iloc[trmiRows[n]], ignore_index = True, verify_integrity = False)
    arr = []
    for m in range(0, len(df.iloc[trmiRows[n]])):
        #print (name[m])
        arr.append(df.iloc[trmiRows[n]][m] )
    df2list.append(arr)
df2=pd.DataFrame(df2list,columns=name)
print (df2)

# RECONSTRUCT PRICE DATAFRAME based on matching windowTimeFrame
df3list = []
for n in range(0, len(priceRows)):
    arr = []
    for m in range(0, len(dfp.iloc[priceRows[n]])):
        arr.append(dfp.iloc[priceRows[n]][m] )
    df3list.append(arr)
df3=pd.DataFrame(df3list,columns=namep)
print (df3)


### MAIN PROCESSING
numPrice=len(timePrice)
  
data1 = df2['windowTimestamp']
data2 = df3['lastPrice']
sizeRaw=len(data1)

# SETUP TIME SERIES SEQ NUMBER in DATAFRAME
df2['numraw'] = list(range(1,sizeRaw+1))
df3['numraw'] = list(range(1,sizeRaw+1))

# OBTAIN COLUMN LIST
name = df2.columns.values
isCalc = 0
for n in range(0,len(name) - 1):
    if name[n] == 'buzz':
        isCalc = 1
    if isCalc == 1:
        datat=df2[name[n]] # OBTAIN TRMI DATA ON THE SPECIFIC COLUMN
        p = pearsonr(datat, data2) # CALCULATE CORELATION COEFFICIENT
        if math.isnan(p[0]) == False:
            tmp = name[n] + ":CORRELATION WITH PRICE = " + str(p[0])
            print(tmp)

# CORELATION in B/W data1 and data2

#p = pearsonr(data1,data2)
#print (p[0])

# LINEAR REGRESSION
#tmSeries = df['numraw']
#model=sm.ols( formula="joy ~ numraw",data=df).fit()
#print (model.params)
#print (model.summary())






