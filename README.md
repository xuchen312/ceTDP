# ceTDP

**ceTDP** is a unified framework for valid and quantitative cluster-extent inference in neuroimaging. It estimates lower bounds on the **True Discovery Proportion (TDP)**, i.e., the proportion of truly activated voxels within a selected region, while maintaining family-wise error rate (FWER) control.

Unlike conventional cluster-extent inference, ceTDP supports quantitative inference within significant clusters, anatomical regions, and arbitrary user-defined regions.

## Method Overview

The ceTDP framework consists of two stages.

### Stage 1: Cluster extent threshold computation and region specification

Stage 1 determines the minimum significant cluster extent threshold (`k`) using either parametric (RFT-based) or nonparametric (permutation-based) inference. Regions of interest (ROIs) are then specified, and their overlap with significant supra-threshold clusters is prepared for Stage 2.

### Stage 2: TDP bound estimation

Given the Stage 1 outputs, ceTDP estimates lower bounds on the **True Discovery Number (TDN)** within each selected region. The **True Discovery Proportion (TDP)** is obtained by

TDP = TDN / |S|

where |S| denotes the number of voxels in the selected region.

Two complementary algorithms are provided:

- **ceTDP-cons** — exact conservative lower bounds with strict FWER control.
- **ceTDP-appr** — heuristic approximate lower bounds that are often tighter but do not guarantee the global optimum.

## Workflow

The ceTDP framework consists of two stages:

| Stage | Component | Main output |
|------|-----------|-------------|
| **Stage 1** | **ceTDP-k** | Minimum significant cluster extent threshold (*k*) |
| **Stage 1** | **Region specification** | ROI and cluster-overlap information |
| **Stage 2** | **ceTDP-cons / ceTDP-appr** | Lower bound on the True Discovery Number (TDN) |
| **Final result** | **TDP** | TDP = TDN / \|S\| |

### Stage 1

Stage 1 first determines the cluster extent threshold (`k`) and then specifies the regions for subsequent TDP inference.

### Stage 2

Stage 2 uses the Stage 1 outputs to estimate lower bounds on the True Discovery Number (TDN) using either **ceTDP-cons** or **ceTDP-appr**.

### TDP

For a selected region \(S\), the corresponding TDP lower bound is obtained by normalizing the TDN lower bound:

TDP = TDN / |S|,

where |S| denotes the number of voxels in the selected region.

## Software Suite

This repository serves as the entry point for all ceTDP software implementations accompanying:

**Method paper**

> Goeman JJ, Górecki P, Monajemi R, Chen X, Nichols TE & Weeda W. *Cluster extent inference revisited: quantification and localisation of brain activity*. Journal of the Royal Statistical Society Series B, 2023.

**Software paper**

> Chen X, Peek L, Monajemi R, Górecki P, Nichols TE, Goeman JJ & Weeda W. *ceTDP: A Practical Tutorial on Valid and Quantitative Cluster-Extent Inference in Neuroimaging*. arXiv, 2026.

## Available Implementations

### Stage 1: ceTDP-k

| Tool | Language | Description |
|------|----------|-------------|
| ceTDP-k-SPM | MATLAB | Parametric (SPM) |
| ceTDP-k-FSL | FSL | Parametric (FSL pipeline) |
| ceTDP-k-R | R/C++ | Nonparametric permutation inference |

Repository: [**ceTDP-k**](https://github.com/xuchen312/ceTDP-k) 

Outputs:

- minimum significant cluster extent threshold (`k`)
- region specification inputs for Stage 2

### Stage 2: Conservative inference (ceTDP-cons)

| Tool | Language | Repository |
|------|----------|------------|
| ceTDP-cons-SPM | MATLAB | [ceTDP-cons-SPM](https://github.com/xuchen312/ceTDP-cons-SPM) |
| ceTDP-cons-C | C | [ceTDP-cons-C](https://github.com/rmonajemi/ceTDP-cons-C) |
| ceTDP-cons-R | R | [ceTDP-cons-R](https://github.com/xuchen312/ceTDP-cons-R) |
| ceTDP-cons-Python | Python | [ceTDP-cons-Python](https://github.com/xuchen312/ceTDP-cons-Python) |

Computes exact conservative lower bounds on TDN.

### Stage 2: Approximate inference (ceTDP-appr)

| Tool | Language | Repository |
|------|----------|------------|
| ceTDP-appr-C | C | [ceTDP-appr-C]([LINK](https://github.com/ppgorecki/ceTDP-appr)) |

Computes heuristic approximate lower bounds on TDN.

## Auxiliary Utilities

Utility scripts facilitate preprocessing and visualization but are **not part of the inferential procedure**.

| Tool | Description |
|------|-------------|
| `cluster_export.py` | Export supra-threshold clusters and ROI-overlapping subclusters as CSV |
| `cetdp_vis.py` | Generate layered voxel-wise ceTDP visualization maps |

See the utility documentation for detailed usage.

## General Workflow

1. Run **ceTDP-k** to determine the cluster extent threshold (`k`).
2. (Optional) Specify ROIs and prepare overlapping cluster information.
3. Run **ceTDP-cons** or **ceTDP-appr**.
4. Obtain TDN lower bounds and convert to TDP if required.
5. (Optional) Generate layered visualization maps.

## Citation

If you use ceTDP, please cite both the methodological and software papers.

---










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
