#!/usr/bin/env python3

import pandas as pd

yeo_network='Yeo_7Networks.csv'

atlas_labels=['Schaefer2018_100Parcels_7Networks_order.csv',
'Schaefer2018_200Parcels_7Networks_order.csv',
'Schaefer2018_300Parcels_7Networks_order.csv'
]

def main():
	network_labels = pd.read_csv(yeo_network)

	# Read in network labels
	networks = []
	for x in network_labels['Network Name']:
		if x not in networks:
			networks.append(x)

	# Ensure we are dealing with the correct network parcellation
	assert len(networks) == 7

	for a in atlas_labels:
		df = pd.read_csv(a, names=['1', 'name', 'coordx', 'coordy', 'coordz', '2'],
			delim_whitespace=True)
		export_df = pd.DataFrame()

		# For each parcel label, find the corresponding network label
		for d in df['name']:
			parcel_name = "_".join(d.split("_")[:-1])
			network_found = network_labels[network_labels['Label Name'] == parcel_name]

			# Exporting variables
			network_name = str(network_found['Network Name'].iloc[0])
			network_index = str(networks.index(network_name) + 1)
			parcel_label = d
			export_df = export_df.append({
				"roi_label" : parcel_label,
				"network" : network_name,
				"network_index" : network_index
			}, ignore_index=True)

		export_df.index += 1
		export_df.index.name = 'index'
		export_filename = a.split('.')[0] + '_network_labels.csv'
		export_df.to_csv(export_filename)


if __name__ == "__main__":
	main()
