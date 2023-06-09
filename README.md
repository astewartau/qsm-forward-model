# QSM Forward Model

Based on Marques, J. P., et al. (2021). QSM reconstruction challenge 2.0: A realistic in silico head phantom for MRI data simulation and evaluation of susceptibility mapping procedures. Magnetic Resonance in Medicine, 86(1), 526-542. https://doi.org/10.1002/mrm.28716

Includes code for:

 - Field model (forward multiplication with dipole kernel based on chi)
 - Signal model (magnitude and phase simulation based on field/M0/R1/R2star)
 - Phase offset model
 - Noise model
 - Shim field model
 - k-space cropping

## Install

```
pip install qsm-forward
```

## Example using simulated sources

In this example, we simulated susceptibility sources (spheres and rectangles) to generate a BIDS directory:

```python
import qsm_forward

if __name__ == "__main__":
    recon_params = qsm_forward.ReconParams()
    recon_params.subject = "simulated-sources"
    recon_params.peak_snr = 100

    tissue_params = qsm_forward.TissueParams(chi=qsm_forward.simulate_susceptibility_sources())
    
    qsm_forward.generate_bids(tissue_params, recon_params, "bids")
```

```
bids/
└── sub-simulated-sources
    └── ses-1
        ├── anat
        │   ├── sub-simulated-sources_ses-1_run-1_echo-1_part-mag_MEGRE.json
        │   ├── sub-simulated-sources_ses-1_run-1_echo-1_part-mag_MEGRE.nii
        │   ├── sub-simulated-sources_ses-1_run-1_echo-1_part-phase_MEGRE.json
        │   ├── sub-simulated-sources_ses-1_run-1_echo-1_part-phase_MEGRE.nii
        │   ├── sub-simulated-sources_ses-1_run-1_echo-2_part-mag_MEGRE.json
        │   ├── sub-simulated-sources_ses-1_run-1_echo-2_part-mag_MEGRE.nii
        │   ├── sub-simulated-sources_ses-1_run-1_echo-2_part-phase_MEGRE.json
        │   ├── sub-simulated-sources_ses-1_run-1_echo-2_part-phase_MEGRE.nii
        │   ├── sub-simulated-sources_ses-1_run-1_echo-3_part-mag_MEGRE.json
        │   ├── sub-simulated-sources_ses-1_run-1_echo-3_part-mag_MEGRE.nii
        │   ├── sub-simulated-sources_ses-1_run-1_echo-3_part-phase_MEGRE.json
        │   ├── sub-simulated-sources_ses-1_run-1_echo-3_part-phase_MEGRE.nii
        │   ├── sub-simulated-sources_ses-1_run-1_echo-4_part-mag_MEGRE.json
        │   ├── sub-simulated-sources_ses-1_run-1_echo-4_part-mag_MEGRE.nii
        │   ├── sub-simulated-sources_ses-1_run-1_echo-4_part-phase_MEGRE.json
        │   └── sub-simulated-sources_ses-1_run-1_echo-4_part-phase_MEGRE.nii
        └── extra_data
            ├── sub-simulated-sources_ses-1_run-1_chi.nii
            ├── sub-simulated-sources_ses-1_run-1_mask.nii
            └── sub-simulated-sources_ses-1_run-1_segmentation.nii
```

Some repesentative images including the mask, first and last-echo phase image, and ground truth susceptibility (chi):

