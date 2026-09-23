# Cluster Export Utility

This utility extracts connected components from significant supra-threshold clusters (STCs) or from the intersection of STCs with specified regions, and exports voxel coordinates for downstream ceTDP analyses.

Both **Python** (`cluster_export.py`) and **MATLAB** (`cluster_export.m`) implementations are provided.

## Overview

The utility identifies connected STCs from statistical images using a user-defined **cluster-defining threshold (CDT)** and **cluster-extent threshold (`k`)**. It can also extract connected components from the intersection of significant STCs with specified regions to prepare the cluster information required for Stage 2 of ceTDP.

### Features

- Connected-component extraction from significant STCs
- Connected-component extraction from STC-region intersections
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

#### Connected components from STC–ROI intersections

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
| `--cdt` | CDT in statistic units (T/Z/F), not p-value |
| `--extent` | Minimum cluster-extent threshold (`k`) |
| `--roi` | Optional ROI or region NIfTI mask |
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
- `ROI` — *optional* NIfTI file or volume defining specified regions

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

Each CSV file contains voxel coordinates, e.g.,

```text
x,y,z
31,42,18
32,42,18
33,42,18
...
```

The exported voxel coordinates are 1-based voxel indices, consistent with MATLAB/SPM indexing.

### Whole-brain clusters

When no region is specified, surviving STCs are exported as separate CSV files.

### Connected components from STC–ROI intersections

When an ROI mask is provided, the utility intersects the significant STCs with the specified regions and identifies connected components within the intersection. Each connected component is exported as a separate CSV file.

The resulting CSV files provide the connected-component information required for subsequent Stage 2 ceTDP analyses.

## Typical Workflow

1. Obtain a statistical NIfTI image.
2. Determine the appropriate CDT.
3. Determine the cluster-extent threshold (`k`) using **ceTDP-k**.
4. Extract connected components from the significant STCs.
5. *(Optional)* Specify an ROI mask to extract connected components from its intersection with the significant STCs.
6. Export voxel coordinates as CSV files.
7. Use the resulting CSV files as connected-component information for Stage 2 of ceTDP.

### Example

```bash
python cluster_export.py \
    --input spmT_0001.nii \
    --cdt 3.1 \
    --extent 20 \
    --outdir clusters
```

## Notes

This utility performs **connected-component extraction** from significant STCs based on the supplied CDT and cluster-extent threshold (`k`). It does not determine the statistical CDT or perform the core Stage 2 TDN/TDP inference itself.

The appropriate CDT and `k` should therefore be determined by the corresponding statistical analysis and **ceTDP-k** procedure.
