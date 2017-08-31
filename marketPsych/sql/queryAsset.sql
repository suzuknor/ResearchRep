#!/bin/sh

assetCode="'$1'"
assetClass="$2"
numCount=$3
outName=$1
dataType="'News_Social'"

# 1: OBTALN RAW COUNT 
echo '#!/bin/sh' > sql.cmd
echo 'bq query "select count(*) from test.'$assetClass'_1H where assetCode='$assetCode' and dataType='$dataType'"' >> sql.cmd

chmod 755 sql.cmd

rawcnt=`./sql.cmd | grep -v '\-\-\-\-' | grep -v 'f0_' | sed -e 's/|/,/g' | sed -e 's/NULL//g' | sed -e 's/ //g' | cut -b2- | awk -F, 'NR==2 {print $1}'`

numLimit=$numCount
numOffset=`expr $rawcnt - $numCount`



# 2: OBTAIN RESULT
echo '#!/bin/sh' > sql.cmd
echo 'bq query -n 100000 "select * from test.'$assetClass'_1H where assetCode='$assetCode' and dataType='$dataType' order by windowTimestamp asc limit '$numLimit ' offset '$numOffset'"' >> sql.cmd

chmod 755 sql.cmd


./sql.cmd | grep -v '\-\-\-\-' | sed -e 's/|/,/g' | sed -e 's/NULL/0.0/g' | sed -e 's/ //g' | cut -b2- > sql.ret0
tail -n +2 sql.ret0 > sql.ret1
cut -b1- sql.ret1 > $outName.trmi.ret

#rm sql.cmd
#rm sql.ret0
#rm sql.ret1




