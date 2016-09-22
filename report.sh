#!/bin/sh
echo "creating apiusage.csv..."
grep -ohr 'chrome\.[\.a-zA-Z0-9]*' addons/  | sort | uniq -c | sort -nr | awk '{if(NR==1){print "API,Count";}else{print  $2 "," $1;}}' > apiusage.csv
echo "generating report..."
python generate.py
