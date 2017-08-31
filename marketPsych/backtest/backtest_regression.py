# coding: utf-8

from backtestAnalytics import trmiAnalytics as ta
import sys
import os
import pandas as pd

# ARGUMENT
#  1: G5 or G20
#  2: CURRPAIR NAME
argvs=sys.argv
argc=len(argvs)
if argc != 4:
    print ('Usage: # python %s Target_Currency Number_of_Depth_for_DecisionTree start_from' % argvs[0])
    quit()

#group=argvs[1]
target=argvs[1]
numDepth=int(argvs[2])
startFrom=int(argvs[3])


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

dataSpan=300

# LOAD TARGET PRICE
prcDF = asys.loadData(pfile, ',')
prcLen = len(prcDF)
prcName = prcDF.columns.values

count = 0


accPL = 0
for i in range(0,startFrom - dataSpan + 1):
    prcArr = []
    for x in range(0,dataSpan):
        prcArr.append(prcDF.iloc[prcLen - startFrom + i + x])
    prc2DF = pd.DataFrame(prcArr, columns=prcName)

    # CONSTRUCT TRMI DataFrame
    fwdCorrTop = []
    count = 0
    for tfile in trmiFiles:
        trmiDF = asys.loadData(tfile, ',')
        asys.setTrmiAsset(trmiGroup[count])
        trmiName =trmiDF.columns.values

        # FIND SAME TIMESTAMP in TRMI DF as PRC DF
        trmiArr = []
        priceArr = []
        for y in range(0,len(prc2DF)):
            pKey = str(prc2DF['windowTimestamp'].iloc[y])
            trmiTmp = trmiDF.loc[trmiDF['windowTimestamp'] == pKey]
            if len(trmiTmp) > 0:
                trmiArr.append(trmiTmp.iloc[0])
                priceArr.append(prc2DF.iloc[y])
        prc3DF = pd.DataFrame(priceArr, columns=prcName)
        trmi2DF = pd.DataFrame(trmiArr, columns=trmiName)

        # OBTAIN FORWARD LOOKING CORRELATION INDICES
        #print (trmiGroup[count])
        #print (prc3DF['windowTimestamp'].iloc[len(prc3DF) - 1])
        fwdCorrArr = []
        fwdCorrArr = asys.getForwardLookingCorr(trmi2DF, prc3DF, 5)
        # print (fwdCorrArr[0])
        fwdCorrTop.extend(fwdCorrArr[0])
        count = count + 1

    # OBTAIN TOP 3 CORRELATION RANKING
    TopRank = sorted(fwdCorrTop, reverse=True)
    #print (TopRank[0])
    #print (TopRank[1])
    #print (TopRank[2])
    country = []
    indexname = []
    for k in range(0,3):
        country.append(TopRank[k][1])
        indexname.append(TopRank[k][2].split('-')[1])
    print (country)
    print (indexname)

    # OBTAIN LINEAR REGRESSION
    regression = asys.getLinearRegression(prc3DF, 5)

    # OBTAIN TARGET COUNRY'S INDICES
    trmiIndices = []
    for k in range(0,3):
        # LOAD TARGET CONTRY
        trmiDF = asys.loadData(trmiFiles[trmiGroup.index(country[k])], ',')
        # ADJUST TO TARGET RANGE
        trmiArr = []
        priceArr = []
        for y in range(0,len(prc2DF)):
            pKey = str(prc2DF['windowTimestamp'].iloc[y])
            trmiTmp = trmiDF.loc[trmiDF['windowTimestamp'] == pKey]
            if len(trmiTmp) > 0:
                trmiArr.append(trmiTmp.iloc[0])
                priceArr.append(prc2DF.iloc[y])
        prc3DF = pd.DataFrame(priceArr, columns=prcName)
        trmi2DF = pd.DataFrame(trmiArr, columns=trmiName)
        d = trmi2DF[indexname[k]]
        trmiIndices.append(d)

    # Macine Learning
    #print (prc3DF)
    ret = asys.getSupervisingData(prc3DF, trmiIndices[0], trmiIndices[1], trmiIndices[2], numDepth)
    lastTradePrc = prc3DF.iloc[len(prc3DF) - 1]['lastPrice']
    lastOpenPrc = prc3DF.iloc[len(prc3DF) - 1]['openPrice']
    lastWindowTime = prc3DF.iloc[len(prc3DF) - 1]['windowTimestamp']

    nextTradePrc = prcDF.iloc[prcLen - startFrom + dataSpan + i]['lastPrice']
    nextOpenPrc = prcDF.iloc[prcLen - startFrom + dataSpan + i]['openPrice']
    nextWindowTime = prcDF.iloc[prcLen - startFrom + dataSpan + i]['windowTimestamp']

    position = 0
    if ret > 0 and regression > 0:
        position = 1
    elif ret < 0 and regression < 0:
        position = -1
    else:
        position = 0
    pl = (nextTradePrc - lastTradePrc) * position
    accPL = accPL + pl

    print(str(nextWindowTime) + ',: Prediction = ,' + str(position) + ',===== Actual PL = ,' + str(pl) + ',===== Acumulative PL = ,' + str(accPL) + ',=====,' + str(lastTradePrc) + ',:,' + str(nextTradePrc), flush=True) 
