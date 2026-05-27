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

### Stage 1: Cluster Extent Threshold Computation (ceTDP-k)

Stage 1 tools compute **intermediate quantities** (i.e., cluster extent thresholds) required as input for Stage 2. These outputs are essential for the subsequent estimation of TDN/TDP bounds and are typically derived from parametric or nonparametric cluster inference procedures.

| Tool | Language | Description | Command | Repository | Author |
|------|----------|-------------|---------|------------|--------|
| ceTDP-k-SPM | MATLAB | Parametric | `spm_ceTDP_minsize.m` | [ceTDP-k](https://github.com/xuchen312/ceTDP-k) | XC (modified implementation) |
| ceTDP-k-FSL | FSL | Parametric | `smoothest` + `cluster` | [ceTDP-k](https://github.com/xuchen312/ceTDP-k) | XC (pipeline using FSL tools) |
| ceTDP-k-R | R | Nonparametric | `kval.R` | [ceTDP-k](https://github.com/xuchen312/ceTDP-k) | XC |

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

## Auxiliary Utilities

The repository also provides utility scripts for preprocessing and exporting cluster information for downstream ceTDP analyses.

These tools are not part of the core inferential procedures, but facilitate integration with arbitrary ROI definitions and external pipelines.

| Tool | Language | Description | Command | Repository | Author |
|------|----------|-------------|---------|------------|--------|
| ceTDP-cluster-export | Python | Export voxel coordinates for supra-threshold clusters and ROI-overlapping subclusters from NIfTI statistical maps | `cluster_export.py` | current repository | XC |
| ceTDP-vis | Python | Generate layered ceTDP visualization maps using cluster-level TDP estimates | `cetdp_vis.py` | current repository | XC |

### Cluster Export Utility (`cluster_export.py`)

This utility extracts connected supra-threshold voxel clusters from statistical NIfTI images and exports voxel coordinates for downstream analyses.

Features include:

- whole-brain cluster extraction
- ROI-constrained subcluster extraction
- configurable 3D connectivity (6/18/26)
- voxel and MNI/world coordinates
- command-line interface
- compatibility with arbitrary NIfTI statistical maps

#### Installation

Install Python dependencies:

```python
pip install nibabel numpy pandas scipy
```

#### Basic usage

Whole-brain clustering:

```bash
python cluster_export.py \
    --input spmT_0001.nii \
    --cdt 3.1 \
    --extent 20
```

ROI-constrained clustering:

```bash
python cluster_export.py \
    --input spmT_0001.nii \
    --roi AAL.nii.gz \
    --cdt 3.1 \
    --extent 20
```

#### Output

CSV files are written to:

```bash
clusters/
```

Each CSV contains voxel coordinates:

```
x,y,z
```

### ceTDP Visualization Utility (`cetdp_vis.py`)

This utility generates layered voxelwise ceTDP visualization maps from cluster label images and cluster-level TDP estimates.

For each cluster:

- interior voxels are assigned conservative ceTDP-cons TDP values
- inner boundary voxels are assigned approximate ceTDP-appr TDP values

The resulting NIfTI image can be visualized using standard neuroimaging software such as FSLeyes, MRIcroGL, or nilearn.

#### Features

- layered ceTDP visualization
- inner-boundary enhancement
- configurable 3D connectivity (6/18/26)
- command-line interface
- direct NIfTI output
- compatibility with arbitrary cluster label images

#### Installation

Install Python dependencies:

```bash
pip install nibabel numpy pandas scipy
```

#### Input

The utility requires:

1. A cluster label NIfTI image:

```text
clus.nii.gz
```

Voxel values should correspond to cluster labels:

- 0 = background
- positive integers = cluster IDs

2. A CSV table containing cluster-level TDP values:

```csv
cluster_id,tdp1,tdp2
21,0.018,0.158
22,0.223,0.312
23,0.205,0.296
```

where:

- `tdp1` = ceTDP-cons TDP estimate
- `tdp2` = ceTDP-appr TDP estimate

#### Basic usage

```bash
python cetdp_vis.py \
    --cluster clus.nii.gz \
    --table tdp_values.csv
```

#### Custom output

```bash
python cetdp_vis.py \
    --cluster clus.nii.gz \
    --table tdp_values.csv \
    --output output/cetdp_vis.nii.gz
```

#### Connectivity options

```bash
python cetdp_vis.py \
    --cluster clus.nii.gz \
    --table tdp_values.csv \
    --connectivity 6
```

Supported connectivity values:

- 6
- 18
- 26 (default)

#### Output

The utility generates a voxelwise layered visualization map:

```text
cetdp_vis.nii.gz
```

Voxel values correspond to:

- cluster interior → ceTDP-cons values
- inner boundary → ceTDP-appr values
- background → 0

#### Visualization

The output NIfTI image can be visualized using:

- FSLeyes
- MRIcroGL
- nilearn
- ITK-SNAP

Example:

```bash
fsleyes cetdp_vis.nii.gz
```

#### Visualization rationale

The layered visualization strategy combines conservative ceTDP-cons estimates within cluster interiors with potentially tighter ceTDP-appr estimates along cluster boundaries.

This rendering approach visually highlights spatial uncertainty and heterogeneity in cluster-level activation quantification while remaining fully voxel-lattice based.

---

## Installation & Usage

Each tool is maintained in its own repository. Please refer to the corresponding repository for installation instructions.

### General workflow

1. Run a Stage 1 tool:
   - Compute intermediate quantities required for Stage 2 inference
   - Define ROIs for subsequent analysis
  
2. (Optional) Use preprocessing utilities to export supra-threshold clusters or ROI-overlapping subclusters

3. Run a Stage 2 tool:
   - **ceTDP-cons** (statistically guaranteed)
   - **ceTDP-appr** (heuristic but potentially tighter)

4. Convert TDN to TDP if needed
5. (Optional) Generate layered ceTDP visualization maps 
6. Visualize results

## Citation

If you use this software, please cite:
- [Method paper](https://doi.org/10.1093/jrsssb/qkad067),
- [Software paper]().
