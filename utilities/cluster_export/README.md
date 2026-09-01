# Cluster Export Utility

This utility extracts connected supra-threshold clusters from statistical NIfTI images and exports voxel coordinates for downstream ceTDP analyses.

Both **Python** (`cluster_export.py`) and **MATLAB** (`cluster_export.m`) implementations are provided.

## Overview

The utility identifies connected supra-threshold clusters from statistical images using a user-defined **cluster-defining threshold (CDT)** and **cluster-extent threshold (`k`)**. It can also extract ROI-overlapping subclusters to prepare the cluster information required for Stage 2 of ceTDP.

### Features

- Whole-brain cluster extraction
- ROI-overlapping subcluster extraction
- Configurable 3D connectivity
- Export of voxel coordinates as CSV
- Compatible with arbitrary NIfTI statistical maps
- Available in both Python and MATLAB

## Python Implementation

### Requirements

```bash
pip install nibabel numpy pandas scipy
```

### Basic Usage

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

### Arguments

| Argument | Description |
|----------|-------------|
| `--input` | Input statistical NIfTI image |
| `--cdt` | Cluster-defining threshold in statistic units (T/Z/F), not p-value |
| `--extent` | Minimum cluster-extent threshold (`k`) |
| `--roi` | Optional ROI atlas NIfTI |
| `--connectivity` | 3D connectivity: 6, 18, or 26 (default: 18) |
| `--absolute` | Use `abs(statistic) >= CDT` instead of `statistic >= CDT` |
| `--outdir` | Output directory (default: `clusters/`) |

### CDT Input

In the Python implementation, `--cdt` must be provided as a **statistic threshold**, such as a T, Z, or F value.

For example:

```bash
--cdt 3.1
```

The Python implementation does not read `SPM.mat` or `xSPM` and therefore does not convert an uncorrected p-value into a statistic threshold automatically.

For example, the following is not valid:

```bash
--cdt 0.001
```

If the CDT is defined by an uncorrected p-value, it must first be converted to the corresponding statistic threshold using the appropriate statistical model and degrees of freedom.

> **Note:** The MATLAB implementation can accept an uncorrected p-value as `cdt` when an `xSPM` structure is provided, using SPM's statistical information for the conversion.

### Connectivity

The Python implementation uses **18-connectivity by default**.

Supported values are:

```bash
--connectivity 6
--connectivity 18
--connectivity 26
```

These correspond to:

- **6-connectivity**: face-connected voxels
- **18-connectivity**: face- and edge-connected voxels
- **26-connectivity**: face-, edge-, and corner-connected voxels

### Absolute Threshold

By default, the Python implementation extracts voxels satisfying:

```text
statistic >= CDT
```

The optional `--absolute` flag instead uses:

```text
abs(statistic) >= CDT
```

For example:

```bash
python cluster_export.py \
    --input spmT_0001.nii \
    --cdt 3.1 \
    --extent 20 \
    --absolute
```

This allows both positive and negative supra-threshold statistics to be included.

## MATLAB Implementation

The MATLAB implementation is provided as:

```matlab
cluster_export.m
```

### Basic Usage

Run the function directly:

```matlab
cluster_export
```

The function can also be called with the minimum cluster extent threshold:

```matlab
cluster_export(minClusSz)
```

The full interface is:

```matlab
cluster_export(minClusSz, xSPM, cdt, ROI)
```

where:

- `minClusSz` — minimum cluster-extent threshold
- `xSPM` — *optional* SPM results structure
- `cdt` — *optional* cluster-defining threshold
- `ROI` — *optional* ROI NIfTI file or ROI volume

When `xSPM` is provided, an uncorrected p-value can be supplied as `cdt` and converted to the corresponding statistic threshold using SPM.

For example:

```matlab
cluster_export(20, xSPM, 0.001)
```

## Output

The utility exports cluster voxel coordinates as CSV files.

### Python

By default, CSV files are written to

```bash
clusters/
```

The output directory can be changed using:

```bash
--outdir <directory>
```

For example:

```bash
python cluster_export.py \
    --input spmT_0001.nii \
    --cdt 3.1 \
    --extent 20 \
    --outdir results
```

### MATLAB

The MATLAB implementation saves CSV files directly to the current working directory. It does not create a separate output directory by default.

### CSV Contents

Each CSV file contains voxel coordinates:

```text
x,y,z
31,42,18
32,42,18
33,42,18
...
```

The exported voxel coordinates are 1-based voxel indices, consistent with MATLAB/SPM indexing.

### Whole-brain clusters

When no ROI is specified, surviving supra-threshold clusters are exported as separate CSV files.

### ROI-overlapping subclusters

When an ROI atlas is provided, the utility intersects the supra-threshold clusters with the ROI and identifies connected ROI-overlapping subclusters. Each surviving subcluster is exported as a separate CSV file.

The resulting CSV files provide the cluster information required for subsequent Stage 2 ceTDP analyses.

## Typical Workflow

1. Obtain a statistical NIfTI image.
2. Determine the appropriate CDT.
3. Determine the cluster-extent threshold (`k`) using **ceTDP-k**.
4. Extract significant supra-threshold clusters.
5. *(Optional)* Provide an ROI atlas to extract ROI-overlapping subclusters.
6. Export voxel coordinates as CSV files.
7. Use the resulting CSV files as cluster information for Stage 2 of ceTDP.

### Example

```bash
python cluster_export.py \
    --input spmT_0001.nii \
    --cdt 3.1 \
    --extent 20 \
    --outdir clusters
```

## Notes

This utility performs **cluster extraction** based on supplied CDT and cluster-extent threshold (`k`). It does not determine the statistical CDT or perform the Stage 2 TDN/TDP inference itself.

The appropriate CDT and `k` should therefore be determined by the corresponding statistical analysis and **ceTDP-k** procedure.
