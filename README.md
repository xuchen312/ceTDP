# ceTDP

This repository provides a unified guide to estimating lower bounds on the **True Discovery Proportion (TDP)**, i.e., the proportion of truly activated voxels within a region (e.g., cluster), based on cluster extent thresholding.

The framework supports supra-threshold clusters, anatomical regions, and arbitrary user-defined regions, and is compatible with standard cluster inference workflows while enabling quantitative assessment of activation via TDP.

In practice, most implementations compute lower bounds on the **True Discovery Number (TDN)**, from which TDP is derived.

## Method Overview

Two complementary approaches are provided:

- **ceTDP-cons** uses a fast, non-iterative exact algorithm to compute conservative lower bounds on the TDN, while maintaining strict FWER control.

- **ceTDP-appr** uses a two-phase heuristic algorithm to compute approximate (and potentially tighter) lower bounds on TDN.
  *Note:* As a heuristic method, it may not converge to the global optimum, and guarantees may depend on whether sufficient runtime is allocated.

## Output

Most implementations compute bounds on the **True Discovery Number (TDN)**. The **TDP** can be obtained as:

TDP = TDN / |S|,

where |S| is the size of the selected region.

**Exception:** The SPM-based implementation directly displays TDP in its result table.

This separation reflects the underlying methodology, where inference is naturally formulated in terms of TDN, with TDP obtained by normalisation.

## Software Suite Overview

This repository provides an overview of all software implementations of the method described in:

**Method paper**  
> **Cluster extent inference revisited: quantification and localisation of brain activity**  
> Goeman, J.J., Górecki, P., Monajemi, R., Chen, X., Nichols, T.E. and Weeda, W., *Journal of the Royal Statistical Society Series B: Statistical Methodology*, vol. 85, no. 4, 2023, 1128–1153 

**Software paper**
> **ceTDP: A Practical Tutorial on Valid and Quantitative Cluster-Extent Inference in Neuroimaging**  
> Chen, X., Peek, L., Monajemi, R., Górecki, P., Nichols, T.E., Goeman, J.J. and Weeda, W., *arXiv*, 2026

This project includes multiple implementations across different programming environments, contributed by different authors.

## Method–Implementation Mapping

Function and executable names vary across implementations. All tools are mapped to the following methodological components:

- **ceTDP-cons** (conservative bounds)
- **ceTDP-appr** (approximate bounds)

---

## Available Tools

Command denotes the main command, script, function, or executable used to run each implementation.

### Stage 1: Cluster Extent Threshold Computation

Stage 1 tools compute **intermediate quantities** (i.e., cluster extent thresholds) required as input for Stage 2. These outputs are essential for the subsequent estimation of TDN/TDP bounds and are typically derived from parametric or nonparametric cluster inference procedures.

| Tool | Language | Description | Command | Repository | Author |
|------|----------|-------------|---------|------------|--------|
| ceTDP-k-SPM | MATLAB | Parametric | `spm_ceTDP_minsize.m` | [ceTDP-k](https://github.com/xuchen312/ceTDP-k) | XC (modified implementation) |
| ceTDP-k-FSL | FSL | Parametric | `smoothest` + `cluster` | [ceTDP-k](https://github.com/xuchen312/ceTDP-k) | XC (pipeline using FSL tools) |
| ceTDP-k-R | R | Nonparametric | xxx | [ceTDP-k](https://github.com/xuchen312/ceTDP-k) | XC |

The input to Stage 2 also requires the definition of regions of interest (ROIs), which can be arbitrary regions. For each ROI, its overlap with significant supra-threshold clusters (identified via standard cluster inference) is computed and used as input for Stage 2.

### Stage 2: TDP Bound Estimation

The software provides two methodological variants:

#### Conservative bounds (ceTDP-cons)

| Tool | Language | Command | Repository | Author |
|------|----------|---------|------------|--------|
| ceTDP-cons-SPM | MATLAB | `spm_ceTDP_cons.m` | [ceTDP-cons-SPM](https://github.com/xuchen312/ceTDP-cons-SPM) | XC |
| ceTDP-cons-C | C | `lb` | [ceTDP-cons-C](https://github.com/rmonajemi/ceTDP-cons-C) | RM & XC |
| ceTDP-cons-R | R | `lb.R` | [ceTDP-cons-R](https://github.com/xuchen312/ceTDP-cons-R) | JJG & XC |
| ceTDP-cons-Python | Python | `lb.py` | [ceTDP-cons-Python](https://github.com/xuchen312/ceTDP-cons-Python) | XC |

#### Approximate bounds (ceTDP-appr)

| Tool | Language | Command | Repository | Author |
|------|----------|---------|------------|--------|
| ceTDP-appr-C | C | `fgreedy` | [ceTDP-appr-C]([LINK](https://github.com/ppgorecki/ceTDP-appr)) | PG |

---

## Installation & Usage

Each tool is maintained in its own repository. Please refer to the corresponding repository for installation instructions.

### General workflow

1. Run a Stage 1 tool:
   - Compute intermediate quantities required for Stage 2 inference
   - Define ROIs for subsequent analysis

2. Run a Stage 2 tool:
   - **ceTDP-cons** (statistically guaranteed)
   - **ceTDP-appr** (heuristic but potentially tighter)

3. Convert TDN to TDP if needed  
4. Visualize results

## Citation

If you use this software, please cite:
- [Method paper](https://doi.org/10.1093/jrsssb/qkad067),
- [Software paper]().
