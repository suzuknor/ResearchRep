# coding: utf-8

from trmiAnalytics import trmiAnalytics as ta
import sys
import os
import pandas as pd

# ARGUMENT
#  1: G5 or G20
#  2: CURRPAIR NAME
argvs=sys.argv
argc=len(argvs)
if argc != 3:
    print ('Usage: # python %s Target_Currency Number_of_Depth_for_DecisionTree' % argvs[0])
    quit()

#group=argvs[1]
target=argvs[1]
numDepth=argvs[2]


trmiFiles = []
trmiGroup = []


trmiFiles = ['../sql/JP.trmi.ret', '../sql/US.trmi.ret', '../sql/FR.trmi.ret', '../sql/GB.trmi.ret', '../sql/DE.trmi.ret','../sql/CN.trmi.ret', '../sql/CA.trmi.ret','../sql/CL.trmi.ret', '../sql/BR.trmi.ret', '../sql/AU.trmi.ret', '../sql/EG.trmi.ret', '../sql/IN.trmi.ret', '../sql/IR.trmi.ret', '../sql/IQ.trmi.ret', '../sql/IL.trmi.ret', '../sql/IT.trmi.ret', '../sql/LY.trmi.ret', '../sql/MX.trmi.ret', '../sql/KP.trmi.ret', '../sql/RU.trmi.ret', '../sql/ZA.trmi.ret', '../sql/CH.trmi.ret']
trmiGroup=['JP', 'US', 'FR', 'GB', 'DE', 'CN', 'CA','CL', 'BR', 'AU', 'EG', 'IN', 'IR', 'IQ', 'IL', 'IT', 'LY', 'MX', 'KP', 'RU', 'ZA', 'CH']


if target == "JPY":
    pfile='../sql/JPY.prc.ret'
elif target == "EURJPY":
    pfile='../sql/EURJPY.prc.ret'
elif target == "GBPJPY":
    pfile='../sql/GBPJPY.prc.ret'
elif target == "CHFJPY":
    pfile='../sql/CHFJPY.prc.ret'
elif target == "AUDJPY":
    pfile='../sql/AUDJPY.prc.ret'
elif target == "NZDJPY":
    pfile='../sql/NZDJPY.prc.ret'
elif target == "CADJPY":
    pfile='../sql/CADJPY.prc.ret'
else:
    print ("No such currency pair supported")
    sys.exit()

topRank = []
btmRank = []
frdTopRank = []
frdBtmRank = []
count=0
asys = ta()
for tfile in trmiFiles:
    print (tfile)
    if asys.setPriceData(pfile) == False:
        print ("Price file NG")
        sys.exit()

    if asys.setTrmiData(tfile) == False:
        print ("Trmi file NG")
        sys.exit()

    asys.setTrmiAsset(trmiGroup[count])

    mats=[]

    mats=asys.validateData()

    # REGULAR CORR
    arr = []
    arr=asys.getRegularCorr(mats[0], mats[1])

    # FORWARD LOOKING CORR
    frdarr = []
    frdarr = asys.getForwardLookingCorr(mats[0], mats[1], 5)

    topRank.extend(arr[0])
    btmRank.extend(arr[1])

    frdTopRank.extend(frdarr[0])
    frdBtmRank.extend(frdarr[1])

    count = count + 1
rank = sorted(topRank)
btm = []
for n in range(0,10):
    btm.append(rank[n])
numRank = len(rank)
colNames=['Correlation','Country Code','Index']
df1=pd.DataFrame(btm, columns=colNames)

top = []
rank = sorted(topRank, reverse=True)
for n in range(0,10):
    top.append(rank[n])
df2=pd.DataFrame(top, columns=colNames)

btm = []
rank = sorted(frdTopRank)
for n in range(0,10):
    btm.append(rank[n])
df3=pd.DataFrame(btm, columns=colNames)

top = []
rank = sorted(frdTopRank, reverse=True)
for n in range(0,10):
    top.append(rank[n])
df4=pd.DataFrame(top, columns=colNames)



df1.to_csv('../data/' + target + '_COU_NEG_CORR.csv', index=False)
df2.to_csv('../data/' + target + '_COU_POS_CORR.csv', index=False)

df3.to_csv('../data/' + target + '_COU_NEG_CORR_FRD.csv', index=False)
df4.to_csv('../data/' + target + '_COU_POS_CORR_FRD.csv', index=False)

asys.getLinearRegression(mats[1])

country = []
indexname = []
cou = df4['Country Code']
indx = df4['Index']
for i in range(6,9): #TOP 3
    country.append(cou[i])
    indexname.append(indx[i].split('-')[1])
trmiArr = []
for i in range(3,6):
    idnum = trmiGroup.index(country[i-6])
    print (trmiFiles[idnum])
    asys.setPriceData(pfile)
    asys.setTrmiData(trmiFiles[idnum])
    asys.setTrmiAsset(country[i-6])
    arr = asys.validateData()
    d = arr[0][indexname[i-6]]
    trmiArr.append(d)


asys.getSupervisingData(mats[1], trmiArr[0], trmiArr[1], trmiArr[2], numDepth) # TOP 3









