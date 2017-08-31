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

dataSpan=500

# LOAD TARGET PRICE
prcDF = asys.loadData(pfile, ',')
prcLen = len(prcDF)
prcName = prcDF.columns.values

count = 0


accPL = 0
for i in range(prcLen - startFrom - dataSpan + 1,prcLen - dataSpan + 1,dataSpan):
    # PRICE DATAFRAME CONSTRUCTION IN THE SPECIFIED RANGE
    prc2DF = prcDF[i:i + dataSpan]

    # TRMI DATAFRAME CONSTRUCTION IN THE SPECIFIC RANGE
    count = 0
    fwdCorrTop = []
    for tfile in trmiFiles:
        # LOAD TRMI FILES
        trmiDF = asys.loadData(tfile, ',')
        asys.setTrmiAsset(trmiGroup[count])
        trmiName =trmiDF.columns.values

        trmiArr = []
        priceArr = []
        for j in range(0,len(prc2DF)):
            # KET = windowTimeStamp in prc2DF2
            pKey = str(prc2DF['windowTimestamp'].iloc[j])
            # FIND TARGET windowTimestamp in TRMI DATAFRAME
            trmiTmp = trmiDF.loc[trmiDF['windowTimestamp'] == pKey]
            if len(trmiTmp) > 0: # FOUND TARGET windowTimestamp in TRMI DATAFRAME
                trmiArr.append(trmiTmp.iloc[0])
                priceArr.append(prc2DF.iloc[j])

        # RECONSTRUCT PRICE AND TRMI DATA FRAME WHICH IS TOTALLY MATCHING BY windowTimestamp
        prc3DF = pd.DataFrame(priceArr, columns=prcName)
        trmi2DF = pd.DataFrame(trmiArr, columns=trmiName)

        # OBTAIN FORWARD LOOKING CORRELATION INDICES
        fwdCorrArr = []
        fwdCorrArr = asys.getForwardLookingCorr(trmi2DF, prc3DF,5)
        fwdCorrTop.extend(fwdCorrArr[0])
        count = count + 1
        # END OF LOOP tfile

    TopRank = sorted(fwdCorrTop, reverse=True)
    country = []
    indexname = []
    for k in range(0,3):
        country.append(TopRank[k][1])
        indexname.append(TopRank[k][2].split('-')[1])


    # OBTAIN TOP 3 CORRELATION INDICES
    trmiIndices = []
    for k in range(0,3):
        trmiTmp = asys.loadData(trmiFiles[trmiGroup.index(country[k])],',')
        trmiIndices.append(trmiTmp)

    prcDF1 = prcDF[i:i + (2 * dataSpan)]
    # windowTimestam MATCHING b/w prcDF1 and TOP 3 TRMI Correlated index
    trmiArr1 = []
    trmiArr2 = []
    trmiArr3 = []
    priceArr = []
    for j in range(0,len(prcDF1)):
        # KET = windowTimeStamp in prcDF1                                                                  
        pKey = str(prcDF1['windowTimestamp'].iloc[j])
        # FIND TARGET windowTimestamp in TRMI DATAFRAME                                                     
        trmiTmp1 = trmiIndices[0].loc[trmiDF['windowTimestamp'] == pKey]
        trmiTmp2 = trmiIndices[1].loc[trmiDF['windowTimestamp'] == pKey]
        trmiTmp3 = trmiIndices[2].loc[trmiDF['windowTimestamp'] == pKey]
        if len(trmiTmp1) > 0: # FOUND TARGET windowTimestamp in TRMI DATAFRAME                               
            trmiArr1.append(trmiTmp1.iloc[0])
            trmiArr2.append(trmiTmp2.iloc[0])
            trmiArr3.append(trmiTmp3.iloc[0])
            priceArr.append(prcDF1.iloc[j])

    # RECONSTRUCT PRICE AND TRMI DATA FRAME WHICH IS TOTALLY MATCHING BY windowTimestamp                    
    prcDF2 = pd.DataFrame(priceArr, columns=prcName)
    trmiDF1 = pd.DataFrame(trmiArr1, columns=trmiName)
    trmiDF2 = pd.DataFrame(trmiArr2, columns=trmiName)
    trmiDF3 = pd.DataFrame(trmiArr3, columns=trmiName)

    dataLen = len(prcDF2)
    # STUDY
    prc = prcDF2[0:dataSpan]
    trmi1 = trmiDF1[0:dataSpan][indexname[0]]
    trmi2 = trmiDF2[0:dataSpan][indexname[1]]
    trmi3 = trmiDF3[0:dataSpan][indexname[2]]

    ret = asys.getSupervisingData(prc,trmi1,trmi2,trmi3,numDepth,-1)
    lastTradePrice = prcDF2.iloc[dataSpan - 1]['lastPrice']
    nextTradePrice = prcDF2.iloc[dataSpan]['lastPrice']
    lastWindowTime = prcDF2.iloc[dataSpan- 1]['windowTimestamp']
    nextWindowTime = prcDF2.iloc[dataSpan]['windowTimestamp']
    pl = (nextTradePrice - lastTradePrice) * ret
    accPL = accPL + pl
    print (str(nextWindowTime) + ',' + str(ret) + ',' + str(pl) + ',' + str(accPL) + ',' + str(lastTradePrice) + ',' + str(nextTradePrice))
    for x in range(dataSpan, dataLen-1):
        prc = prcDF2[0:x+1]
        trmi1 = trmiDF1[0:x+1][indexname[0]]
        trmi2 = trmiDF2[0:x+1][indexname[1]]
        trmi3 = trmiDF3[0:x+1][indexname[2]]
        ret = asys.getSupervisingData(prc,trmi1,trmi2,trmi3,numDepth,-1)
        lastTradePrice = prcDF2.iloc[x]['lastPrice']
        nextTradePrice = prcDF2.iloc[x+1]['lastPrice']
        lastWindowTime = prcDF2.iloc[x]['windowTimestamp']
        nextWindowTime = prcDF2.iloc[x+1]['windowTimestamp']
        pl = (nextTradePrice - lastTradePrice) * ret
        accPL = accPL + pl
        print (str(nextWindowTime) + ',' + str(ret) + ',' + str(pl) + ',' + str(accPL) + ',' + str(lastTradePrice) + ',' + str(nextTradePrice))

    
