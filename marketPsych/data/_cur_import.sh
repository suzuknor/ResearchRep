#!/bin/sh

#gsutil cp ./cur_template.txt gs://trmi/CUR/WDAI_UHOU/cur_template.txt
#bq load --source_format=CSV --field_delimiter='\t' --autodetect test.CUR_1H gs://trmi/CUR/WDAI_UHOU/cur_template.txt
rm *.m
for flist in `ls -s1 *CUR* | awk '{print $2'}`; do
    echo $flist
    sed -e 's/\t\t/\t0.0\t/g' $flist > $flist.m
    gsutil cp ./$flist.m gs://trmi/CUR/WDAI_UHOU/$flist.m
    bq load --source_format=CSV --field_delimiter='\t' --autodetect test.CUR_1H gs://trmi/CUR/WDAI_UHOU/$flist.m
    gsutil rm gs://trmi/CUR/WDAI_UHOU/$flist.m
done

for flist in `ls -s1 *COU* | awk '{print $2'}`; do
    echo $flist
    sed -e 's/\t\t/\t0.0\t/g' $flist > $flist.m
    gsutil cp ./$flist.m gs://trmi/COU/WDAI_UHOU/$flist.m
    bq load --source_format=CSV --field_delimiter='\t' --autodetect test.COU_1H gs://trmi/COU/WDAI_UHOU/$flist.m
    gsutil rm gs://trmi/COU/WDAI_UHOU/$flist.m
done

for flist in `ls -s1 *COM_ENM* | awk '{print $2'}`; do
    echo $flist
    sed -e 's/\t\t/\t0.0\t/g' $flist > $flist.m
    gsutil cp ./$flist.m gs://trmi/COM_ENM/WDAI_UHOU/$flist.m
    bq load --source_format=CSV --field_delimiter='\t' --autodetect test.COM_ENM_1H gs://trmi/COM_ENM/WDAI_UHOU/$flist.m
    gsutil rm gs://trmi/COM_ENM/WDAI_UHOU/$flist.m
done

for flist in `ls -s1 *COM_AGR* | awk '{print $2'}`; do
    echo $flist
    sed -e 's/\t\t/\t0.0\t/g' $flist > $flist.m
    gsutil cp ./$flist.m gs://trmi/COM_AGR/WDAI_UHOU/$flist.m
    bq load --source_format=CSV --field_delimiter='\t' --autodetect test.COM_AGR_1H gs://trmi/COM_AGR/WDAI_UHOU/$flist.m
    gsutil rm gs://trmi/COM_AGR/WDAI_UHOU/$flist.m
done


rm *.m
