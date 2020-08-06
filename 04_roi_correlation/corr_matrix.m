function corr_matrix(roi, output)
matrix=readmatrix(roi,'Delimiter',',');
x = corr(matrix);

disp(strcat("Exporting corr matrix for roi :", roi));
writematrix(x, output);

end
