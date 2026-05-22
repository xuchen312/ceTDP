#!/usr/bin/env python3

import os
import argparse
import numpy as np
import pandas as pd
import nibabel as nib

from scipy.ndimage import label


# --------------------------------------------------
# connectivity helper
# --------------------------------------------------

def get_structure(connectivity=18):
    """
    Return 3D connectivity structure.

    connectivity:
        6  = face
        18 = edge
        26 = corner
    """

    if connectivity == 6:
        structure = np.zeros((3, 3, 3), dtype=int)
        structure[1, 1, :] = 1
        structure[1, :, 1] = 1
        structure[:, 1, 1] = 1

    elif connectivity == 18:
        structure = np.ones((3, 3, 3), dtype=int)
        corners = [
            (0, 0, 0),
            (0, 0, 2),
            (0, 2, 0),
            (0, 2, 2),
            (2, 0, 0),
            (2, 0, 2),
            (2, 2, 0),
            (2, 2, 2),
        ]
        for c in corners:
            structure[c] = 0

    elif connectivity == 26:
        structure = np.ones((3, 3, 3), dtype=int)

    else:
        raise ValueError("Connectivity must be one of: 6, 18, 26")

    return structure


# --------------------------------------------------
# save cluster csv
# --------------------------------------------------

def save_cluster_csv(outfile, ijk):

    df = pd.DataFrame({
        'i': ijk[:, 0],
        'j': ijk[:, 1],
        'k': ijk[:, 2],
    })

    df.to_csv(outfile, index=False)


# --------------------------------------------------
# main
# --------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description='Export suprathreshold clusters to CSV.'
    )
    
    parser.add_argument(
        '--input',
        required=True,
        help='Input statistical map (NIfTI)'
    )

    parser.add_argument(
        '--cdt',
        required=True,
        type=float,
        help='Cluster-defining threshold'
    )

    parser.add_argument(
        '--extent',
        required=True,
        type=int,
        help='Minimum significant cluster size'
    )

    parser.add_argument(
        '--roi',
        default=None,
        help='ROI atlas NIfTI'
    )

    parser.add_argument(
        '--connectivity',
        default=18,
        type=int,
        choices=[6, 18, 26],
        help='3D connectivity'
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
    
    # --------------------------------------------------
    # load image
    # --------------------------------------------------

    img = nib.load(args.input)
    data = img.get_fdata()

    # --------------------------------------------------
    # thresholding
    # --------------------------------------------------

    if args.absolute:
        mask = np.abs(data) >= args.cdt
    else:
        mask = data >= args.cdt

    # --------------------------------------------------
    # connected component labeling
    # --------------------------------------------------

    structure = get_structure(args.connectivity)

    labels, num = label(mask, structure=structure)

    print(f'Found {num} suprathreshold clusters.')
    
    # --------------------------------------------------
    # ROI mode
    # --------------------------------------------------

    if args.roi is not None:

        roi_img = nib.load(args.roi)
        roi = roi_img.get_fdata()

        roi_labels = np.unique(roi[roi > 0]).astype(int)

        print(f'Found {len(roi_labels)} ROI labels.')

        for roi_id in roi_labels:

            roi_mask = (roi == roi_id) & (labels > 0)

            sublabels, subnum = label(
                roi_mask,
                structure=structure
            )

            for j in range(1, subnum + 1):

                idx = (sublabels == j)
                clus_size = np.sum(idx)

                if clus_size < args.extent:
                    continue
                
                ijk = np.argwhere(idx) + 1

                outfile = os.path.join(
                    args.outdir,
                    f'roi{roi_id}_subclus{j}_size{clus_size}.csv'
                )
                
                save_cluster_csv(outfile, ijk)

                print(f'Wrote: {outfile}')
                
    # --------------------------------------------------
    # whole-brain mode
    # --------------------------------------------------

    else:

        for i in range(1, num + 1):

            idx = (labels == i)
            clus_size = np.sum(idx)

            if clus_size < args.extent:
                continue

            ijk = np.argwhere(idx) + 1

            outfile = os.path.join(
                args.outdir,
                f'clus{i}_size{clus_size}.csv'
            )
            
            save_cluster_csv(outfile, ijk)

            print(f'Wrote: {outfile}')


if __name__ == '__main__':
    main()
