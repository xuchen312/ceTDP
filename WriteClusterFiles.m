function WriteClusterFiles(minClusSz,xSPM,cdt)
% Generate cluster information CSV files.
% 
% INPUTS:
% minClusSz - Minimum significant cluster size (extracted from ClusterTDP)
%
% Inputs (optional):
% xSPM      - Structure containing SPM, distribution & filtering details
% cdt       - Cluster defining threshold (CDT)
%             If less than zero, u is taken to be uncorrected P-value
%

%--- 1) Check inputs
if nargin < 1
    error('Please specify the mandatory input ''minClusSz''.');
end
if nargin < 2 | isempty(xSPM)
  [~,xSPM] = spm_getSPM;
end
if nargin < 3 | isempty(cdt)
    cdt = xSPM.u;
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
for i = 1:NUM
    if sum(L(:)==i) > kval  % extract clusters with size > kval
        % get [X,Y,Z] voxel coordinates for each cluster
        [x,y,z] = ind2sub(size(L),find(L==i));
        % export to CSV
        fileID = fopen(sprintf('clus%d_size%d_kval%d.csv',i,sum(L(:)==i),kval),'w');
        fprintf(fileID, 'x,y,z\n');
        for j = 1:length(x)
            fprintf(fileID,'%d,%d,%d\n',x(j),y(j),z(j));
        end
        fclose(fileID);
    end
end

return
