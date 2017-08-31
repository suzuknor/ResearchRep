#!/bin/sh
targetDB=$1

cd $HOME/marketPsych/data/old
ls -1l *.txt > _file.list
awk '{print $9}' _file.list > _file.list2
rm _file.list

cat ./_file.list2 | while read line
do
    echo $line
    sed -e 's/\t\t/\t0.0\t/g' $HOME/marketPsych/data/old/$line > $HOME/marketPsych/data/old/$line.m
    gsutil cp $HOME/marketPsych/data/old/$line.m gs://trmi/$targetDB/WDAI_UHOU/$line
    bq load --source_format=CSV --field_delimiter='\t' --autodetect test.$targetDB"_1H" gs://trmi/$targetDB/WDAI_UHOU/$line
    gsutil rm gs://trmi/$targetDB/WDAI_UHOU/$line
    rm $HOME/marketPsych/data/old/$line.m
done
