# ceTDP Visualization Utility

This utility generates a voxel-wise NIfTI visualization map encoding both conservative and heuristic ceTDP results from cluster label images and cluster-level TDP measures.

The output is a NIfTI image that can be visualized using standard neuroimaging software such as FSLeyes, MRIcron, or Nilearn.

## Overview

For each cluster, the visualization combines the two ceTDP measures:

- **Cluster interior:** conservative TDP lower bounds (ceTDP-cons)
- **Inner boundary:** heuristic TDP estimates (ceTDP-heur)

This layered representation provides an intuitive visualization of the complementary TDP measures while remaining fully voxel-lattice based.

## Features

- Layered ceTDP visualization
- Conservative interior and heuristic boundary encoding
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

A CSV file containing the two cluster-level ceTDP measures for each cluster, e.g.,

```csv
cluster_id,tdp1,tdp2
21,0.018,0.158
22,0.223,0.312
23,0.205,0.296
```

where:

- `tdp1` = conservative TDP lower bound (ceTDP-cons)
- `tdp2` = heuristic TDP estimate (ceTDP-heur)

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

Supported 3D connectivity values:

- 6
- 18
- 26 (default)

## Output

The utility generates a voxel-wise layered visualization map:

```text
cetdp_vis.nii.gz
```

Voxel values represent:

| Region | Encoded Measure |
|---------|--------------|
| Cluster interior | Conservative TDP lower bound (ceTDP-cons) |
| Inner boundary | Heuristic TDP estimate (ceTDP-heur) |
| Background | 0 |

## Visualization

The generated NIfTI image can be opened directly in:

- FSLeyes
- MRIcron
- Nilearn

Example:

```bash
fsleyes cetdp_vis.nii.gz
```

## Visualization Rationale

The layered visualization encodes conservative TDP lower bounds within cluster interiors and heuristic TDP estimates (typically tighter) along cluster boundaries.

This provides an intuitive visualization of complementary TDP measures while preserving the voxel lattice structure.
