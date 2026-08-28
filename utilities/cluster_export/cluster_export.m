function cluster_export(minClusSz,xSPM,cdt,ROI)
% Generate cluster information CSV files.
% 
% INPUTS (mandatory):
% minClusSz - Minimum significant cluster size
%
% Inputs (optional):
% xSPM      - Structure containing SPM, distribution & filtering details
% cdt       - Cluster defining threshold (CDT)
%             If less than zero, u is taken to be uncorrected P-value
% ROI       - NIFTI file with regions of interest (labelled using 1,2,...)
%

%--- 1) Check inputs
if nargin < 1
    error('Please specify the mandatory input ''minClusSz''.');
end
if nargin < 2 || isempty(xSPM)
    try
        [~,xSPM] = spm_getSPM;
    catch
        load SPM.mat
        [~,xSPM] = spm_getSPM;
    end
end
if nargin < 3 || isempty(cdt)
    cdt = xSPM.u;
end
if nargin >= 4 && ~isempty(ROI)
    if ischar(ROI) || isstring(ROI)
        ROI = spm_read_vols(spm_vol(ROI));
    end
end

% if CDT is below 1, assume this to be a p-value
if cdt <= 1
    cdt = spm_u(cdt,xSPM.df,xSPM.STAT);
end

%--- 2) k-value = minClusSz-1
kval = minClusSz-1;

%--- 3) Generate cluster info files
Tmap = spm_read_vols(spm_vol(fullfile(xSPM.swd,xSPM.Vspm.fname)));

% apply CDT & generate clusters
Tmap(Tmap<cdt) = 0;
[L,NUM] = spm_bwlabel(Tmap);
% iterate through clusters & export cluster info files
if nargin >= 4 && ~isempty(ROI)

    labels_roi = unique(ROI(ROI>0));
    for i = 1:length(labels_roi)
        mask_roi = double(ROI==labels_roi(i) & L>0);
        [L_i,NUM_i] = spm_bwlabel(mask_roi);
        for j = 1:NUM_i
            idx = (L_i == j);
            clusSize = sum(idx(:));
            if clusSize > kval  % extract clusters with size > kval
                % get [X,Y,Z] voxel coordinates for each cluster
                [x,y,z] = ind2sub(size(L_i),find(L_i==j));
                % export to CSV
                fileID = fopen(sprintf('roi%d_subclus%d_size%d_kval%d.csv',labels_roi(i),j,clusSize,kval),'w');
                if fileID == -1
                    error('Cannot open output file.');
                end
                fprintf(fileID, 'x,y,z\n');
                fprintf(fileID,'%d,%d,%d\n',[x y z]');
                fclose(fileID);
            end
        end
    end

else

    for i = 1:NUM
        idx = (L == i);
        clusSize = sum(idx(:));
        if clusSize > kval  % extract clusters with size > kval
            % get [X,Y,Z] voxel coordinates for each cluster
            [x,y,z] = ind2sub(size(L),find(L==i));
            % export to CSV
            fileID = fopen(sprintf('clus%d_size%d_kval%d.csv',i,clusSize,kval),'w');
            if fileID == -1
                error('Cannot open output file.');
            end
            fprintf(fileID, 'x,y,z\n');
            fprintf(fileID,'%d,%d,%d\n',[x y z]');
            fclose(fileID);
        end
    end

end

return
