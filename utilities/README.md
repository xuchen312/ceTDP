# ceTDP Utilities

Auxiliary tools for Stage 1 region specification and visualization.

## Available tools

### cluster_export

Export connected components from significant supra-threshold clusters (STCs) or from the intersection of STCs with specified regions as CSV.

Implementations:

- Python: `cluster_export.py`
- MATLAB: `cluster_export.m`

See `cluster_export/README.md`.

### cetdp_vis

Generate a voxel-wise NIfTI visualization map encoding both conservative and heuristic TDP results.

Implementation:

- Python: `cetdp_vis.py`

See `cetdp_vis/README.md`.
