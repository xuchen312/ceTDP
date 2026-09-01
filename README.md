# ceTDP

**ceTDP** is a two-stage framework for valid and quantitative cluster-extent inference in neuroimaging. It estimates lower bounds on the **True Discovery Proportion (TDP)**, i.e., the proportion of truly activated voxels within a selected region, while maintaining family-wise error rate (FWER) control.

Unlike conventional cluster-extent inference, ceTDP supports quantitative inference within significant clusters, anatomical regions, and arbitrary user-defined regions.

## Method Overview

The ceTDP framework consists of two stages.

### Stage 1: Cluster extent threshold computation and region specification

Stage 1 determines the minimum significant cluster extent threshold (`k`) using either parametric (Random Field Theory) or nonparametric (permutation-based) inference. Regions for subsequent inference are then defined, and the corresponding cluster information is prepared for Stage 2.

ROI specification is optional. When no ROI is specified, significant supra-threshold clusters can be used directly as the regions of inference.

### Stage 2: TDP bound estimation

Given the Stage 1 outputs, ceTDP estimates lower bounds on the **True Discovery Number (TDN)** within each selected region. The **True Discovery Proportion (TDP)** is obtained by

> **TDP = TDN / |S|**

where `|S|` denotes the number of voxels in the selected region.

Two complementary algorithms are provided:

- **ceTDP-cons** — exact, non-iterative conservative lower bounds with strict FWER control.
- **ceTDP-appr** — heuristic approximate lower bounds that are often tighter but do not guarantee the global optimum.

## Workflow

| Stage | Component | Main output |
|------|-----------|-------------|
| **Stage 1** | **ceTDP-k** | Minimum significant cluster extent threshold (`k`) |
| **Stage 1** | **Region specification** | Selected regions and corresponding cluster information |
| **Stage 2** | **ceTDP-cons / ceTDP-appr** | Lower bound on the TDN |
| **Stage 2** | **TDP** | `TDP = TDN / \|S\|` |

## Software Suite

This repository serves as the entry point for all software implementations accompanying the ceTDP framework.

### Method paper

> **Cluster extent inference revisited: quantification and localisation of brain activity**  
> Goeman JJ, Górecki P, Monajemi R, Chen X, Nichols TE & Weeda W.  
> *Journal of the Royal Statistical Society Series B*, 2023.

### Software paper

> **ceTDP: A Practical Tutorial on Valid and Quantitative Cluster-Extent Inference in Neuroimaging**  
> Chen X, Peek L, Monajemi R, Górecki P, Nichols TE, Goeman JJ & Weeda W.  
> *arXiv*, 2026.

## Available Implementations

### Stage 1: ceTDP-k

Stage 1 includes cluster extent threshold computation and region specification. The **ceTDP-k** repository provides implementations for computing the minimum significant cluster extent threshold (`k`).

| Tool | Language | Description | Repository |
|------|----------|-------------|------------|
| **ceTDP-k-SPM** | MATLAB | Parametric (SPM) | ceTDP-k |
| **ceTDP-k-FSL** | FSL | Parametric (FSL pipeline) | ceTDP-k |
| **ceTDP-k-R** | R / C++ | Nonparametric permutation inference | ceTDP-k |

Repository: [**ceTDP-k**](https://github.com/xuchen312/ceTDP-k)

Primary output:

- Minimum significant cluster extent threshold (`k`)

Region specification is a separate part of Stage 1. The corresponding cluster information files required by Stage 2 can be prepared using the utilities provided in this repository.

### Stage 2: Conservative inference (ceTDP-cons)

| Tool | Language | Repository |
|------|----------|------------|
| **ceTDP-cons-SPM** | MATLAB | [ceTDP-cons-SPM](https://github.com/xuchen312/ceTDP-cons-SPM) |
| **ceTDP-cons-C** | C | [ceTDP-cons-C](https://github.com/rmonajemi/ceTDP-cons-C) |
| **ceTDP-cons-R** | R | [ceTDP-cons-R](https://github.com/xuchen312/ceTDP-cons-R) |
| **ceTDP-cons-Python** | Python | [ceTDP-cons-Python](https://github.com/xuchen312/ceTDP-cons-Python) |

Computes exact, non-iterative conservative lower bounds on the TDN.

### Stage 2: Approximate inference (ceTDP-appr)

| Tool | Language | Repository |
|------|----------|------------|
| **ceTDP-appr** | C | [ceTDP-appr](https://github.com/ppgorecki/ceTDP-appr) |

Computes heuristic approximate lower bounds on the TDN.

## Utilities

This repository also provides auxiliary utilities for **region specification** and **visualization**. These tools facilitate data preparation and visualization but are **not part of the core ceTDP inferential procedure**.

| Tool | Description |
|------|-------------|
| **cluster_export** | Export supra-threshold clusters and ROI-overlapping subclusters as CSV (MATLAB & Python) |
| **cetdp_vis** | Generate layered voxel-wise ceTDP visualization maps |

See `utilities/README.md` for detailed documentation.

## General Workflow

1. **Run ceTDP-k** to compute the minimum significant cluster extent threshold (`k`).
2. **Define the regions for inference** and prepare the corresponding cluster information files. ROI specification is optional; significant supra-threshold clusters can be used directly when no ROI is specified.
3. **Run ceTDP-cons** or **ceTDP-appr** to estimate TDN lower bounds.
4. **Convert TDN to TDP** using `TDP = TDN / |S|`.
5. *(Optional)* Generate layered voxel-wise visualization maps using **cetdp_vis**.

## Citation

If you use ceTDP, please cite both the methodological and software papers.

**Method paper**

Goeman JJ, Górecki P, Monajemi R, Chen X, Nichols TE & Weeda W. Cluster extent inference revisited: quantification and localisation of brain activity. *Journal of the Royal Statistical Society Series B*, 2023.

**Software paper**

Chen X, Peek L, Monajemi R, Górecki P, Nichols TE, Goeman JJ & Weeda W. ceTDP: A Practical Tutorial on Valid and Quantitative Cluster-Extent Inference in Neuroimaging. *arXiv*, 2026.
