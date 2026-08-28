#!/usr/bin/env python3

import os
import argparse
import numpy as np
import pandas as pd
import nibabel as nib

from scipy.ndimage import label

# ============================================================
# Connectivity structure
# ============================================================

def get_structure(connectivity=18):
    """
    Return 3D connectivity structure.

    connectivity:
        6  = face
        18 = edge
        26 = corner
    """

    if connectivity == 6:

        structure = np.zeros((3, 3, 3), dtype=np.uint8)

        structure[1, 1, :] = 1
        structure[1, :, 1] = 1
        structure[:, 1, 1] = 1

    elif connectivity == 18:

        structure = np.ones((3, 3, 3), dtype=np.uint8)

        corners = [(0, 0, 0),
                   (0, 0, 2),
                   (0, 2, 0),
                   (0, 2, 2),
                   (2, 0, 0),
                   (2, 0, 2),
                   (2, 2, 0),
                   (2, 2, 2),]

        for c in corners:
            structure[c] = 0

    elif connectivity == 26:

        structure = np.ones((3, 3, 3), dtype=np.uint8)

    else:

        raise ValueError("Connectivity must be one of: 6, 18, 26")

    return structure

# ============================================================
# Save cluster CSV
# ============================================================

def save_cluster_csv(outfile, ijk):

    df = pd.DataFrame({'x': ijk[:, 0],
                       'y': ijk[:, 1],
                       'z': ijk[:, 2],})

    df.to_csv(outfile, index=False)

# ============================================================
# Main
# ============================================================

def main():

    parser = argparse.ArgumentParser(description='Export suprathreshold clusters to CSV.')

    parser.add_argument(
        '--input', 
        required=True, 
        help='Input statistical map (NIfTI)')

    parser.add_argument(
        '--cdt', 
        required=True, 
        type=float, 
        help='Cluster-defining threshold')

    parser.add_argument(
        '--extent', 
        required=True, 
        type=int, 
        help='Minimum significant cluster size')

    parser.add_argument(
        '--roi', 
        default=None, 
        help='ROI atlas NIfTI')

    parser.add_argument(
        '--connectivity',
        default=18,
        type=int,
        choices=[6, 18, 26],
        help='3D connectivity (default = 18)'
    )

    parser.add_argument(
        '--absolute',
        action='store_true',
        help='Use abs(statmap) >= CDT'
    )

    parser.add_argument(
        '--outdir',
        default='clusters',
        help='Output directory'
    )

    args = parser.parse_args()
    
    os.makedirs(args.outdir, exist_ok=True)

    # ============================================================
    # Load image
    # ============================================================

    img = nib.load(args.input)
    
    data = img.get_fdata()

    # ============================================================
    # Create binary mask
    # ============================================================

    if args.absolute:

        mask = ( np.isfinite(data) & (np.abs(data) >= args.cdt) )

    else:

        mask = ( np.isfinite(data) & (data >= args.cdt) )

    # force binary uint8
    mask = mask.astype(np.uint8)

    # ============================================================
    # Connected-component labeling
    # ============================================================

    structure = get_structure(args.connectivity)

    labels, num = label(mask, structure=structure)

    print(f'Found {num} suprathreshold clusters.')

    # ============================================================
    # ROI MODE
    # ============================================================

    if args.roi is not None:

        roi_img = nib.load(args.roi)
        
        # round ROI labels to integers
        roi = np.rint(roi_img.get_fdata()).astype(np.int32)
        
        roi_labels = np.unique(roi[roi > 0])
        
        print(f'Found {len(roi_labels)} ROI labels.')

        kval = args.extent - 1

        for roi_id in roi_labels:

            # binary ROI mask
            roi_mask = ((roi == roi_id) & (labels > 0)).astype(np.uint8)

            sublabels, subnum = label(roi_mask, structure=structure)

            for j in range(1, subnum + 1):

                idx = (sublabels == j)

                clus_size = int(np.sum(idx))
                
                if clus_size <= kval:
                    continue
                
                ijk = np.column_stack(np.where(idx)) + 1

                outfile = os.path.join(
                    args.outdir,
                    f'roi{roi_id}_subclus{j}_size{clus_size}_kval{kval}.csv'
                )

                save_cluster_csv(outfile, ijk)

                print(f'Wrote: {outfile}')

    # ============================================================
    # WHOLE-BRAIN MODE
    # ============================================================

    else:

        kval = args.extent - 1

        for i in range(1, num + 1):

            idx = (labels == i)

            clus_size = int(np.sum(idx))
            
            if clus_size <= kval:
                continue

            ijk = np.column_stack(np.where(idx)) + 1

            outfile = os.path.join(
                args.outdir,
                f'clus{i}_size{clus_size}_kval{kval}.csv'
            )

            save_cluster_csv(outfile, ijk)

            print(f'Wrote: {outfile}')


if __name__ == '__main__':
    main()
