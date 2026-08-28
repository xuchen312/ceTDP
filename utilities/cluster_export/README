# Cluster Export Utility

This utility extracts connected supra-threshold clusters from statistical NIfTI images and exports voxel coordinates for downstream ceTDP analyses.

Both **Python** (`cluster_export.py`) and **MATLAB** (`cluster_export.m`) implementations are provided.

## Overview

The utility identifies connected supra-threshold clusters from statistical images using a user-defined **cluster-forming threshold (CFT)** and **cluster-extent threshold (`k`)**. It can also extract ROI-overlapping subclusters to prepare the cluster information required for Stage 2 of ceTDP.

### Features

- Whole-brain cluster extraction
- ROI-overlapping subcluster extraction
- Configurable 3D connectivity (6, 18, or 26)
- Export of voxel coordinates as CSV
- Compatible with arbitrary NIfTI statistical maps
- Available in both Python and MATLAB

## Python Implementation

### Requirements

```bash
pip install nibabel numpy pandas scipy
```

### Basic usage

#### Whole-brain clusters

```bash
python cluster_export.py \
    --input spmT_0001.nii \
    --cdt 3.1 \
    --extent 20
```

#### ROI-overlapping subclusters

```bash
python cluster_export.py \
    --input spmT_0001.nii \
    --roi ROI.nii.gz \
    --cdt 3.1 \
    --extent 20
```

## MATLAB Implementation

Run the MATLAB version directly:

```matlab
cluster_export
```

The MATLAB implementation provides equivalent functionality for extracting both whole-brain clusters and ROI-overlapping subclusters.

## Output

CSV files are written to the output directory (default: `clusters/`).

Each CSV contains voxel coordinates:

```text
x,y,z
```

These CSV files provide the cluster information required for Stage 2 of ceTDP.

## Typical Workflow

1. Load a statistical NIfTI image.
2. Apply the CFT.
3. Remove clusters smaller than the cluster extent threshold (`k`).
4. *(Optional)* Restrict clusters to user-defined ROIs.
5. Export voxel coordinates as CSV files for Stage 2 ceTDP analyses.
