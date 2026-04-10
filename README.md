# ceTDP

This repository provides a detailed guide for estimating the lower bound on the true discovery proportion (TDP), i.e., the proportion of truly activated voxels within each cluster, using two complementary approaches: **ceTDP-con** and **ceTDP-appr**. Here, the clusters can be supra-threshold clusters, anatomical regions, or arbitrary user-defined regions. The results are compatible with standard cluster inference workflows, while additionally offering activation quantification through TDP estimates.

## Software Suite Overview

This repository provides an overview all software implementations of the method described in:

> **Cluster extent inference revisited: quantification and localisation of brain activity**  
> Goeman, J.J., Górecki, P., Monajemi, R., Chen, X., Nichols, T.E. and Weeda, W., *Journal of the Royal Statistical Society Series B: Statistical Methodology*, vol. 85, no. 4, 2023, 1128–1153 

and the corresponding software paper:

> **ceTDP: A Practical Tutorial on Valid and Quantitative Cluster-Extent Inference in Neuroimaging**  
> Chen, X., Peek, L., Monajemi, R., Górecki, P., Nichols, T.E., Goeman, J.J. and Weeda, W., *arXiv*, 2026

This project includes multiple implementations across different programming environments, contributed by different authors.

---

## Available Tools

### Stage 1: Cluster Extent Threshold Computation

| Tool | Language | Description | Link | Author |
|------|----------|------------|------|--------|
| ceTDP-k-MATLAB | MATLAB | Parametric | [GitHub](LINK) | XC |
| ceTDP-k-FSL | FSL | Parametric | [GitHub](LINK) | XC |
| ceTDP-k-R | R | Nonparametric | [GitHub](LINK) | XC |

### Stage 2: TDP Bound Estimation

#### Conservative Estimate

| Tool | Language | Link | Author |
|------|----------|------|--------|
| ceTDP-Cons-MATLAB | MATLAB | [ceTDP-Cons-SPM](https://github.com/xuchen312/ceTDP-Cons-SPM) | XC |
| ceTDP-Cons-C | C | [ceTDP-Cons-C](LINK) | RM & XC |
| ceTDP-Cons-R | R | [ceTDP-Cons-R](LINK) | JJG & XC |

#### Approximate Estimate

| Tool | Language | Link | Author |
|------|----------|------|--------|
| ceTDP-Appr-C | C | [ceTDP-Appr-C]([LINK](https://github.com/ppgorecki/ceTDP-Appr)) | PG |

---

## Installation & Usage

Each tool is maintained in its own repository. Please follow the instructions provided in each repository.

General workflow:

1. Run Stage 1 tool (choose one implementation)
2. Run Stage 2 tool (choose conservative/approximate or both)
3. Analyze output

## Citation

If you use this software, please cite: [Method paper](https://doi.org/10.1093/jrsssb/qkad067) and [Software paper]().





## ceTDP-Cons

**ceTDP-Cons** uses a fast, non-iterative exact algorithm that provides a conservative TDP bound while maintaining strict FWER control.

## ceTDP-Appr

**ceTDP-Appr** uses a two-phase heuristic algorithm that computes an approximate (and potentially tighter) TDP bound.

### Installation

- Go to the project page: [ceTDP-Appr](https://github.com/ppgorecki/ceTDP-Appr).

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
