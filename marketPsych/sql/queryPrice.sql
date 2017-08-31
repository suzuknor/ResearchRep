#!/bin/sh

assetCode="'$1'"
assetClass="$2"
numCount=$3
outFile=$2

# 1: OBTALN RAW COUNT 
echo '#!/bin/sh' > sqlp.cmd
echo 'bq query "select count(*) from test.'$assetClass' where assetCode='$assetCode'"' >> sqlp.cmd

chmod 755 sqlp.cmd

rawcnt=`./sqlp.cmd | grep -v '\-\-\-\-' | grep -v 'f0_' | sed -e 's/|/,/g' | sed -e 's/NULL//g' | sed -e 's/ //g' | cut -b2- | awk -F, 'NR==2 {print $1}'`

numLimit=$numCount
numOffset=`expr $rawcnt - $numCount`



# 2: OBTAIN RESULT
echo '#!/bin/sh' > sqlp.cmd
echo 'bq query -n 100000 "select * from test.'$assetClass' where assetCode='$assetCode' order by windowTimestamp asc limit '$numLimit ' offset '$numOffset'"' >> sqlp.cmd

chmod 755 sqlp.cmd


./sqlp.cmd | grep -v '\-\-\-\-' | sed -e 's/|/,/g' | sed -e 's/NULL/0.0/g' | sed -e 's/ //g' | cut -b2- > sqlp.ret0
tail -n +2 sqlp.ret0 > sqlp.ret1
cut -b1- sqlp.ret1 > $outFile.prc.ret

rm sqlp.cmd
rm sqlp.ret0
rm sqlp.ret1




