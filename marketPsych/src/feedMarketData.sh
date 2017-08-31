#!/bin/sh

assetCode=$1

while true
do
    if [ -e ../bin/$assetCode.eoj ]; then
	echo "Found $assetCode.eoj, processing...."
	# Transfer AssetCode Price into Cloud Storage
	gsutil cp ../bin/$assetCode.dat gs://econnect/$assetCode.dat
	# Insert Asset Codde Price into BigQuery
	tblName=`echo $assetCode | sed -e 's/=//g' | sed -e 's/\///g'`
	bq load --source_format=CSV --field_delimiter=',' --autodetect test.$tblName gs://econnect/$assetCode.dat
	# DELETE EOJ FILE
	rm ../bin/$assetCode.eoj

    fi
    sleep 30
done