![Image](https://i.imgur.com/dtklHUh.png)

## Example using head phantom data

In this example, we generate a BIDS-compliant dataset based on head phantom maps. You must provide these maps yourself by gaining access to the QSM Challenge 2.0 head phantom data or generating your own realistic maps:

```python
import qsm_forward
import numpy as np

if __name__ == "__main__":
    tissue_params = qsm_forward.TissueParams("../head-phantom-maps")
    
    recon_params_all = [
        qsm_forward.ReconParams(voxel_size=voxel_size, peak_snr=100, session=session)
        for (voxel_size, session) in [
            (np.array([0.8, 0.8, 0.8]), "0p8"),
            (np.array([1.0, 1.0, 1.0]), "1p0"),
            (np.array([1.2, 1.2, 1.2]), "1p2")
        ]
    ]

    for recon_params in recon_params_all:    
        qsm_forward.generate_bids(tissue_params=tissue_params, recon_params=recon_params, bids_dir="bids")
```

```
bids/
└── sub-1
    ├── ses-0p8
    │   ├── anat
    │   │   ├── sub-1_ses-0p8_run-1_echo-1_part-mag_MEGRE.json
    │   │   ├── sub-1_ses-0p8_run-1_echo-1_part-mag_MEGRE.nii
    │   │   ├── sub-1_ses-0p8_run-1_echo-1_part-phase_MEGRE.json
    │   │   ├── sub-1_ses-0p8_run-1_echo-1_part-phase_MEGRE.nii
    │   │   ├── sub-1_ses-0p8_run-1_echo-2_part-mag_MEGRE.json
    │   │   ├── sub-1_ses-0p8_run-1_echo-2_part-mag_MEGRE.nii
    │   │   ├── sub-1_ses-0p8_run-1_echo-2_part-phase_MEGRE.json
    │   │   ├── sub-1_ses-0p8_run-1_echo-2_part-phase_MEGRE.nii
    │   │   ├── sub-1_ses-0p8_run-1_echo-3_part-mag_MEGRE.json
    │   │   ├── sub-1_ses-0p8_run-1_echo-3_part-mag_MEGRE.nii
    │   │   ├── sub-1_ses-0p8_run-1_echo-3_part-phase_MEGRE.json
    │   │   ├── sub-1_ses-0p8_run-1_echo-3_part-phase_MEGRE.nii
    │   │   ├── sub-1_ses-0p8_run-1_echo-4_part-mag_MEGRE.json
    │   │   ├── sub-1_ses-0p8_run-1_echo-4_part-mag_MEGRE.nii
    │   │   ├── sub-1_ses-0p8_run-1_echo-4_part-phase_MEGRE.json
    │   │   └── sub-1_ses-0p8_run-1_echo-4_part-phase_MEGRE.nii
    │   └── extra_data
    │       ├── sub-1_ses-0p8_run-1_chi.nii
    │       ├── sub-1_ses-0p8_run-1_mask.nii
    │       └── sub-1_ses-0p8_run-1_segmentation.nii
    ├── ses-1p0
    │   ├── anat
    │   │   ├── sub-1_ses-1p0_run-1_echo-1_part-mag_MEGRE.json
    │   │   ├── sub-1_ses-1p0_run-1_echo-1_part-mag_MEGRE.nii
    │   │   ├── sub-1_ses-1p0_run-1_echo-1_part-phase_MEGRE.json
    │   │   ├── sub-1_ses-1p0_run-1_echo-1_part-phase_MEGRE.nii
    │   │   ├── sub-1_ses-1p0_run-1_echo-2_part-mag_MEGRE.json
    │   │   ├── sub-1_ses-1p0_run-1_echo-2_part-mag_MEGRE.nii
    │   │   ├── sub-1_ses-1p0_run-1_echo-2_part-phase_MEGRE.json
    │   │   ├── sub-1_ses-1p0_run-1_echo-2_part-phase_MEGRE.nii
    │   │   ├── sub-1_ses-1p0_run-1_echo-3_part-mag_MEGRE.json
    │   │   ├── sub-1_ses-1p0_run-1_echo-3_part-mag_MEGRE.nii
    │   │   ├── sub-1_ses-1p0_run-1_echo-3_part-phase_MEGRE.json
    │   │   ├── sub-1_ses-1p0_run-1_echo-3_part-phase_MEGRE.nii
    │   │   ├── sub-1_ses-1p0_run-1_echo-4_part-mag_MEGRE.json
    │   │   ├── sub-1_ses-1p0_run-1_echo-4_part-mag_MEGRE.nii
    │   │   ├── sub-1_ses-1p0_run-1_echo-4_part-phase_MEGRE.json
    │   │   └── sub-1_ses-1p0_run-1_echo-4_part-phase_MEGRE.nii
    │   └── extra_data
    │       ├── sub-1_ses-1p0_run-1_chi.nii
    │       ├── sub-1_ses-1p0_run-1_mask.nii
    │       └── sub-1_ses-1p0_run-1_segmentation.nii
    └── ses-1p2
        ├── anat
        │   ├── sub-1_ses-1p2_run-1_echo-1_part-mag_MEGRE.json
        │   ├── sub-1_ses-1p2_run-1_echo-1_part-mag_MEGRE.nii
        │   ├── sub-1_ses-1p2_run-1_echo-1_part-phase_MEGRE.json
        │   ├── sub-1_ses-1p2_run-1_echo-1_part-phase_MEGRE.nii
        │   ├── sub-1_ses-1p2_run-1_echo-2_part-mag_MEGRE.json
        │   ├── sub-1_ses-1p2_run-1_echo-2_part-mag_MEGRE.nii
        │   ├── sub-1_ses-1p2_run-1_echo-2_part-phase_MEGRE.json
        │   ├── sub-1_ses-1p2_run-1_echo-2_part-phase_MEGRE.nii
        │   ├── sub-1_ses-1p2_run-1_echo-3_part-mag_MEGRE.json
        │   ├── sub-1_ses-1p2_run-1_echo-3_part-mag_MEGRE.nii
        │   ├── sub-1_ses-1p2_run-1_echo-3_part-phase_MEGRE.json
        │   ├── sub-1_ses-1p2_run-1_echo-3_part-phase_MEGRE.nii
        │   ├── sub-1_ses-1p2_run-1_echo-4_part-mag_MEGRE.json
        │   ├── sub-1_ses-1p2_run-1_echo-4_part-mag_MEGRE.nii
        │   ├── sub-1_ses-1p2_run-1_echo-4_part-phase_MEGRE.json
        │   └── sub-1_ses-1p2_run-1_echo-4_part-phase_MEGRE.nii
        └── extra_data
            ├── sub-1_ses-1p2_run-1_chi.nii
            ├── sub-1_ses-1p2_run-1_mask.nii
            └── sub-1_ses-1p2_run-1_segmentation.nii
```

Some repesentative images including the ground truth chi map, first-echo magnitude image, and first and last-echo phase images:

![Image](https://i.imgur.com/cE1cQ3U.png)


