#!/usr/bin/env python3
"""
	Author: Jisoo Lily Jeong
	Date last modified: 06/01/2020
	Python Version: 3.7.6
	Description: Script to extract network-level correlation
	Project: Rockland Norm Project
"""

import pandas as pd
import numpy as np
import argparse
import sys
import os

def main():
	parser = argparse.ArgumentParser(description='Network level correlation pipeline')
	parser.add_argument('-i', '--input-dir', help='Input directory')
	parser.add_argument('-o', '--output-dir', help='Output directory')

	args = parser.parse_args()

	script_dir = os.path.dirname(os.path.realpath(__file__))

	#####################################
	#Schaefer 100, 200, and 300 atlases #
	#####################################

	label1 = os.path.join(script_dir, 
		'utils', 'Schaefer2018_100Parcels_7Networks_order_networklabels.csv')
	label2 = os.path.join(script_dir,
        	'utils', 'Schaefer2018_200Parcels_7Networks_order_networklabels.csv')
	label3 = os.path.join(script_dir,
        	'utils', 'Schaefer2018_300Parcels_7Networks_order_networklabels.csv')

	label1_df = pd.read_csv(label1)
	label2_df = pd.read_csv(label2)
	label3_df = pd.read_csv(label3)

	for root, dirs, files in os.walk(args.input_dir):
		for f in files:
			if not f.endswith('normalized_corr.csv'): continue

			parcels = get_parcel(f)
			labels = get_label(parcels, label1_df, label2_df, label3_df)
			networks = labels['network_index'].unique()

			matrix = np.zeros((len(networks), len(networks)))
			filepath = os.path.join(root, f)
			df = pd.read_csv(filepath, header=None)

			for idx_i, i in enumerate(networks):
				indices_i = labels.index[labels['network_index']==i].tolist()
				for idx_j, j in enumerate(networks):
					indices_j = labels.index[labels['network_index']==j].tolist()
					network_np = df.loc[indices_i, indices_j].to_numpy()
					if idx_i != idx_j:
						nanmean = np.nanmean(network_np)
					else:
						num_nodes = len(indices_i)
						nanmean = (np.nansum(network_np) - num_nodes) / (num_nodes * num_nodes)
					matrix[idx_i][idx_j] = nanmean

			export_filename = f.split('.')[0] + '_networkFC.csv'
			export_filepath = os.path.join(args.output_dir, export_filename)
			print('Saving {}'.format(export_filepath))
			np.savetxt(export_filepath, matrix, delimiter=",")

def get_label(parcels, df1, df2, df3):
	if parcels == 100: return df1
	elif parcels == 200: return df2
	else: return df3
	
def get_parcel(filename):
	if "Schaefer100" in filename:
		return 100
	elif "Schaefer200" in filename:
		return 200
	elif "Schaefer300" in filename:
		return 300
	else:
		print('Incompatible file')
		sys.exit(1)

if __name__ == "__main__":
	main()
