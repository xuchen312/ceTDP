#!/usr/bin/env python3

"""
ceTDP visualization utility

Creates layered ceTDP visualization maps.

Interior voxels:
    ceTDP-cons TDP values

Inner boundary voxels:
    ceTDP-appr TDP values

Requirements:
    pip install nibabel numpy pandas scipy

Example:
    python cetdp_vis.py
    
    python cetdp_vis.py \
    --cluster clus.nii.gz \
    --table tdps.csv \
    --connectivity 26 \
    --output cetdp_vis.nii.gz
"""

import argparse
import os

import numpy as np
import pandas as pd
import nibabel as nib

from scipy.ndimage import (
    binary_erosion,
    generate_binary_structure
)


# ============================================================
# boundary extraction
# ============================================================

def extract_boundary(mask, connectivity):

    if connectivity == 6:
        structure = generate_binary_structure(3,1)
    elif connectivity in [18,26]:
        structure = generate_binary_structure(3,2)
    else:
        raise ValueError('3D connectivity must be 6, 18, or 26')
        
    eroded = binary_erosion(
        mask,
        structure=structure,
        iterations=1,
        border_value=0
    )

    boundary = mask & (~eroded)

    return boundary


# ============================================================
# save nifti
# ============================================================

def save_nifti(data, outfile, template_img):

    outdir = os.path.dirname(outfile)

    if outdir != '':
        os.makedirs(outdir, exist_ok=True)

    out = nib.Nifti1Image(
        data.astype(np.float32),
        affine=template_img.affine,
        header=template_img.header
    )

    nib.save(out, outfile)

    print(f"Saved: {outfile}")


# ============================================================
# main
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description='Render ceTDP cluster visualization.'
    )

    parser.add_argument(
        '--cluster',
        required=True,
        help='Cluster label NIfTI'
    )

    parser.add_argument(
        '--table',
        required=True,
        help='CSV with cluster id, tdp1, tdp2'
    )
    
    parser.add_argument(
        '--connectivity',
        default=26,
        type=int,
        choices=[6, 18, 26],
        help='Boundary connectivity (18 and 26 currently equivalent)'
    )

    parser.add_argument(
        '--output',
        default='cetdp_vis.nii.gz',
        help='Output NIfTI'
    )

    args = parser.parse_args()

    # --------------------------------------------------------
    # load cluster image
    # --------------------------------------------------------

    clus_img = nib.load(args.cluster)
    
    clus = clus_img.get_fdata()

    # --------------------------------------------------------
    # validate cluster labels
    # --------------------------------------------------------

    if not np.allclose(clus, np.round(clus)):
        raise ValueError('Cluster image must contain integer labels')

    clus = np.round(clus).astype(np.int32)

    # --------------------------------------------------------
    # load table
    # --------------------------------------------------------

    tab = pd.read_csv(args.table)

    required_cols = ['cluster_id', 'tdp1', 'tdp2']

    for col in required_cols:
        if col not in tab.columns:
            raise ValueError(f'Missing column: {col}')

    # --------------------------------------------------------
    # initialize output
    # --------------------------------------------------------

    out = np.zeros(clus.shape, dtype=np.float32)

    # --------------------------------------------------------
    # process clusters
    # --------------------------------------------------------

    for _, row in tab.iterrows():
        
        cid = int(row['cluster_id'])
        tdp1 = row['tdp1']
        tdp2 = row['tdp2']
        
        if tdp2 < tdp1:
            print(f'Warning: cluster {cid} has tdp2 < tdp1')

        print(f'Processing cluster {int(cid)}')

        mask = (clus == cid)

        if np.sum(mask) == 0:
            print(f'Warning: cluster {cid} not found')
            continue

        boundary = extract_boundary(mask, args.connectivity)

        interior = mask & (~boundary)

        # --------------------------------------------
        # assign values
        # --------------------------------------------

        out[interior] = tdp1

        out[boundary] = tdp2

    # --------------------------------------------------------
    # save
    # --------------------------------------------------------
    
    print(
        f'Rendered {len(tab)} clusters '
        f'using {args.connectivity}-connectivity.'
    )

    save_nifti(out, args.output, clus_img)

    print('Done.')


# ============================================================
# entry
# ============================================================

if __name__ == '__main__':
    main()
