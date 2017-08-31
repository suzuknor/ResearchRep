#!/bin/sh
numData=$1
numDepth=$2
echo $numData
# EXTRACT MARKET PSYCH DATA FROM BIG QUERY
cd $HOME/marketPsych/sql
./queryAll.sql $numData

# RUN ANALYTICS TO GENERATE DASHBOARD
cd $HOME/marketPsych/analytics
#(1) USDJPY DASHBOARD
   # DROP CURRENT DASHBOARD TABLE
   bq rm -f -t test.JPY_COU_POS_CORR
   bq rm -f -t test.JPY_COU_NEG_CORR
   bq rm -f -t test.JPY_COU_POS_CORR_FRD
   bq rm -f -t test.JPY_COU_NEG_CORR_FRD

   # GENERATE USDJPY DASHBOARD DATA
   python ./getLinearRegressionPrice.py JPY $numDepth
   gsutil cp ../data/JPY_COU_POS_CORR.csv gs://tranalytics/JPY_COU_POS_CORR.csv
   gsutil cp ../data/JPY_COU_POS_CORR_FRD.csv gs://tranalytics/JPY_COU_POS_CORR_FRD.csv

   bq load --source_format=CSV --field_delimiter=',' --autodetect test.JPY_COU_POS_CORR gs://tranalytics/JPY_COU_POS_CORR.csv
   bq load --source_format=CSV --field_delimiter=',' --autodetect test.JPY_COU_POS_CORR_FRD gs://tranalytics/JPY_COU_POS_CORR_FRD.csv



