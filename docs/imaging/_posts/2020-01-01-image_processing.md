---
title: "Image Processing"
excerpt: "Image Processing"
layout: single

---
The [“FAIRly-big” strategy](https://www.nature.com/articles/s41597-022-01163-2) (Wagner et al., 2021) was adopted for reproducible image processing, ensuring all preparation and analyses were accompanied by a full audit trail in [Datalad](https://www.datalad.org/) (Halchenko et al., 2021).
Structural MRI data were processed using [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/) and [sMRIPrep](https://www.nipreps.org/smriprep/), yielding commonly used measures of brain structure
RBC provides full FreeSurfer outputs as well as tabulated data parcellated using 35 anatomical, functional, and multimodal atlases such as Desikan Killiany, Glasser, Gordon, and multiple Schaefer parcellations.
Specific features include commonly used measures such as regional surface area, cortical thickness, gray matter volume, folding and curvature indices, etc.
Moreover, summary brain measures (e.g., mean and standard deviation of various measures) are provided for the whole brain and per hemisphere.
Tabulated data are also accompanied by .json files describing each structural feature in detail.

Functional data were processed using [C-PAC](https://fcp-indi.github.io/docs/nightly/user/quick) -
or Configurable Pipeline for the Analysis of Connectomes (Craddock et al., 2013).
These steps were all carried out in [Datalad](https://www.datalad.org/) to keep track of provenance and ensure the ultimate reproducibility for all datasets.
Following [extensive benchmarking and harmonization studies](https://www.biorxiv.org/content/10.1101/2021.12.01.470790v3.abstract) (Li et al., 2021), C-PAC was executed using a configuration file that was crafted specifically for RBC, which is available [here](https://github.com/FCP-INDI/C-PAC/blob/0182f98c61cb7fbb495c8300e6a6a7991c859240/CPAC/resources/configs/pipeline_config_rbc-options.yml#L172).
C-PAC outputs include measures such as fully-processed functional timeseries, functional connectivity matrices, ReHo (regional homogeneity), ALFF (amplitude of low frequency fluctuation), as well as extensive measures of quality control.
Derivatives are available in volumetric MNI space as well as in parcellated format using 16 different atlases, including Glasser and Schaefer parcellations.
A more detailed description of the list of outputs can be obtained [here](https://fcp-indi.github.io/docs/nightly/user/output_dir).

A repository describing all of the atlases used by C-PAC in RBC can be found [here](https://github.com/FCP-INDI/C-PAC_templates/tree/d2913cd6d5861d9cb5ffb79aa03da18b6eb603eb/sourcedata/atlases).

## 07/06/2026: fMRIPrep and XCP-D Release

RBC now also provides fMRIPrep, FreeSurfer, and XCP-D derivatives.
For more information, see the [fMRIPrep and XCP-D Release section on the Get Data page]({{ "/docs/get_data#fmriprep-xcpd-pipeline-release" | relative_url }}).

Structural MRI data were processed with [fMRIPrep](https://fmriprep.org/) using the `--anat-only` flag.
T1w images were corrected for intensity non-uniformity with ANTs `N4BiasFieldCorrection`, skull-stripped with the ANTs brain extraction workflow using the OASIS30ANTs as target template, and segmented into CSF, white matter, and gray matter with FSL `FAST`.
Brain surfaces were reconstructed with FreeSurfer `recon-all`, and the brain mask was refined by reconciling ANTs-derived and FreeSurfer-derived cortical gray matter segmentations.
T1w images were nonlinearly normalized to MNI152NLin6Asym and MNI152NLin2009cAsym templates accessed through `TemplateFlow`. Grayordinate "dscalar" files containing 91k samples were resampled onto fsLR using the Connectome Workbench. Finally, 
FreeSurfer outputs were further processed with [FreeSurfer-Post](https://github.com/PennLINC/freesurfer-post) to produce tabulated structural data.

Functional MRI data were preprocessed with [fMRIPrep](https://fmriprep.org/).
For each BOLD run, fMRIPrep generated a BOLD reference, estimated head-motion parameters with FSL `MCFLIRT`, and co-registered the BOLD reference to the T1w reference with FreeSurfer `bbregister` boundary-based registration.
Confound time series include framewise displacement (FD), DVARS, global CSF, white matter, and whole-brain signals, CompCor physiological regressors, motion estimates, temporal derivatives, and quadratic terms.
Frames exceeding 0.5 mm FD or 1.5 standardized DVARS were annotated as motion outliers. Grayordinates files containing 91k samples were also generated with surface data transformed directly to fsLR space and subcortical data transformed to 2 mm resolution MNI152NLin6Asym space. All resamplings can be performed with a single interpolation step by composing all the pertinent transformations (i.e. head-motion transform matrices, susceptibility distortion correction when available, and co-registrations to anatomical and output spaces). Gridded (volumetric) resamplings were performed using nitransforms, configured with cubic B-spline interpolation.

Post-processing of fMRIPrep outputs was performed with [XCP-D](https://xcp-d.readthedocs.io/en/latest/) using the `--mode linc` flag.
XCP-D discarded non-steady-state volumes, selected 36 nuisance regressors, despiked BOLD data with AFNI `3dDespike`, band-pass filtered the data to retain 0.01–0.08 Hz signals, and smoothed denoised BOLD data with a 6 mm FWHM Gaussian kernel. Atlases used in the workflow included the Schaefer 4S atlas at 10 resolutions, Glasser, Gordon, Tian, HCP, and MIDB. XCP-D produced processed functional timeseries, pairwise functional connectivity, ALFF, and ReHo, with surface ReHo computed using `2dReHo` and subcortical ReHo computed using AFNI `3dReHo`.
