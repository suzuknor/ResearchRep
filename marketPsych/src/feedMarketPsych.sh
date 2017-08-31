#!/bin/sh
# Continuous Data Feed from Market Psych site and import Market Psych into Google BigQuery
# Author: NORIYUKI SUZUKI / Market Development Manager, Thomson Reuters
# Created: June 22 2017
# Version: beta 0.8
# Command Arguments:
#       $1 FTP Directory
#       $2 Google Storage gs://bucket/area
#       $3 Google BigQuery dataset.table
assetType=$1
googleStorage=$2
bigQueryTable=$3


if [ ! -e ./_prev.$assetType.list ]; then
    touch ./_prev.$assetType.list
fi

while true
do
# LIST UP curent file in the ftp dir
python ./listFTP.py /TRMI_LIVE/$assetType/WDAI_UHOU/LastTwoHours/ | sort -k9  > _curr.$assetType.list
diff ./_prev.$assetType.list ./_curr.$assetType.list > ./_diff.$assetType.list
grep ">"  ./_diff.$assetType.list | awk '{print $10}' > ./_transfer.$assetType.list

cat ./_transfer.$assetType.list | while read line
do
    echo "--->retrieve  $line"

    ### FTP RETRIEVE from FTP to Local Compute Engine
    python ./doFTP.py /TRMI_LIVE/$assetType/WDAI_UHOU/LastTwoHours/$line /home/suzuknor/devel/marketPsych/data/$line

    ### REPLACE NULL to 0.0 (FLOAT TYPE)
    sed -e 's/\t\t/\t0.0\t/g' /home/suzuknor/devel/marketPsych/data/$line > /home/suzuknor/devel/marketPsych/data/$line.m

    ### COPY LOCALLY FEED TRMI FILE INTO CLOUD STORAGE BUCKET
    gsutil cp /home/suzuknor/devel/marketPsych/data/$line.m gs://trmi/$assetType/WDAI_UHOU/$line

    ### IMPORT DATA FROM CLOUD STORAGE BUCKET to BigQuery
    bq load --source_format=CSV --field_delimiter='\t' --autodetect test.$assetType"_1H" gs://trmi/$assetType/WDAI_UHOU/$line

    ### CLEAN UP DATA in CLOUD STORAGE
    gsutil rm gs://trmi/$assetType/WDAI_UHOU/$line
    rm /home/suzuknor/devel/marketPsych/data/$line.m
    rm /home/suzuknor/devel/marketPsych/data/$line
done

cp ./_curr.$assetType.list ./_prev.$assetType.list
sleep 60
done

