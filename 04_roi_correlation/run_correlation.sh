#!/usr/bin/env bash

data_dir=$1
output_dir=$2

roits=`ls $data_dir/*normalized.csv`
for roi in $roits; do
	output=$output_dir/`basename $roi | tr "." "\n" | sed -n "1p"`"_corr.csv"
	matlab -nojvm -nodesktop -nosplash -r "corr_matrix('$roi','$output');quit();"
done
