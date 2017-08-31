# coding: utf-8

### Converting DD-MMM-YYYY HH:MM:SS.NNN to TRMI Date Time Format
import datetime as dt


# In[5]:

### CLASS DateTimeConvert Definition
class convert2TrmiDateTime:
    _origDateTimeStr = ''
 
    def setOriginalDateTime(self, origDateTimeStr):
        self._origDateTimeStr = origDateTimeStr

    def convert2TrmiDateTime(self):
        if self._origDateTimeStr != '':
            _formattedDateTime1 = dt.datetime.strptime(self._origDateTimeStr, '%Y-%m-%d%H:%M:%S')
            _formattedDateTime2 = _formattedDateTime1.strftime('%Y-%m-%dT%H:%M:%S.000000000Z')
            return _formattedDateTime2
        else:
            return ''
