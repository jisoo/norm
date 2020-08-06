# Rockland Sample Norm Processing Pipeline
This repository has been created by mnarayan, adimaron, and jisoo.

## 1. Denoising Images
_Note: if you already have denoised derivatives, you may skip this step._

## 2. Extracting ROI Time-series
To extract the ROI time-series using Schaefer atlases of 100, 200, and 300 parcels:
```bash
mkdir $roi_output_dir
cd 02_roi_timeseries && python fetch_roi_timeseries.py -i $denoised_output_dir -o $roi_output_dir
```

## 3. Successive Normalization
To successively normalize ROI time-series matrices:
```bash
mkdir $normalized_output_dir
cd 03_successive_normalization && bash run_normalizer.sh $roi_output_dir $normalized_output_dir
```

## 4. ROI Correlation Analysis
To get the correlation among the normalized ROI timeseries:
```bash
mkdir $roi_correlation_output_dir
cd 04_roi_correlation && bash run_correlation.sh $normalized_output_dir $roi_correlation_output_dir
```

## 5. Network Connectivity Analysis
To get the average connectivity within each network:
```bash
mkdir $network_output_dir
cd 05_network_connectivity && bash run_network_corr.py -i $roi_correlation_output_dir -o $network_output_dir
```
