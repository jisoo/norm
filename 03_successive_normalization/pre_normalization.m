% Original Author: Adi Maron-Katz
% Edited by: Jisoo Lily Jeong
% Date: May 27, 2020
function pre_normalization(roi, output)
addpath('ggmClass-tools');

data=readmatrix(roi, 'Delimiter', ' ');

% Select ROIs that have the standard deviation greater than 0.01
valid_rois=find(std(data')>0.01);

if ismember(0, std(data')>0.01)
	disp(strcat('NaN found for:', roi));
else
	disp(strcat('No NaNs in:', roi));
end


% Extract the ROIs from the data
data_cleaned=data(valid_rois,:);

% Successive normalization
standardize.successive_normalize(data_cleaned, output);

end
