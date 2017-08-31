# coding: utf-8

## trmiAnalytics Python module
#  2017 07 07
#  Noriyuki Suzuki / Market Development Manager / Thomson Reuters
#  Class: trmiAnalytics
#  Method:
#     1: setPriceData: importing price history and put it into pandas dataframe object
#     2: setTrmiData:  importing trmi history and put it into pandas dataframe object
#     3: ValidateData: Validate (matching) data using windowTimestamp on both price and trmi data
#     4: getCorr:      Obtain Correlation ranking
#     5: getForwardLookingCorr:    Obtain Forward Looking Correlation ranking
import os
from scipy.stats.stats import pearsonr
import pandas as pd
import statsmodels.formula.api as sm
from sklearn import linear_model as lm
from sklearn import tree
import numpy as np
import math

class trmiAnalytics:
    _priceFilePath = ''
    _trmiFilePath = ''
    _trmiAssetCode = ''

    def setPriceData(self, pFilePath):
        self._priceFilePath = pFilePath
        return os.path.exists(self._priceFilePath)
    def setTrmiData(self, tFilePath):
        self._trmiFilePath = tFilePath
        return os.path.exists(self._trmiFilePath)
    def setTrmiAsset(self, assetCode):
        self._trmiAssetCode = assetCode

    def validateData(self):
        ### TRMI DATA LOAD and DROP empty columns
        dft = pd.read_csv(self._trmiFilePath, sep=',')
        namet = dft.columns.values
        dft = dft.drop( namet[len(dft.columns.str.contains('^Unnamed')) - 1],1)
        namet = dft.columns.values

        ### PRICE DATA LOAD and DROP empty columns
        dfp = pd.read_csv(self._priceFilePath, sep=',')
        namep = dfp.columns.values
        dfp = dfp.drop( namep[len(dfp.columns.str.contains('^Unnamed')) - 1],1)
        namep = dfp.columns.values

        ### EXTRACT windowTimestamp from both TRMI and PRICE DATA
        timeTrmi= dft['windowTimestamp']
        timePrice=dfp['windowTimestamp']

        ### CREATE KEY VALUE MAPS: KEY=windowTimestamp, ITEM=SEQ NUMBER
        trmiTimeMap = {}
        priceTimeMap = {}
        for n in range( 0, len(timeTrmi) ):
            trmiTimeMap[timeTrmi[n]] = n
        for n in range( 0, len(timePrice) ):
            priceTimeMap[timePrice[n]] = n

        ### SPECIFY windowTimeStamp to cover timestamp in both TRMI and PRICE DATA (refering PRICE as primary)
        trmiRows = []
        priceRows = []
        for pKey, pItem in priceTimeMap.items(): ## Using priceTimeMap iterator
            if pKey in trmiTimeMap:
                trmiRows.append(trmiTimeMap[pKey])
                priceRows.append(pItem)
        trmiRows.sort()
        priceRows.sort()

        ### RE-CONSTRUCT TRMI and PRICE DataFrame using raw seq number in xxxRows
        dftlist = []
        dfplist = []

        for n in range(0, len(trmiRows)):
            arr = []
            for m in range(0, len(dft.iloc[trmiRows[n]])):
                arr.append(dft.iloc[trmiRows[n]][m])
            dftlist.append(arr)
        dft2 = pd.DataFrame(dftlist, columns=namet)

        for n in range(0, len(priceRows)):
            arr = []
            for m in range(0, len(dfp.iloc[priceRows[n]])):
                arr.append(dfp.iloc[priceRows[n]][m])
            dfplist.append(arr)
        dfp2 = pd.DataFrame(dfplist, columns=namep)

        return [dft2, dfp2]

    def getRegularCorr(self, dft2, dfp2):
        name = dft2.columns.values
        datap = dfp2['lastPrice']
        isCalc = 0
        rankArr = []
        for n in range(0, len(name) - 1):
            arr = []
            if name[n] == 'sentiment':
                isCalc = 1
            if isCalc == 1:
                datat = dft2[name[n]]
                p = pearsonr(datat, datap)
                if math.isnan(p[0]) == False:
                    arr.append(p[0])
                    arr.append(self._trmiAssetCode)
                    arr.append(self._trmiAssetCode + '-' + name[n])
                    rankArr.append(arr)

        return [sorted(rankArr,reverse=True), sorted(rankArr)]

    def getForwardLookingCorr(self, df3, df4, numForward):
        trmiNumRow = len(df3['windowTimestamp'])
        priceNumRow = len(df4['windowTimestamp'])
        namet = df3.columns.values
        namep = df4.columns.values

        dftlist = []
        dfplist = []
        for n in range(numForward, trmiNumRow):
            arr = []
            for m in range(0, len(df3.iloc[n])):
                arr.append(df3.iloc[n][m])
            dftlist.append(arr)
        df5 = pd.DataFrame(dftlist, columns=namet)

        for n in range(0, priceNumRow - numForward):
            arr = []
            for m in range(0, len(df4.iloc[n])):
                arr.append(df4.iloc[n][m])
            dfplist.append(arr)
        df6 = pd.DataFrame(dfplist, columns=namep)
        
        return self.getRegularCorr(df5, df6)

    def getLinearRegression(self, dfp):

        clf = lm.LinearRegression()
        X = []
        for i in range(1, len(dfp) + 1):
            x = []
            x.append(i)
            X.append(x)

        Y = dfp.loc[:, ['lastPrice']].as_matrix()
        clf.fit(X,Y)
        print (clf.coef_[0][0])
        print (clf.intercept_[0])
        p = pearsonr(X,Y)
        print (p[0][0])

    def getSupervisingData(self, dfp, dft1, dft2, dft3, numDepth):
        # Test period = 10
        tPeriod = 30
        print (numDepth)
        # SUPPERVISOR DATA CREATION
        X = []
        sSize = len(dfp)
        P = []
        P = dfp['lastPrice']
        for i in range(1,sSize):# - tPeriod):
            if P[i] > P[i - 1]:
                X.append(1)
            elif P[i] == P[i - 1]:
                X.append(0)
            else:
                X.append(-1)


        # LEARNING DATA CREATION
        sSize = len(dft1)
        T = []
        for i in range(0,sSize-1):# - tPeriod):
            arr = []
            arr.append(dft1[i])
            arr.append(dft2[i])
            arr.append(dft3[i])
            T.append(arr)

        # Decision Tree Instance Creation
        clf = tree.DecisionTreeClassifier(max_depth=int(numDepth))
        clf = clf.fit(T,X)

        # Test Model
        T = []
        #for i in range(sSize - 1 - tPeriod, sSize - 1):
        for i in range(0, sSize - 1):
            arr = []
            arr.append(dft1[i])
            arr.append(dft2[i])
            arr.append(dft3[i])
            T.append(arr)
        
        predicted = clf.predict(T)
        Y = []
        for i in range(sSize - tPeriod, sSize):
            if P[i] > P[i - 1]:
                Y.append(1)
            elif P[i] == P[i - 1]:
                Y.append(0)
            else:
                Y.append(-1)
        print (X)
        print (predicted)
        print (sum( (predicted == X) / len(X)) )



