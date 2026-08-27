# ceTDP Visualization Utility

This utility generates layered voxelwise ceTDP visualization maps from cluster label images and cluster-level TDP estimates.

The output is a NIfTI image that can be visualized using standard neuroimaging software such as **FSLeyes**, **MRIcroGL**, **ITK-SNAP**, or **nilearn**.

## Overview

For each cluster, the visualization combines the two ceTDP inference methods:

- **Cluster interior:** conservative ceTDP-cons TDP values
- **Inner boundary:** approximate ceTDP-appr TDP values

This layered representation highlights spatial heterogeneity while remaining fully voxel-lattice based.

## Features

- Layered ceTDP visualization
- Inner-boundary enhancement
- Configurable 3D connectivity (6, 18, or 26)
- Command-line interface
- Direct NIfTI output
- Compatible with arbitrary cluster label images

## Requirements

```bash
pip install nibabel numpy pandas scipy
```

## Input

The utility requires two files.

### 1. Cluster label image

A NIfTI image in which voxel values correspond to cluster labels:

```text
clus.nii.gz
```

Label convention:

- `0` = background
- Positive integers = cluster IDs

### 2. Cluster-level TDP table

A CSV file containing ceTDP estimates for each cluster:

```csv
cluster_id,tdp1,tdp2
21,0.018,0.158
22,0.223,0.312
23,0.205,0.296
```

where:

- `tdp1` = ceTDP-cons TDP estimate
- `tdp2` = ceTDP-appr TDP estimate

## Usage

### Basic

```bash
python cetdp_vis.py \
    --cluster clus.nii.gz \
    --table tdp_values.csv
```

### Custom output

```bash
python cetdp_vis.py \
    --cluster clus.nii.gz \
    --table tdp_values.csv \
    --output output/cetdp_vis.nii.gz
```

### Connectivity

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

## Output

The utility generates a voxelwise layered visualization map:

```text
cetdp_vis.nii.gz
```

Voxel values represent:

| Region | Value source |
|---------|--------------|
| Cluster interior | ceTDP-cons |
| Inner boundary | ceTDP-appr |
| Background | 0 |

## Visualization

The generated NIfTI image can be opened directly in:

- FSLeyes
- MRIcroGL
- ITK-SNAP
- nilearn

Example:

```bash
fsleyes cetdp_vis.nii.gz
```

## Visualization Rationale

The layered visualization combines conservative ceTDP-cons estimates within cluster interiors with potentially tighter ceTDP-appr estimates along cluster boundaries.

This provides an intuitive visualization of spatial uncertainty and heterogeneity in cluster-level activation quantification while preserving the voxel lattice structure.
