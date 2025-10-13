# CTP-RFT

This repository provides a detailed guide for estimating the lower bound on the true discovery proportion (TDP), i.e., the proportion of truly activated voxels within each cluster, using two complementary approaches: **ClusterTDP** and **TDPClusters**. The results are compatible with standard cluster inference workflows, while additionally offering activation quantification through TDP estimates.

## ClusterTDP

**ClusterTDP** uses a fast, non-iterative exact algorithm that provides a conservative TDP bound while maintaining strict FWER control.

### Installation
- Go to the project page: [ClusterTDP-SPM](https://github.com/xuchen312/ClusterTDP-SPM).
- Download the SPM extension from the repository.
- In MATLAB, add `spm12` & `ClusterTDP-SPM` to your search paths:
  ```matlab
  addpath(genpath('.../spm12'));
  addpath('.../ClusterTDP-SPM');
  ```

### General Usage

- **Syntax**:
  ```matlab
  [hReg,xSPM,SPM,TabDat] = spm_clusterTDP([xSPM,file])
  ```
- **Inputs** (*optional*)
  - ```xSPM``` Thresholded SPM structure,
  - ```file``` Character string specifying a filename (for CSV export).
  
- **Outputs** (*optional; must use none or all for interactive exploration*)
  - ```hReg``` Handle to the results GUI,
  - ```xSPM``` Thresholded SPM structure,
  - ```SPM``` Standard SPM structure,
  - ```TabDat``` Result summary table structure.
  
- **Example**
  ```matlab
  spm_clusterTDP
  ```
  
- **Note:**
  The intermediate output (estimated minimum significant cluster size) is required for use in **TDPClusters**.

## TDPClusters

**TDPClusters** uses a two-phase heuristic algorithm that computes an approximate (and potentially tighter) TDP bound.

### Installation
- Go to the project page: [TDPClusters](https://github.com/ppgorecki/TDPClusters).
- Download the standalone tool from the repository.
- Open a terminal, navigate to the tool directory, and run:
  ```
  cd upperbounds
  make
  ```
  
### General Usage
- **Syntax**:
  ```
  ./fgreedy -x batch7.cnf -T0 -N60 –k[kval] [file]
  ```
- **Inputs** (*optional*)
  - ```batch7.cnf``` Configuration file specifying parameters and rules essential for the algorithm,
  - ```-T``` Global time limit in seconds (use ```0``` to disable the time limit),
  - ```-N``` No improvement time threshold in seconds (recommended: ```60```),
  - ```-k``` k-value = min. significant cluster size − 1 (from **ClusterTDP**),
  - ```file``` Input cluster file in CSV/TSV format (function ```WriteClusterFiles``` can be used to create these files).
  
- **Outputs** (*optional; must use none or all for interactive exploration*)
  - ```minscore``` Estimated TDN = TDP × cluster size.
  
- **Example**
  ```
  ./fgreedy -x batch7.cnf -T0 -N60 –k128 clus1.csv
  ```
  
- **Note:**
  The algorithm is heuristic and may not converge to the global optimum, so error guarantees may not always hold.

## Found bugs? Any questions?

Please contact Xu Chen at xuchen312@gmail.com.
