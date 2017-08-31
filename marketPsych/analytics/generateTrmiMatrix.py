# coding: utf-8

### Generating Data Matrix (in Signal) from TRMI Raw Data
from trmiDateTime import convert2TrmiDateTime as dtmi


# In[1]:

### Class for Generate Data Matrix (in signal) from TRMI Raw Data
class genTrmiMatrix:
    _filepath = ''
    _dataType = 'News_Social'
    _mat = []
    
    def setFilePath(self,filePath):
        self._filepath = filePath
        
    def setDataType(self,dataType):
        self._dataType = dataType
        
    def load2Matrix(self):
        _dtmi = dtmi()
        _isHeader = 0
        with open(self._filepath) as f:
            for line in f:
                # Eliminate \n \r
                _line = line.replace('\n','')
                _line = _line.replace('\r','')
                _listItems = _line.split(',')

                ### 2nd : name, 3rd : DateTime, 4th DataType, 6th : Num Buzz, 7th - data
                # Data Filtered by DataType
                if _listItems[3] == self._dataType: 
                    _matSingle = []
                    _sizeItems = len(_listItems) - 1
                    _datetime = _listItems[2]
                    _dtmi.setOriginalDateTime(_datetime)
                    _matSingle.append(_dtmi.convert2TrmiDateTime()) # Append Date Time
                    _matSingle.append(_listItems[1]) # Append Asset
                    for i in range(5, _sizeItems):
                        try:
                            _matSingle.append(float(_listItems[i])) # Append Actual Indicies
                        except ValueError:
                            _matSingle.append(0.0)
                    self._mat.append(_matSingle)
        return self._mat

    def getHeaderIndex(self):
        _dict = {}
        with open(self._filepath) as f:
            x = 0
            for line in f:
                _line = line.replace('\n','')
                _line = _line.replace('\r','')
                _listItems = _line.split(',')
                i = 0
                # Add TimeStamp
                _dict[_listItems[2]] = i
                i = i + 1

                # Add Asset Class
                _dict[_listItems[1]] = i
                i = i + 1
                _sizeItem = len(_listItems) - 1
                for j in range(5, _sizeItem):
                    _dict[_listItems[j]] = i
                    i = i + 1
                # Process ONLY HEADER Record    
                x = x + 1
                if x > 0:
                    break
        return _dict
        
class genTickMatrix:
    _filepath = ''
    _mat = []
    
    def setFilePath(self,filePath):
        self._filepath = filePath
        
    def load2Matrix(self):
        _dtmi = dtmi()
        with open(self._filepath) as f:
            for line in f:
                # Eliminate \n \r
                _line = line.replace('\n','')
                _line = _line.replace('\r','')
                _listItems = _line.split(',')
                ### 1st RIC, 2nd Date, 3rd Time, 6th Open, 7th High, 8th Low, 9th Close
                _matSingle = []
                if _listItems[5] != '':
                    _datetime = _listItems[1] + ' ' + _listItems[2]
                    _dtmi.setOriginalDateTime(_datetime)
                    _matSingle.append(_dtmi.convert2TrmiDateTime()) # Append Date Time
                    _matSingle.append(_listItems[0]) # Append Ric Code
                    _matSingle.append(float(_listItems[5])) # Append Open Price
                    _matSingle.append(float(_listItems[6])) # Append High Price
                    _matSingle.append(float(_listItems[7])) # Append Low Price
                    _matSingle.append(float(_listItems[8])) # Append Close Price
                    self._mat.append(_matSingle)
        return self._mat

class trmiManipulation:
    _trmiMat = []
    _tickMat = []
    
    def setMatrices(self, tickMat, trmiMat):
        self._tickMat = tickMat
        self._trmiMat = trmiMat
    
    def rearrangeMatrices(self):
        _tickMatSize = len(self._tickMat)
        _trmiMatSize = len(self._trmiMat)
        ### Generate TickDict
        for i in range(0, _tickMatSize):
            _item = self._tickMat[i].split(',')
            print (_item[1])
        ### Generate TrmiDict
