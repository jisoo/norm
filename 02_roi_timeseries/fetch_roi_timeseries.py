#!/usr/bin/env python3
"""
    File name: fetch_roi_timeseries.py
    Author: Manjari Narayan
    Edited by: Jisoo Lily Jeong
    Date created: 01/15/2019
    Date last modified: 05/27/2020
    Python Version: 3.7.6
    Description: Script to extract roi level timeseries after fmriprep and denoiser
    Project: Rockland Norm Project
"""

from nilearn.input_data import NiftiLabelsMasker
import nilearn.signal
import nilearn.image
import numpy as np
import argparse
import sys
import errno
import os

def main():
    parser = argparse.ArgumentParser(description='Rockland Norm ROI extraction Pipeline')
    parser.add_argument('-i', '--input-dir', help='Input directory')
    parser.add_argument('-o', '--output-dir', help='Output directory')

    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))

    #####################################
    #Schaefer 100, 200, and 300 atlases #
    #####################################

    atlasfile = os.path.join(script_dir,"atlas",
	'Schaefer2018_100Parcels_7Networks_order_FSLMNI152_1mm.nii.gz')
    atlasfile2 = os.path.join(script_dir,"atlas",
        'Schaefer2018_200Parcels_7Networks_order_FSLMNI152_1mm.nii.gz')
    atlasfile3 = os.path.join(script_dir,"atlas",
        'Schaefer2018_300Parcels_7Networks_order_FSLMNI152_1mm.nii.gz')

    # extract signals
    masker = NiftiLabelsMasker(labels_img=atlasfile,smoothing_fwhm=4,
	standardize=False,detrend=False,low_pass=None,high_pass=None,verbose=5)
    masker2 = NiftiLabelsMasker(labels_img=atlasfile2,smoothing_fwhm=4,
	standardize=False,detrend=False,low_pass=None,high_pass=None,verbose=5)
    masker3 = NiftiLabelsMasker(labels_img=atlasfile3,smoothing_fwhm=4,
	standardize=False,detrend=False,low_pass=None,high_pass=None,verbose=5) 

    for root, dirs, files in os.walk(args.input_dir):
        for f in files:
            if not f.endswith('.nii.gz'): continue

            # setting up paths
            img = f
            imgfile = os.path.join(root,img)

            # save parcellated time series
            try:
                os.mkdir(os.path.join(args.output_dir,img.replace('.nii.gz','_roits')))
            except OSError as exc:
                if exc.errno != errno.EEXIST: raise
                pass
        
            ####### Atlas 1 ########
            time_series = masker.fit_transform(imgfile, confounds=None)
            outfile = os.path.join(args.output_dir,img.replace('.nii.gz','_roits'),
                                    img.replace('.nii.gz','_Schaefer100_Yeo7Networks.csv'))
            np.savetxt(outfile,time_series)

            ####### Atlas 2 ########
            time_series = masker2.fit_transform(imgfile, confounds=None)
            outfile = os.path.join(args.output_dir,img.replace('.nii.gz','_roits'),
                                    img.replace('.nii.gz','_Schaefer200_Yeo7Networks.csv'))
            np.savetxt(outfile,time_series)

            ####### Atlas 3 ########
            time_series = masker3.fit_transform(imgfile, confounds=None)
            outfile = os.path.join(args.output_dir,img.replace('.nii.gz','_roits'),
                                    img.replace('.nii.gz','_Schaefer300_Yeo7Networks.csv'))
            np.savetxt(outfile,time_series)

if __name__ == "__main__":
	main()
