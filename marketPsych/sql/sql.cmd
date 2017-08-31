#!/bin/sh
bq query -n 100000 "select * from test.COM_AGR_1H where assetCode='CTTL' and dataType='News_Social' order by windowTimestamp asc limit 10000  offset 13226"
