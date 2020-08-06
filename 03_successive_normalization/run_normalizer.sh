#!/usr/bin/env bash

data_dir=$1
output_dir=$2

roits=`ls $data_dir/*roits/*csv`
for roi in $roits; do
	output=$output_dir/`basename $roi | tr "." "\n" | sed -n "1p"`"_normalized"
	matlab -nojvm -nodesktop -nosplash -r "pre_normalization('$roi','$output');quit();"
done
